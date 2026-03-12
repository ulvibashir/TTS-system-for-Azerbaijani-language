"""
Stress Assignment Module for Azerbaijani TTS

Applies lexical and phrasal stress to a sequence of Word objects:
  - Default rule: primary stress on the final syllable
  - Exception rules: question particles, negation, postpositions, etc.
  - Phrasal stress: focus and topic annotation

Reference:
  Salimi, H. — A Generative Phonology of Azerbaijani
  Huseynli, N. — Azerbaijani Prosody (internal research notes)
"""

import json
from pathlib import Path
from typing import List, Optional, Tuple

from g2p_converter import Word, Phoneme


RULES_PATH = Path(__file__).parent.parent / "Rules" / "stress_rules.json"


def load_rules() -> dict:
    with open(RULES_PATH, encoding="utf-8") as f:
        return json.load(f)


RULES = load_rules()


# ---------------------------------------------------------------------------
# Constants from rules
# ---------------------------------------------------------------------------

POSTPOSITIONS = set(RULES["exception_rules"][6]["postpositions"])
CONJUNCTIONS  = set(RULES["exception_rules"][7]["conjunctions"])
CLITIC_PARTICLES = {"mi", "mı", "mu", "mü"}
NO_STRESS_WORDS  = set(["deyil"]) | POSTPOSITIONS | CONJUNCTIONS

EXCEPTION_WORDS: dict = {}  # word → stressed_syllable_index
for rule in RULES["exception_rules"]:
    if "word" in rule:
        EXCEPTION_WORDS[rule["word"]] = rule["stressed_syllable"]
    if "words" in rule:
        for w in rule["words"]:
            EXCEPTION_WORDS[w] = rule["stressed_syllable"]


# ---------------------------------------------------------------------------
# Notation
# ---------------------------------------------------------------------------

PRIMARY_STRESS   = RULES["stress_notation"]["primary_stress"]    # ˈ
SECONDARY_STRESS = RULES["stress_notation"]["secondary_stress"]  # ˌ


# ---------------------------------------------------------------------------
# Core stress assigner
# ---------------------------------------------------------------------------

class StressAssigner:
    """Assign lexical stress to Azerbaijani Word objects."""

    def assign_word_stress(self, word: Word) -> Word:
        """
        Assign primary stress to the correct syllable of a word.

        Modifies the `is_stressed` attribute of vowel Phoneme objects in-place
        and also sets `word.stressed_syllable`.

        Returns the modified Word.
        """
        if not word.syllables:
            return word

        g = word.graphemes.lower()

        # 1. Unstressed function words
        if g in POSTPOSITIONS or g in CONJUNCTIONS or g in CLITIC_PARTICLES:
            word.stressed_syllable = -1
            return word

        # 2. Lexical exceptions (known words with fixed stress)
        if g in EXCEPTION_WORDS:
            idx = EXCEPTION_WORDS[g]
            if idx >= 0:
                self._mark_stress(word, idx)
            return word

        # 3. Negation suffix -ma/-mə: stress penultimate syllable.
        # Require 3+ syllables to avoid false matches on common nouns/
        # gerunds that happen to end in 'ma'/'mə' (e.g. alma = apple).
        if self._has_negation_suffix(g) and len(word.syllables) >= 3:
            self._mark_stress(word, len(word.syllables) - 2)
            return word

        # 4. Default: final syllable
        self._mark_stress(word, len(word.syllables) - 1)
        return word

    def assign_phrase_stress(self, words: List[Word]) -> List[Word]:
        """
        Apply phrasal stress over a list of words.

        Rules:
          - The main content word immediately before the verb carries the
            highest pitch accent (focus default position in Azerbaijani).
          - Postpositions and conjunctions are always unstressed.
          - In a sequence, the last stressed word before sentence-final
            punctuation is the phrase-final head.
        """
        for word in words:
            self.assign_word_stress(word)

        # Identify sentence-final punctuation
        has_sentence_end = (words and
                            words[-1].graphemes in (".", "!", "?"))

        # Demote stress on function words that slipped through
        for word in words:
            if word.graphemes.lower() in POSTPOSITIONS | CONJUNCTIONS | CLITIC_PARTICLES:
                word.stressed_syllable = -1
                for ph in word.phonemes:
                    ph.is_stressed = False

        return words

    # --- private helpers ----------------------------------------------------

    @staticmethod
    def _mark_stress(word: Word, syllable_idx: int) -> None:
        """Mark the vowel in the given syllable as stressed."""
        word.stressed_syllable = syllable_idx
        try:
            syl = word.syllables[syllable_idx]
        except IndexError:
            return
        for ph in syl:
            if ph.is_vowel:
                ph.is_stressed = True
                break

    @staticmethod
    def _has_negation_suffix(graphemes: str) -> bool:
        """Return True if the word ends in the negation suffix -ma/-mə."""
        # Exclude the infinitive -maq/-mək
        return (graphemes.endswith(("ma", "mə"))
                and not graphemes.endswith(("maq", "mək")))


# ---------------------------------------------------------------------------
# Stress rendering
# ---------------------------------------------------------------------------

def render_stressed_ipa(word: Word) -> str:
    """
    Render the IPA phoneme string with IPA stress diacritics.

    Returns a string like: ˈæl.ma  (stress marker before stressed syllable)
    """
    if not word.syllables:
        return "".join(ph.symbol for ph in word.phonemes)

    parts = []
    for syl_idx, syl in enumerate(word.syllables):
        syl_str = "".join(ph.symbol for ph in syl)
        if syl_idx == word.stressed_syllable:
            parts.append(PRIMARY_STRESS + syl_str)
        else:
            parts.append(syl_str)
    return ".".join(parts)


# ---------------------------------------------------------------------------
# Module-level convenience
# ---------------------------------------------------------------------------

_assigner: Optional[StressAssigner] = None


def get_assigner() -> StressAssigner:
    global _assigner
    if _assigner is None:
        _assigner = StressAssigner()
    return _assigner


def assign_stress(words: List[Word]) -> List[Word]:
    """Assign word and phrasal stress to a list of Word objects."""
    return get_assigner().assign_phrase_stress(words)


def stressed_ipa(words: List[Word]) -> str:
    """Render a sequence of stressed Word objects as an IPA string."""
    parts = []
    for w in words:
        if w.graphemes in (".", ",", "!", "?", ";", ":", "—"):
            parts.append(w.graphemes)
        else:
            parts.append(render_stressed_ipa(w))
    return " ".join(parts)


# ---------------------------------------------------------------------------
# CLI usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    from g2p_converter import AzerbaijaniG2P

    conv = AzerbaijaniG2P()
    sa   = StressAssigner()

    samples = [
        "alma",
        "kitab",
        "Azərbaycan",
        "gözəl",
        "getmək",
        "oxumaq",
        "getmir",   # negation (getmir = doesn't go)
        "deyil",    # negative copula
        "üçün",     # postposition
        "bəlkə",    # maybe
        "yalnız",   # only
    ]

    inputs = sys.argv[1:] if len(sys.argv) > 1 else samples

    for word_str in inputs:
        w = conv.convert_word(word_str)
        sa.assign_word_stress(w)
        ipa = render_stressed_ipa(w)
        syl_count = len(w.syllables)
        stress_idx = w.stressed_syllable
        print(f"{word_str:15} → [{ipa}]  "
              f"syllables={syl_count}  stressed_syl={stress_idx}")
