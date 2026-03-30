"""Tests for stress_assigner.py — word stress, exceptions, phrasal stress."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from g2p_converter import AzerbaijaniG2P
from stress_assigner import (
    StressAssigner, render_stressed_ipa, assign_stress, stressed_ipa,
)


def make_word(g2p, sa, text):
    """Helper: convert and stress-assign a word."""
    w = g2p.convert_word(text)
    sa.assign_word_stress(w)
    return w


# ---------------------------------------------------------------------------
# Default stress rule (final syllable)
# ---------------------------------------------------------------------------

class TestDefaultStress:
    def test_disyllabic_final_stress(self):
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "alma")
        # Default: final syllable (index 1 for 2-syllable word)
        assert w.stressed_syllable == len(w.syllables) - 1

    def test_trisyllabic_final_stress(self):
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "oxumaq")
        assert w.stressed_syllable == len(w.syllables) - 1

    def test_monosyllabic_stress(self):
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "gəl")
        assert w.stressed_syllable == 0

    def test_stressed_vowel_marked(self):
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "kitab")
        stressed_syl = w.syllables[w.stressed_syllable]
        stressed_vowels = [p for p in stressed_syl if p.is_vowel and p.is_stressed]
        assert len(stressed_vowels) >= 1


# ---------------------------------------------------------------------------
# Exception rules
# ---------------------------------------------------------------------------

class TestStressExceptions:
    def test_deyil_first_syllable(self):
        """Negative copula 'deyil' → stress on first syllable."""
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "deyil")
        assert w.stressed_syllable == 0

    def test_bəlkə_first_syllable(self):
        """Adverb 'bəlkə' → stress on first syllable."""
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "bəlkə")
        assert w.stressed_syllable == 0

    def test_yalnız_first_syllable(self):
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "yalnız")
        assert w.stressed_syllable == 0

    def test_postposition_unstressed(self):
        """Postpositions like 'üçün' should be unstressed."""
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "üçün")
        assert w.stressed_syllable == -1

    def test_conjunction_unstressed(self):
        """Conjunctions like 'və' should be unstressed."""
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "və")
        assert w.stressed_syllable == -1

    def test_conjunction_amma_unstressed(self):
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "amma")
        assert w.stressed_syllable == -1

    def test_negation_stress_shift(self):
        """Negation suffix -ma/-mə shifts stress to penultimate (3+ syllables)."""
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        # "yazmadı" = 3 syllables, ends in -ma (before -dı)
        # Actually, "yazmadı" doesn't end in -ma. Let's use "yazma" if 3+ syl
        # Better: "oxumadı" (4 syllables: o-xu-ma-dı) — doesn't end in ma/mə
        # The rule checks if graphemes end in ma/mə. "getmə" = 2 syl, needs 3+
        # Let's use "almadı" — but this doesn't end in ma either (ends in dı)
        # The _has_negation_suffix checks endswith("ma"/"mə"), so "oxuma" works
        # But not "oxumadı" since it ends in "dı"
        # Actually let's check the real negation words that end in ma:
        # "yazma" (don't write) = 2 syllables, needs 3+
        # "oxutma" (don't have read) = 3 syllables
        w = make_word(g2p, sa, "oxutma")
        if len(w.syllables) >= 3:
            assert w.stressed_syllable == len(w.syllables) - 2


# ---------------------------------------------------------------------------
# Phrasal stress
# ---------------------------------------------------------------------------

class TestPhrasalStress:
    def test_phrase_stress_assignment(self):
        g2p = AzerbaijaniG2P()
        words = g2p.convert_text("kitab oxudum")
        words = assign_stress(words)
        # All content words should have stress assigned
        for w in words:
            if w.graphemes not in (".", ",", "!", "?", ";", ":", "—"):
                assert w.stressed_syllable >= 0 or w.graphemes.lower() in {
                    "və", "ya", "amma", "lakin", "ancaq", "çünki", "ki",
                    "nə", "həm", "üçün", "ilə", "kimi", "qədər", "haqqında",
                    "qarşı", "görə", "sonra", "əvvəl", "yanında",
                    "mi", "mı", "mu", "mü",
                }

    def test_postposition_demoted_in_phrase(self):
        g2p = AzerbaijaniG2P()
        words = g2p.convert_text("məktəb üçün")
        words = assign_stress(words)
        ucun = [w for w in words if w.graphemes.lower() == "üçün"]
        if ucun:
            assert ucun[0].stressed_syllable == -1


# ---------------------------------------------------------------------------
# Stress rendering
# ---------------------------------------------------------------------------

class TestStressRendering:
    def test_render_stressed_ipa(self):
        g2p = AzerbaijaniG2P()
        sa = StressAssigner()
        w = make_word(g2p, sa, "alma")
        rendered = render_stressed_ipa(w)
        assert "ˈ" in rendered  # Primary stress marker present

    def test_stressed_ipa_text(self):
        g2p = AzerbaijaniG2P()
        words = g2p.convert_text("salam dünya")
        words = assign_stress(words)
        result = stressed_ipa(words)
        assert len(result) > 0
        assert "ˈ" in result

    def test_punctuation_in_stressed_ipa(self):
        g2p = AzerbaijaniG2P()
        words = g2p.convert_text("salam!")
        words = assign_stress(words)
        result = stressed_ipa(words)
        assert "!" in result
