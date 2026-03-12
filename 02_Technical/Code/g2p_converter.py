"""
Grapheme-to-Phoneme (G2P) Converter for Azerbaijani

Converts normalized Azerbaijani Latin-script text to IPA phoneme sequences
using a rule-based approach:
  1. Character-level mapping (graphemes → base phonemes)
  2. Context-sensitive rules (palatalization, ğ allophony, assimilation)
  3. Geminate detection
  4. Syllabification

Reference:
  Salimi, H. — A Generative Phonology of Azerbaijani (University of Florida)
  Cambridge Core — Azerbaijani (Journal of the International Phonetic Association)
"""

import re
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


RULES_PATH = Path(__file__).parent.parent / "Rules" / "g2p_rules.json"


def load_rules() -> dict:
    with open(RULES_PATH, encoding="utf-8") as f:
        return json.load(f)


RULES = load_rules()

# Convenient sets derived from rules
VOWELS      = set(RULES["vowels"].keys())
FRONT_VOWELS = set(RULES["vowel_classes"]["front"])
BACK_VOWELS  = set(RULES["vowel_classes"]["back"])
CONSONANTS  = set(RULES["consonants"].keys())

VOICED_OBSTRUENTS = {"b": "p", "d": "t", "g": "k", "c": "tʃ", "z": "s"}
VELAR_CONSONANTS  = {"k", "q", "g", "ğ"}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Phoneme:
    symbol: str
    grapheme: str = ""
    is_vowel: bool = False
    is_stressed: bool = False
    syllable_index: int = -1


@dataclass
class Word:
    graphemes: str
    phonemes: List[Phoneme] = field(default_factory=list)
    syllables: List[List[Phoneme]] = field(default_factory=list)
    stressed_syllable: int = -1


# ---------------------------------------------------------------------------
# Core conversion
# ---------------------------------------------------------------------------

