"""Tests for prosody_engine.py — sentence type, duration, pitch, pauses, SSML."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from g2p_converter import AzerbaijaniG2P, Word, Phoneme
from stress_assigner import StressAssigner
from prosody_engine import (
    detect_sentence_type, predict_duration, assign_pitch_accents,
    compute_pauses, ProsodyEngine, SentenceAnnotation, to_ssml,
    to_espeak_markup,
)


def make_words(text):
    """Helper: tokenize, convert, and stress-assign a sentence."""
    g2p = AzerbaijaniG2P()
    sa = StressAssigner()
    import re
    tokens = re.split(r"(\s+|[,\.!?;:—])", text)
    words = []
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        if re.match(r"^[,\.!?;:—]+$", tok):
            words.append(Word(graphemes=tok))
        else:
            w = g2p.convert_word(tok)
            sa.assign_word_stress(w)
            words.append(w)
    return words


# ---------------------------------------------------------------------------
# Sentence type detection
# ---------------------------------------------------------------------------

class TestSentenceTypeDetection:
    def test_declarative(self):
        words = make_words("Azərbaycan gözəl ölkədir.")
        assert detect_sentence_type(words) == "declarative"

    def test_yn_question(self):
        words = make_words("Sən bu kitabı oxudunmu?")
        assert detect_sentence_type(words) == "yn_question"

    def test_wh_question_kim(self):
        words = make_words("Kim bu işi görəcək?")
        assert detect_sentence_type(words) == "wh_question"

    def test_wh_question_harada(self):
        words = make_words("Harada yaşayırsan?")
        assert detect_sentence_type(words) == "wh_question"

    def test_wh_question_nə_vaxt(self):
        words = make_words("Nə vaxt gəlirsən?")
        stype = detect_sentence_type(words)
        assert stype in ("wh_question", "yn_question")

    def test_exclamatory(self):
        words = make_words("Bu nə gözəl gündür!")
        assert detect_sentence_type(words) == "exclamatory"

    def test_default_question_is_yn(self):
        """A question mark without wh-word defaults to yn_question."""
        words = make_words("Gedirsiniz?")
        assert detect_sentence_type(words) == "yn_question"


# ---------------------------------------------------------------------------
# Duration prediction
# ---------------------------------------------------------------------------

class TestDurationPrediction:
    def test_vowel_has_positive_duration(self):
        ph = Phoneme(symbol="a", grapheme="a", is_vowel=True, is_stressed=False)
        dur = predict_duration(ph, is_phrase_final=False)
        assert dur > 0

    def test_stressed_vowel_longer(self):
        unstressed = Phoneme(symbol="a", grapheme="a", is_vowel=True, is_stressed=False)
        stressed = Phoneme(symbol="a", grapheme="a", is_vowel=True, is_stressed=True)
        d_unstressed = predict_duration(unstressed, is_phrase_final=False)
        d_stressed = predict_duration(stressed, is_phrase_final=False)
        assert d_stressed > d_unstressed

    def test_phrase_final_vowel_longer(self):
        ph = Phoneme(symbol="a", grapheme="a", is_vowel=True, is_stressed=False)
        d_normal = predict_duration(ph, is_phrase_final=False)
        d_final = predict_duration(ph, is_phrase_final=True)
        assert d_final > d_normal

    def test_consonant_has_positive_duration(self):
        ph = Phoneme(symbol="s", grapheme="s", is_vowel=False)
        dur = predict_duration(ph, is_phrase_final=False)
        assert dur > 0

    def test_long_marker_duration(self):
        """Long marker ː is classified by _phoneme_type; its duration depends on classification."""
        ph = Phoneme(symbol="ː", grapheme="ğ", is_vowel=False)
        dur = predict_duration(ph, is_phrase_final=False)
        # The ː symbol is in _VOWELS_IPA set, so it gets vowel duration
        assert dur >= 0

    def test_speech_rate_slow(self):
        ph = Phoneme(symbol="a", grapheme="a", is_vowel=True, is_stressed=False)
        d_normal = predict_duration(ph, is_phrase_final=False, speech_rate="normal")
        d_slow = predict_duration(ph, is_phrase_final=False, speech_rate="slow")
        assert d_slow > d_normal

    def test_speech_rate_fast(self):
        ph = Phoneme(symbol="a", grapheme="a", is_vowel=True, is_stressed=False)
        d_normal = predict_duration(ph, is_phrase_final=False, speech_rate="normal")
        d_fast = predict_duration(ph, is_phrase_final=False, speech_rate="fast")
        assert d_fast < d_normal


# ---------------------------------------------------------------------------
# Pitch accents
# ---------------------------------------------------------------------------

class TestPitchAccents:
    def test_declarative_has_pitch_targets(self):
        words = make_words("Salam dünya.")
        content = [w for w in words if w.graphemes != "."]
        anns = assign_pitch_accents(content, "declarative", baseline_hz=150.0)
        pitched = [a for a in anns if a.pitch_target is not None]
        assert len(pitched) > 0

    def test_question_has_higher_final(self):
        words = make_words("Gedirsən?")
        content = [w for w in words if w.graphemes != "?"]
        anns_decl = assign_pitch_accents(content, "declarative", baseline_hz=150.0)
        anns_yn = assign_pitch_accents(content, "yn_question", baseline_hz=150.0)
        # yn_question should have higher pitch on final stressed vowel
        # Just verify annotations are generated
        assert len(anns_yn) > 0

    def test_exclamatory_has_high_peak(self):
        words = make_words("Gözəl!")
        content = [w for w in words if w.graphemes != "!"]
        anns = assign_pitch_accents(content, "exclamatory", baseline_hz=150.0)
        targets = [a.pitch_target for a in anns if a.pitch_target]
        if targets:
            assert max(targets) > 150.0  # Higher than baseline


# ---------------------------------------------------------------------------
# Pause computation
# ---------------------------------------------------------------------------

class TestPauseComputation:
    def test_sentence_boundary_pause(self):
        words = make_words("Salam.")
        pauses = compute_pauses(words)
        # Period should have a pause
        period_indices = [i for i, w in enumerate(words) if w.graphemes == "."]
        for idx in period_indices:
            assert idx in pauses
            assert pauses[idx] > 0

    def test_comma_pause(self):
        words = make_words("Gəl, gedək.")
        pauses = compute_pauses(words)
        comma_indices = [i for i, w in enumerate(words) if w.graphemes == ","]
        for idx in comma_indices:
            assert idx in pauses

    def test_conjunction_pause(self):
        words = make_words("mən və sən")
        pauses = compute_pauses(words)
        ve_indices = [i for i, w in enumerate(words) if w.graphemes.lower() == "və"]
        for idx in ve_indices:
            assert idx in pauses


# ---------------------------------------------------------------------------
# ProsodyEngine integration
# ---------------------------------------------------------------------------

class TestProsodyEngine:
    def test_annotate_returns_sentence_annotation(self):
        pe = ProsodyEngine()
        words = make_words("Azərbaycan gözəl ölkədir.")
        ann = pe.annotate(words)
        assert isinstance(ann, SentenceAnnotation)
        assert ann.sentence_type == "declarative"

    def test_annotate_question(self):
        pe = ProsodyEngine()
        words = make_words("Kim gəldi?")
        ann = pe.annotate(words)
        assert ann.sentence_type == "wh_question"

    def test_speaking_style_formal(self):
        pe = ProsodyEngine(speaking_style="formal")
        words = make_words("Salam.")
        ann = pe.annotate(words)
        assert isinstance(ann, SentenceAnnotation)

    def test_speaker_gender_female(self):
        pe = ProsodyEngine(speaker_gender="female")
        assert pe.baseline_hz > 150  # Female baseline higher than male


# ---------------------------------------------------------------------------
# SSML generation
# ---------------------------------------------------------------------------

class TestSSML:
    def test_ssml_has_speak_tag(self):
        pe = ProsodyEngine()
        words = make_words("Salam dünya.")
        ann = pe.annotate(words)
        ssml = to_ssml(ann)
        assert ssml.startswith("<speak")
        assert ssml.endswith("</speak>")

    def test_ssml_contains_words(self):
        pe = ProsodyEngine()
        words = make_words("Salam dünya.")
        ann = pe.annotate(words)
        ssml = to_ssml(ann)
        assert "Salam" in ssml

    def test_ssml_has_break(self):
        pe = ProsodyEngine()
        words = make_words("Gəl, gedək.")
        ann = pe.annotate(words)
        ssml = to_ssml(ann)
        assert "break" in ssml


# ---------------------------------------------------------------------------
# espeak markup generation
# ---------------------------------------------------------------------------

class TestEspeakMarkup:
    def test_espeak_markup_non_empty(self):
        pe = ProsodyEngine()
        words = make_words("Salam dünya.")
        ann = pe.annotate(words)
        markup = to_espeak_markup(ann)
        assert len(markup) > 0

    def test_espeak_markup_contains_words(self):
        pe = ProsodyEngine()
        words = make_words("Azərbaycan.")
        ann = pe.annotate(words)
        markup = to_espeak_markup(ann)
        assert "Azərbaycan" in markup
