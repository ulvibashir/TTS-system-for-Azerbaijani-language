"""
Prosody Engine for Azerbaijani TTS

Generates prosodic annotations (pitch targets, phone durations, pauses)
from a sequence of stressed Word objects:

  - Sentence type detection (declarative, interrogative, exclamatory)
  - Intonation pattern selection (ToBI-inspired)
  - Phone duration prediction (rule-based)
  - Pause insertion at syntactic boundaries
  - SSML and espeak prosody markup generation

Reference:
  Sadekova et al. — PitchFlow: Adding Pitch Control to TTS (Interspeech 2024)
  Cambridge Core — Azerbaijani phonetic description
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from g2p_converter import Word, Phoneme


RULES_PATH = Path(__file__).parent.parent / "Rules" / "prosody_rules.json"


def load_rules() -> dict:
    with open(RULES_PATH, encoding="utf-8") as f:
        return json.load(f)


RULES = load_rules()


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ProsodyAnnotation:
    """Prosodic annotation for a single phone/phoneme."""
    phoneme: str
    duration_ms: float = 80.0
    pitch_target: Optional[float] = None   # Hz; None = interpolated
    pitch_accent: str = ""                 # ToBI label (H*, L+H*, etc.)
    boundary_tone: str = ""               # L%, H%, etc.


@dataclass
class SentenceAnnotation:
    """Full prosodic annotation for a sentence."""
    words: List[Word]
    sentence_type: str = "declarative"
    phone_annotations: List[ProsodyAnnotation] = field(default_factory=list)
    pauses_ms: Dict[int, float] = field(default_factory=dict)
    # pauses_ms: maps word index → pause duration after that word


# ---------------------------------------------------------------------------
# Sentence type detection
# ---------------------------------------------------------------------------

WH_WORDS = set(RULES["sentence_type_detection"]["wh_question_words"])
YN_MARKERS = set(RULES["sentence_type_detection"]["yn_question_markers"])


def detect_sentence_type(words: List[Word]) -> str:
    """
    Classify the sentence type based on surface features.

    Returns one of: 'declarative', 'yn_question', 'wh_question',
                    'exclamatory', 'imperative'
    """
    graphemes = [w.graphemes.lower() for w in words]
    punct = words[-1].graphemes if words else ""

    if punct == "!":
        return "exclamatory"

    if punct == "?":
        # Check for wh-word at start
        if graphemes and graphemes[0] in WH_WORDS:
            return "wh_question"
        # Check for question particle (mi/mı/mu/mü) anywhere
        for g in graphemes:
            if g in {"mi", "mı", "mu", "mü"}:
                return "yn_question"
        return "yn_question"  # Default: yes/no question

    return "declarative"


# ---------------------------------------------------------------------------
# Duration prediction
# ---------------------------------------------------------------------------

BASE_DUR = RULES["duration_rules"]["base_durations_ms"]
POS_MOD  = RULES["duration_rules"]["position_modifiers"]

# Phoneme type classification (IPA)
_STOPS      = set("pbtdkc") | {"ɡ", "ɢ", "tʃ", "dʒ"}
_FRICATIVES = set("fszvʃʒxɣh")
_NASALS     = set("mn") | {"ŋ"}
_LATERALS   = {"l"}
_RHOTICS    = {"r"}
_APPROX     = {"j", "v"}
_AFFRICATES = {"tʃ", "dʒ"}
_VOWELS_IPA = set("aeæɯiooøuyː")


def _phoneme_type(ph: str) -> str:
    if ph in _VOWELS_IPA or ph in {"a", "e", "æ", "ɯ", "i", "o", "ø", "u", "y"}:
        return "vowel"
    if ph in _AFFRICATES:
        return "affricate"
    if ph in _STOPS:
        return "stop"
    if ph in _FRICATIVES:
        return "fricative"
    if ph in _NASALS:
        return "nasal"
    if ph in _LATERALS:
        return "lateral"
    if ph in _RHOTICS:
        return "rhotic"
    if ph in _APPROX:
        return "approximant"
    if ph == "ː":
        return "long_marker"
    return "stop"  # fallback


def predict_duration(phoneme: Phoneme, is_phrase_final: bool,
                     speech_rate: str = "normal") -> float:
    """Predict phone duration in milliseconds using rule-based modifiers."""
    ptype = _phoneme_type(phoneme.symbol)

    if ptype == "long_marker":
        return 0.0  # handled by lengthening the preceding phone

    if ptype == "vowel":
        base = BASE_DUR["short_vowel"]
    elif ptype == "affricate":
        base = BASE_DUR["affricate"]
    elif ptype == "stop":
        base = BASE_DUR["stop_closure"] + BASE_DUR["stop_burst"]
    elif ptype == "fricative":
        base = BASE_DUR["fricative"]
    elif ptype == "nasal":
        base = BASE_DUR["nasal"]
    elif ptype == "lateral":
        base = BASE_DUR["lateral"]
    elif ptype == "rhotic":
        base = BASE_DUR["rhotic"]
    else:
        base = BASE_DUR["approximant"]

    modifier = 1.0
    if ptype == "vowel":
        if phoneme.is_stressed:
            modifier *= POS_MOD["stressed_vowel"]
        else:
            modifier *= POS_MOD["unstressed_vowel"]
        if is_phrase_final:
            modifier *= POS_MOD["phrase_final_vowel"]
    else:
        if is_phrase_final:
            modifier *= POS_MOD["phrase_final_consonant"]

    rate_mod = RULES["duration_rules"]["speech_rate_modifiers"][speech_rate]
    return round(base * modifier * rate_mod, 1)


# ---------------------------------------------------------------------------
# Pitch target generation
# ---------------------------------------------------------------------------

def _get_intonation_pattern(sentence_type: str) -> dict:
    return RULES["intonation_patterns"].get(sentence_type,
           RULES["intonation_patterns"]["declarative"])


def assign_pitch_accents(words: List[Word], sentence_type: str,
                         baseline_hz: float = 150.0) -> List[ProsodyAnnotation]:
    """
    Assign ToBI-style pitch accents to stressed syllables.

    Simple implementation of the Azerbaijani intonation patterns:
      - Declarative: rise on stressed syllable, fall at end
      - YN-question: steady rise toward end
      - WH-question: high fall on wh-word, falling tail
      - Exclamatory: very high peak, sharp fall
    """
    pattern = _get_intonation_pattern(sentence_type)
    pitch_range = {
        "normal": 1.0,
        "wide": 1.4,
        "very_wide": 1.8
    }.get(pattern.get("pitch_range", "normal"), 1.0)

    high_target = baseline_hz * (1 + 0.5 * pitch_range)
    low_target  = baseline_hz * (1 - 0.25 * pitch_range)

    annotations: List[ProsodyAnnotation] = []
    n_words = len(words)

    for w_idx, word in enumerate(words):
        is_last_word = (w_idx == n_words - 1)
        for ph in word.phonemes:
            ann = ProsodyAnnotation(phoneme=ph.symbol)
            if ph.is_vowel:
                if ph.is_stressed:
                    if sentence_type == "declarative":
                        # L+H* on stressed, final fall
                        ann.pitch_accent = "L+H*"
                        ann.pitch_target = (low_target if is_last_word
                                            else high_target)
                    elif sentence_type == "yn_question":
                        ann.pitch_accent = "H*"
                        ann.pitch_target = (high_target * 1.15 if is_last_word
                                            else high_target)
                    elif sentence_type == "wh_question":
                        ann.pitch_accent = "H*" if w_idx == 0 else "L+H*"
                        ann.pitch_target = (high_target * 1.2 if w_idx == 0
                                            else baseline_hz)
                    elif sentence_type == "exclamatory":
                        ann.pitch_accent = "H*"
                        ann.pitch_target = high_target * 1.3
                    else:
                        ann.pitch_accent = "L+H*"
                        ann.pitch_target = high_target
                else:
                    ann.pitch_target = baseline_hz  # unstressed: near baseline

            # Boundary tones on final phoneme of last word
            if is_last_word and ph == word.phonemes[-1]:
                ann.boundary_tone = pattern.get("final_boundary", "L%")

            annotations.append(ann)

    return annotations


# ---------------------------------------------------------------------------
# Pause insertion
# ---------------------------------------------------------------------------

PAUSE_DUR = RULES["pause_rules"]
PUNCT_MAP = {
    ".": PAUSE_DUR["sentence_boundary"],
    "!": PAUSE_DUR["sentence_boundary"],
    "?": PAUSE_DUR["sentence_boundary"],
    ",": PAUSE_DUR["comma"],
    ";": PAUSE_DUR["semicolon"],
    ":": PAUSE_DUR["colon"],
    "—": PAUSE_DUR["dash"],
    "...": PAUSE_DUR["ellipsis"],
}

CONJUNCTION_PAUSE = PAUSE_DUR["between_major_phrases"]


def compute_pauses(words: List[Word]) -> Dict[int, float]:
    """
    Return a mapping {word_index → pause_duration_ms} for pauses
    that should follow each word.
    """
    pauses: Dict[int, float] = {}
    for i, word in enumerate(words):
        g = word.graphemes
        if g in PUNCT_MAP:
            pauses[i] = PUNCT_MAP[g]
        elif g.lower() in {"və", "ya", "amma", "lakin", "ancaq", "çünki"}:
            pauses[i] = CONJUNCTION_PAUSE
    return pauses


# ---------------------------------------------------------------------------
# Main prosody engine
# ---------------------------------------------------------------------------

class ProsodyEngine:
    """
    Generates full prosodic annotation for a list of Word objects.
    """

    def __init__(self, speaking_style: str = "neutral",
                 speaker_gender: str = "male"):
        style = RULES["speaking_styles"].get(speaking_style,
                RULES["speaking_styles"]["neutral"])
        self.speech_rate   = style["speech_rate"]
        self.pause_mult    = style["pause_multiplier"]
        self.pitch_range   = style["pitch_range_semitones"]

        f0_ref = RULES["f0_reference"]
        self.baseline_hz = (f0_ref["male_baseline_hz"]
                            if speaker_gender == "male"
                            else f0_ref["female_baseline_hz"])

    def annotate(self, words: List[Word]) -> SentenceAnnotation:
        """
        Produce a full SentenceAnnotation from a list of Word objects.

        Parameters
        ----------
        words : list of Word (already stress-annotated)

        Returns
        -------
        SentenceAnnotation
        """
        sent_type = detect_sentence_type(words)
        phone_anns = assign_pitch_accents(words, sent_type, self.baseline_hz)

        # Predict durations
        for w_idx, word in enumerate(words):
            is_last = (w_idx == len(words) - 1)
            for ph in word.phonemes:
                for ann in phone_anns:
                    if ann.phoneme == ph.symbol:
                        ann.duration_ms = predict_duration(ph, is_last,
                                                           self.speech_rate)
                        break

        pauses = compute_pauses(words)
        # Apply pause multiplier
        pauses = {k: round(v * self.pause_mult) for k, v in pauses.items()}

        return SentenceAnnotation(
            words=words,
            sentence_type=sent_type,
            phone_annotations=phone_anns,
            pauses_ms=pauses
        )


# ---------------------------------------------------------------------------
# SSML generation
# ---------------------------------------------------------------------------

def to_ssml(annotation: SentenceAnnotation,
            lang: str = "az-AZ") -> str:
    """
    Convert a SentenceAnnotation to a W3C SSML string.

    The SSML output can be consumed by any SSML-compliant TTS engine.
    """
    lines = [f'<speak xml:lang="{lang}">']
    words = annotation.words
    pauses = annotation.pauses_ms

    for w_idx, word in enumerate(words):
        g = word.graphemes
        if g in PUNCT_MAP:
            # Punctuation → silence element
            dur = pauses.get(w_idx, 0)
            if dur > 0:
                lines.append(f'  <break time="{int(dur)}ms"/>')
            continue

        # Phoneme rendering with prosody
        if word.stressed_syllable >= 0:
            lines.append(f'  <w>{g}</w>')
        else:
            lines.append(f'  <w>{g}</w>')

        # Post-word pause
        if w_idx in pauses:
            lines.append(f'  <break time="{int(pauses[w_idx])}ms"/>')

    lines.append('</speak>')
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# espeak-ng markup generation
# ---------------------------------------------------------------------------

def to_espeak_markup(annotation: SentenceAnnotation) -> str:
    """
    Generate espeak-ng compatible text with stress and pause markers.

    espeak-ng notation:
      - '' before syllable = primary stress
      - ,  before syllable = secondary stress
      - _  = short pause (100ms)
      - _500 = pause of 500ms
    """
    parts = []
    words = annotation.words
    pauses = annotation.pauses_ms

    for w_idx, word in enumerate(words):
        g = word.graphemes
        if g in PUNCT_MAP:
            dur = int(pauses.get(w_idx, 200))
            parts.append(f"_{dur}")
            continue

        # Add stress mark before stressed syllable content
        text = g
        parts.append(text)

        if w_idx in pauses:
            dur = int(pauses[w_idx])
            parts.append(f"_{dur}")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# CLI usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    from g2p_converter import AzerbaijaniG2P
    from stress_assigner import StressAssigner

    conv = AzerbaijaniG2P()
    sa   = StressAssigner()
    pe   = ProsodyEngine(speaking_style="neutral", speaker_gender="male")

    samples = [
        "Azərbaycan gözəl ölkədir.",
        "Sən haraya gedirsən?",
        "Bu nə gözəl gündür!",
        "Kitabı oxudunmu?",
    ]

    inputs = sys.argv[1:] if len(sys.argv) > 1 else samples

    for sent in inputs:
        print(f"\nInput: {sent}")
        tokens = re.split(r"(\s+|[,\.!?;:—])", sent)
        words = []
        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            if re.match(r"^[,\.!?;:—]+$", tok):
                words.append(Word(graphemes=tok))
            else:
                w = conv.convert_word(tok)
                sa.assign_word_stress(w)
                words.append(w)

        ann = pe.annotate(words)
        print(f"  Sentence type : {ann.sentence_type}")
        print(f"  Pauses (ms)   : {ann.pauses_ms}")
        print(f"  SSML:\n{to_ssml(ann)}")