class AzerbaijaniG2P:
    """Rule-based G2P converter for Azerbaijani (Latin script → IPA)."""

    AZ_ALPHABET = set("abcçdeəfgğhxıijklmnoöpqrsştuvüyz")

    def __init__(self):
        self.vowel_map    = RULES["vowels"]
        self.consonant_map = RULES["consonants"]

    # --- public interface ---------------------------------------------------

    def convert_word(self, word: str) -> Word:
        """Convert a single Azerbaijani word to its phoneme representation."""
        word_lower = word.lower()
        chars = list(word_lower)
        phonemes: List[Phoneme] = []
        i = 0
        while i < len(chars):
            ch = chars[i]
            next_ch  = chars[i + 1] if i + 1 < len(chars) else None
            prev_ch  = chars[i - 1] if i > 0 else None

            # Skip non-Azerbaijani characters (punctuation, etc.)
            if ch not in self.AZ_ALPHABET:
                i += 1
                continue

            phoneme_str = self._map_char(ch, prev_ch, next_ch, chars, i)
            if phoneme_str is None:
                i += 1
                continue

            is_vowel = ch in VOWELS
            phonemes.append(Phoneme(symbol=phoneme_str, grapheme=ch,
                                    is_vowel=is_vowel))
            i += 1

        # Post-processing rules
        phonemes = self._apply_geminate_reduction(phonemes)
        phonemes = self._apply_final_devoicing(phonemes)
        phonemes = self._apply_nasal_assimilation(phonemes)

        result = Word(graphemes=word, phonemes=phonemes)
        result.syllables = self._syllabify(phonemes)
        return result

    def convert_text(self, text: str) -> List[Word]:
        """Convert normalized text (space-separated words) to Word objects."""
        tokens = re.split(r"(\s+|[,\.!?;:—])", text)
        results: List[Word] = []
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if re.match(r"^[,\.!?;:—]+$", token):
                # Punctuation carried as a special marker
                results.append(Word(graphemes=token, phonemes=[
                    Phoneme(symbol=token, grapheme=token)
                ]))
            else:
                results.append(self.convert_word(token))
        return results

    def phonemes_to_string(self, word: Word, separator: str = " ") -> str:
        """Return the phoneme string for a word."""
        return separator.join(p.symbol for p in word.phonemes if p.symbol)

    def ipa_string(self, text: str) -> str:
        """Convenience: convert full text to a flat IPA string."""
        words = self.convert_text(text)
        parts = []
        for w in words:
            ph = self.phonemes_to_string(w, "")
            if ph:
                parts.append(ph)
        return " ".join(parts)

    # --- character mapping --------------------------------------------------

    def _map_char(self, ch: str, prev_ch: Optional[str],
                  next_ch: Optional[str], chars: List[str], i: int) -> Optional[str]:
        """Map a single grapheme to its IPA phoneme (context-aware)."""

        if ch in self.vowel_map:
            return self.vowel_map[ch]

        if ch == "g":
            return self._map_g(next_ch, prev_ch)

        if ch == "k":
            return self._map_k(next_ch, prev_ch)

        if ch == "ğ":
            return self._map_gh(prev_ch, next_ch, i, chars)

        if ch == "n":
            return self._map_n(next_ch)

        if ch in self.consonant_map:
            return self.consonant_map[ch]

        return None  # Unknown character

    def _map_g(self, next_ch: Optional[str], prev_ch: Optional[str]) -> str:
        """g → /c/ before front vowels, /ɡ/ elsewhere."""
        if next_ch in FRONT_VOWELS or prev_ch in FRONT_VOWELS:
            return "c"
        return "ɡ"

    def _map_k(self, next_ch: Optional[str], prev_ch: Optional[str]) -> str:
        """k → /c/ adjacent to front vowels, /k/ elsewhere."""
        if next_ch in FRONT_VOWELS or prev_ch in FRONT_VOWELS:
            return "c"
        return "k"

    def _map_gh(self, prev_ch: Optional[str], next_ch: Optional[str],
                 i: int, chars: List[str]) -> str:
        """
        ğ allophony:
          - Between two vowels → /ɣ/
          - Word-final (or before consonant) → /ː/ (lengthens preceding vowel)
          - Elsewhere → /ɣ/
        """
        prev_is_vowel = prev_ch in VOWELS
        next_is_vowel = next_ch in VOWELS

        if prev_is_vowel and next_is_vowel:
            return "ɣ"

        # Word-final or before consonant: compensatory lengthening marker
        is_final = (next_ch is None) or (next_ch not in self.AZ_ALPHABET)
        if is_final or (next_ch and next_ch not in VOWELS):
            return "ː"

        return "ɣ"

    def _map_n(self, next_ch: Optional[str]) -> str:
        """n → /ŋ/ before velar consonants (k, q, g, ğ), /n/ elsewhere."""
        if next_ch in VELAR_CONSONANTS:
            return "ŋ"
        return "n"

    # --- post-processing rules ----------------------------------------------

    def _apply_geminate_reduction(self, phonemes: List[Phoneme]) -> List[Phoneme]:
        """
        Merge consecutive identical consonant phonemes into one geminate (Cː).
        e.g., /tt/ → /tː/
        """
        if not phonemes:
            return phonemes
        result = [phonemes[0]]
        for ph in phonemes[1:]:
            if (ph.symbol == result[-1].symbol
                    and not ph.is_vowel
                    and ph.symbol not in ("ː",)):
                # Replace last with geminate version
                result[-1] = Phoneme(
                    symbol=result[-1].symbol + "ː",
                    grapheme=result[-1].grapheme + ph.grapheme,
                    is_vowel=False
                )
            else:
                result.append(ph)
        return result

    def _apply_final_devoicing(self, phonemes: List[Phoneme]) -> List[Phoneme]:
        """
        Final obstruent devoicing: voiced stops/fricatives at word boundary
        are devoiced (b→p, d→t, etc.).
        This is optional / lexically governed in Azerbaijani;
        applied here as a default for non-learned loanwords.
        """
        if not phonemes:
            return phonemes
        last = phonemes[-1]
        if last.symbol in VOICED_OBSTRUENTS:
            phonemes[-1] = Phoneme(
                symbol=VOICED_OBSTRUENTS[last.symbol],
                grapheme=last.grapheme,
                is_vowel=False,
                is_stressed=last.is_stressed,
                syllable_index=last.syllable_index
            )
        return phonemes

    def _apply_nasal_assimilation(self, phonemes: List[Phoneme]) -> List[Phoneme]:
        """
        n → m before bilabial stops (b, p) — assimilation at morpheme boundary.
        """
        for i, ph in enumerate(phonemes[:-1]):
            if ph.symbol == "n" and phonemes[i + 1].symbol in ("b", "p"):
                phonemes[i] = Phoneme(
                    symbol="m",
                    grapheme=ph.grapheme,
                    is_vowel=False,
                    is_stressed=ph.is_stressed,
                    syllable_index=ph.syllable_index
                )
        return phonemes

    # --- syllabification ----------------------------------------------------

    def _syllabify(self, phonemes: List[Phoneme]) -> List[List[Phoneme]]:
        """
        Divide phonemes into syllables.
        Algorithm: onset-maximization principle.
          - Each syllable has exactly one vowel nucleus.
          - Consonants are preferentially assigned to the onset of the next syllable.
        """
        if not phonemes:
            return []

        # Find vowel positions
        vowel_indices = [i for i, ph in enumerate(phonemes) if ph.is_vowel]
        if not vowel_indices:
            return [phonemes]  # No vowels — single syllable chunk

        syllables: List[List[Phoneme]] = []
        prev_boundary = 0

        for v_idx, v_pos in enumerate(vowel_indices):
            if v_idx == len(vowel_indices) - 1:
                # Last vowel: take all remaining phonemes
                syllables.append(phonemes[prev_boundary:])
            else:
                next_v = vowel_indices[v_idx + 1]
                between = phonemes[v_pos + 1:next_v]
                n_between = len(between)

                if n_between == 0:
                    # Two adjacent vowels — hiatus; split immediately
                    syllables.append(phonemes[prev_boundary:v_pos + 1])
                    prev_boundary = v_pos + 1
                elif n_between == 1:
                    # Single consonant → onset of next syllable
                    syllables.append(phonemes[prev_boundary:v_pos + 1])
                    prev_boundary = v_pos + 1
                else:
                    # Multiple consonants → last one is onset, rest are coda
                    split = v_pos + n_between  # all but last go to coda
                    syllables.append(phonemes[prev_boundary:split])
                    prev_boundary = split

        # Annotate syllable indices
        for s_idx, syl in enumerate(syllables):
            for ph in syl:
                ph.syllable_index = s_idx

        return syllables


