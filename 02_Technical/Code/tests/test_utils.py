"""Tests for utils.py — character sets, vowel harmony, tokenization, metrics."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import (
    is_vowel, is_consonant, count_syllables, last_vowel,
    vowel_harmony_class, tokenize, split_sentences,
    compute_mean_mos, character_error_rate, word_error_rate,
)


# ---------------------------------------------------------------------------
# Character classification
# ---------------------------------------------------------------------------

class TestCharacterSets:
    def test_azerbaijani_vowels(self):
        for v in "aeəıioöuü":
            assert is_vowel(v), f"{v} should be a vowel"

    def test_uppercase_vowels(self):
        # Note: İ (U+0130, capital dotted I) is Azerbaijani-specific and
        # is_vowel uses .lower() which maps it correctly in most locales.
        # Standard ASCII uppercase vowels that map cleanly:
        for v in "AEIOÖUÜ":
            assert is_vowel(v), f"{v} should be a vowel (uppercase)"

    def test_consonants(self):
        for c in "bcçdfgğhxjklmnpqrsştvyz":
            assert is_consonant(c), f"{c} should be a consonant"

    def test_non_azerbaijani_chars(self):
        assert not is_vowel("w")
        assert not is_consonant("w")
        assert not is_vowel("1")


# ---------------------------------------------------------------------------
# Syllable counting
# ---------------------------------------------------------------------------

class TestSyllableCounting:
    def test_monosyllabic(self):
        assert count_syllables("gəl") == 1

    def test_disyllabic(self):
        assert count_syllables("alma") == 2

    def test_trisyllabic(self):
        assert count_syllables("oxumaq") == 3

    def test_tetrasyllabic(self):
        assert count_syllables("Azərbaycan") == 4

    def test_no_vowels(self):
        assert count_syllables("brk") == 0

    def test_empty(self):
        assert count_syllables("") == 0


# ---------------------------------------------------------------------------
# Vowel harmony
# ---------------------------------------------------------------------------

class TestVowelHarmony:
    def test_back_unrounded(self):
        assert vowel_harmony_class("alma") == "back_unrounded"
        assert vowel_harmony_class("qız") == "back_unrounded"

    def test_back_rounded(self):
        assert vowel_harmony_class("qoyun") == "back_rounded"
        assert vowel_harmony_class("torpaq") == "back_unrounded"

    def test_front_unrounded(self):
        assert vowel_harmony_class("gəl") == "front_unrounded"
        assert vowel_harmony_class("kitab") == "back_unrounded"

    def test_front_rounded(self):
        assert vowel_harmony_class("gözlük") == "front_rounded"
        assert vowel_harmony_class("ölkə") == "front_unrounded"

    def test_unknown(self):
        assert vowel_harmony_class("brk") == "unknown"

    def test_last_vowel(self):
        assert last_vowel("alma") == "a"
        assert last_vowel("gözəl") == "ə"
        assert last_vowel("kitab") == "a"
        assert last_vowel("brk") is None


# ---------------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------------

class TestTokenization:
    def test_simple_sentence(self):
        tokens = tokenize("Salam dünya!")
        assert "Salam" in tokens
        assert "dünya" in tokens
        assert "!" in tokens

    def test_azerbaijani_chars(self):
        tokens = tokenize("Gözəl ölkədir.")
        assert "Gözəl" in tokens
        assert "ölkədir" in tokens

    def test_punctuation_separation(self):
        tokens = tokenize("Gəl, gedək.")
        assert "," in tokens
        assert "." in tokens

    def test_split_sentences(self):
        text = "Birinci cümlə. İkinci cümlə! Üçüncü cümlə?"
        sents = split_sentences(text)
        assert len(sents) == 3


# ---------------------------------------------------------------------------
# Evaluation metrics
# ---------------------------------------------------------------------------

class TestMetrics:
    def test_mean_mos_basic(self):
        mean, std = compute_mean_mos([3.0, 3.0, 3.0])
        assert mean == 3.0
        assert std == 0.0

    def test_mean_mos_varied(self):
        mean, std = compute_mean_mos([1.0, 2.0, 3.0, 4.0, 5.0])
        assert mean == 3.0
        assert std > 0

    def test_mean_mos_empty(self):
        mean, std = compute_mean_mos([])
        assert mean == 0.0
        assert std == 0.0

    def test_cer_identical(self):
        assert character_error_rate("salam", "salam") == 0.0

    def test_cer_different(self):
        cer = character_error_rate("salam", "salom")
        assert 0 < cer < 1

    def test_cer_empty_reference(self):
        assert character_error_rate("", "test") == 0.0

    def test_wer_identical(self):
        assert word_error_rate("bu bir test", "bu bir test") == 0.0

    def test_wer_different(self):
        wer = word_error_rate("bu bir test", "bu iki test")
        assert 0 < wer < 1

    def test_wer_empty_reference(self):
        assert word_error_rate("", "test") == 0.0
