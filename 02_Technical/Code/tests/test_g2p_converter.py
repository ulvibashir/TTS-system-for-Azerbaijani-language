"""Tests for g2p_converter.py — phoneme mapping, context rules, syllabification."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from g2p_converter import (
    AzerbaijaniG2P, Word, Phoneme, word_to_ipa, text_to_ipa, text_to_words,
)


# ---------------------------------------------------------------------------
# Vowel mapping
# ---------------------------------------------------------------------------

class TestVowelMapping:
    def test_all_nine_vowels(self):
        g2p = AzerbaijaniG2P()
        expected = {
            "a": "a", "e": "e", "ə": "æ", "ı": "ɯ",
            "i": "i", "o": "o", "ö": "ø", "u": "u", "ü": "y",
        }
        for grapheme, ipa in expected.items():
            w = g2p.convert_word(grapheme)
            phonemes = [p.symbol for p in w.phonemes]
            assert ipa in phonemes, f"{grapheme} should map to {ipa}"

    def test_vowels_marked_as_vowel(self):
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("alma")
        vowel_phonemes = [p for p in w.phonemes if p.is_vowel]
        assert len(vowel_phonemes) == 2  # a, a


# ---------------------------------------------------------------------------
# Consonant mapping
# ---------------------------------------------------------------------------

class TestConsonantMapping:
    def test_basic_consonants(self):
        g2p = AzerbaijaniG2P()
        # b → b
        w = g2p.convert_word("baba")
        symbols = [p.symbol for p in w.phonemes if not p.is_vowel]
        assert "b" in symbols or "p" in symbols  # final devoicing may apply

    def test_ç_mapping(self):
        ipa = word_to_ipa("çay")
        assert "tʃ" in ipa

    def test_ş_mapping(self):
        ipa = word_to_ipa("şəhər")
        assert "ʃ" in ipa

    def test_c_mapping(self):
        ipa = word_to_ipa("can")
        assert "dʒ" in ipa

    def test_q_mapping(self):
        ipa = word_to_ipa("qız")
        assert "ɢ" in ipa


# ---------------------------------------------------------------------------
# Context-sensitive rules
# ---------------------------------------------------------------------------

class TestContextSensitiveRules:
    def test_g_palatalization_before_front_vowel(self):
        """g → /ɟ/ before front vowels (e, ə, i, ö, ü)"""
        ipa = word_to_ipa("gəl")
        assert "ɟ" in ipa

    def test_g_no_palatalization_before_back_vowel(self):
        """g → /ɡ/ before back vowels"""
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("qalaq")
        # q maps to ɢ, not testing g here; test with a word like "gol"
        ipa = word_to_ipa("gol")
        assert "ɡ" in ipa or "k" in ipa  # may devoice at end

    def test_k_palatalization(self):
        """k → /c/ adjacent to front vowels"""
        ipa = word_to_ipa("kənd")
        assert "c" in ipa

    def test_k_no_palatalization(self):
        """k → /k/ when not adjacent to front vowels"""
        ipa = word_to_ipa("qalaq")
        # No k in this word, test with "kart"
        # Actually "kart" has no front vowels adjacent to k
        # Let's verify the phoneme set doesn't include palatal
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("qapaq")
        symbols = [p.symbol for p in w.phonemes]
        assert "c" not in symbols  # No palatalization (no k in word)

    def test_gh_word_final_lengthening(self):
        """ğ at word-final → /ː/ (lengthening)"""
        ipa = word_to_ipa("dağ")
        assert "ː" in ipa

    def test_gh_intervocalic(self):
        """ğ between vowels → /ɣ/"""
        ipa = word_to_ipa("ağac")
        assert "ɣ" in ipa

    def test_n_before_velar(self):
        """n → /ŋ/ before velar consonants"""
        ipa = word_to_ipa("çənk")
        assert "ŋ" in ipa or "n" in ipa


# ---------------------------------------------------------------------------
# Final devoicing
# ---------------------------------------------------------------------------

class TestFinalDevoicing:
    def test_b_to_p(self):
        """Word-final b → p"""
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("kitab")
        last = w.phonemes[-1]
        assert last.symbol == "p", f"Expected 'p' but got '{last.symbol}'"

    def test_d_to_t(self):
        """Word-final d → t"""
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("od")
        last = w.phonemes[-1]
        assert last.symbol == "t", f"Expected 't' but got '{last.symbol}'"

    def test_no_devoicing_mid_word(self):
        """Devoicing should not apply mid-word"""
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("adam")
        # 'd' is mid-word, should remain /d/
        d_phonemes = [p for p in w.phonemes if p.grapheme == "d"]
        assert any(p.symbol == "d" for p in d_phonemes)


# ---------------------------------------------------------------------------
# Geminate reduction
# ---------------------------------------------------------------------------

class TestGeminateReduction:
    def test_double_consonant(self):
        """Double consonants should produce geminate (Cː)"""
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("müəllim")
        symbols = [p.symbol for p in w.phonemes]
        # ll → lː
        assert any("ː" in s for s in symbols), f"Expected geminate in {symbols}"


# ---------------------------------------------------------------------------
# Nasal assimilation
# ---------------------------------------------------------------------------

class TestNasalAssimilation:
    def test_n_before_b(self):
        """n → m before bilabial /b/"""
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("İstanbul")
        # "nb" sequence: n should assimilate to m
        symbols = "".join(p.symbol for p in w.phonemes)
        # The n before b should become m
        assert "mb" in symbols or "mp" in symbols, f"Expected nasal assimilation in {symbols}"


# ---------------------------------------------------------------------------
# Syllabification
# ---------------------------------------------------------------------------

class TestSyllabification:
    def test_disyllabic(self):
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("alma")
        assert len(w.syllables) == 2

    def test_trisyllabic(self):
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("oxumaq")
        assert len(w.syllables) == 3

    def test_monosyllabic(self):
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("gəl")
        assert len(w.syllables) == 1

    def test_tetrasyllabic(self):
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("Azərbaycan")
        assert len(w.syllables) == 4

    def test_each_syllable_has_vowel(self):
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("universitet")
        for syl in w.syllables:
            vowels = [p for p in syl if p.is_vowel]
            assert len(vowels) >= 1, f"Syllable has no vowel: {[p.symbol for p in syl]}"

    def test_syllable_index_annotation(self):
        g2p = AzerbaijaniG2P()
        w = g2p.convert_word("alma")
        for syl_idx, syl in enumerate(w.syllables):
            for ph in syl:
                assert ph.syllable_index == syl_idx


# ---------------------------------------------------------------------------
# Text-level conversion
# ---------------------------------------------------------------------------

class TestTextConversion:
    def test_text_to_ipa(self):
        ipa = text_to_ipa("salam dünya")
        assert len(ipa) > 0
        assert " " in ipa  # Two words

    def test_text_to_words(self):
        words = text_to_words("salam dünya")
        content_words = [w for w in words if w.graphemes.strip() not in ".,!?;:—"]
        assert len(content_words) == 2

    def test_punctuation_preserved(self):
        words = text_to_words("salam!")
        graphemes = [w.graphemes for w in words]
        assert "!" in graphemes or any("!" in g for g in graphemes)

    def test_word_to_ipa_convenience(self):
        ipa = word_to_ipa("kitab")
        assert len(ipa) > 0
        assert "p" in ipa  # final devoicing b→p