# ---------------------------------------------------------------------------
# Module-level convenience functions
# ---------------------------------------------------------------------------

_converter = None


def get_converter() -> AzerbaijaniG2P:
    global _converter
    if _converter is None:
        _converter = AzerbaijaniG2P()
    return _converter


def word_to_ipa(word: str) -> str:
    """Convert a single Azerbaijani word to an IPA string."""
    conv = get_converter()
    w = conv.convert_word(word)
    return conv.phonemes_to_string(w, "")


def text_to_ipa(text: str) -> str:
    """Convert normalized Azerbaijani text to a flat IPA string."""
    return get_converter().ipa_string(text)


def text_to_words(text: str) -> List[Word]:
    """Convert normalized text to a list of Word objects (with phonemes)."""
    return get_converter().convert_text(text)


# ---------------------------------------------------------------------------
# CLI usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    samples = [
        ("alma",       "apple"),
        ("kitab",      "book"),
        ("məktəb",     "school"),
        ("gəl",        "come"),
        ("dağ",        "mountain"),
        ("Azərbaycan", "Azerbaijan"),
        ("torpaq",     "land/soil"),
        ("getmək",     "to go"),
        ("oxumaq",     "to read"),
        ("müəllim",    "teacher"),
        ("gözəl",      "beautiful"),
        ("şəhər",      "city"),
    ]

    inputs = sys.argv[1:] if len(sys.argv) > 1 else [w for w, _ in samples]

    conv = AzerbaijaniG2P()
    for word in inputs:
        w = conv.convert_word(word)
        ipa = conv.phonemes_to_string(w, "")
        syllables = [conv.phonemes_to_string(
            Word(graphemes="", phonemes=syl), "") for syl in w.syllables]
        print(f"{word:15} → /{ipa}/  syllables: {syllables}")
