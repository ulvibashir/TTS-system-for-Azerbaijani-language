"""Tests for text_normalizer.py — NSW expansion, numbers, dates, symbols."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from text_normalizer import (
    normalize, cardinal_to_words, ordinal_to_words, roman_to_words,
    expand_abbreviations, expand_symbols, normalize_dates, normalize_times,
    clean_whitespace, normalize_punctuation, _int_to_words, _ordinal_suffix,
)


# ---------------------------------------------------------------------------
# Number-to-words conversion
# ---------------------------------------------------------------------------

class TestCardinalNumbers:
    def test_zero(self):
        assert _int_to_words(0) == "sıfır"

    def test_single_digits(self):
        assert _int_to_words(1) == "bir"
        assert _int_to_words(5) == "beş"
        assert _int_to_words(9) == "doqquz"

    def test_tens(self):
        assert _int_to_words(10) == "on"
        assert _int_to_words(20) == "iyirmi"
        assert _int_to_words(50) == "əlli"

    def test_compound(self):
        result = _int_to_words(15)
        assert "on" in result
        assert "beş" in result

    def test_hundreds(self):
        assert "yüz" in _int_to_words(100)
        assert "iki" in _int_to_words(200)

    def test_thousands(self):
        assert "min" in _int_to_words(1000)
        assert "iki" in _int_to_words(2000)

    def test_large_number(self):
        result = _int_to_words(1000000)
        assert "milyon" in result

    def test_negative(self):
        result = _int_to_words(-5)
        assert "mənfi" in result
        assert "beş" in result

    def test_cardinal_in_text(self):
        result = cardinal_to_words("Mən 3 kitab aldım.")
        assert "3" not in result
        assert "üç" in result

    def test_cardinal_large_in_text(self):
        result = cardinal_to_words("Əhali 2300000 nəfərdir.")
        assert "milyon" in result


# ---------------------------------------------------------------------------
# Ordinal numbers
# ---------------------------------------------------------------------------

class TestOrdinalNumbers:
    def test_ordinal_basic(self):
        result = ordinal_to_words("1-ci")
        assert "bir" in result
        assert "inci" in result

    def test_ordinal_back_rounded(self):
        result = ordinal_to_words("3-cü")
        assert "üç" in result
        assert "üncü" in result

    def test_ordinal_suffix_vowel_harmony(self):
        # bir → front unrounded → -inci
        assert _ordinal_suffix("bir") == "inci"
        # otuz → back rounded → -uncu
        assert _ordinal_suffix("otuz") == "uncu"
        # qırx → back unrounded → -ıncı
        assert _ordinal_suffix("qırx") == "ıncı"
        # üç → front rounded → -üncü
        assert _ordinal_suffix("üç") == "üncü"

    def test_ordinal_in_sentence(self):
        result = ordinal_to_words("2024-cü ildə")
        assert "2024" not in result or "cü" not in result


# ---------------------------------------------------------------------------
# Roman numerals
# ---------------------------------------------------------------------------

class TestRomanNumerals:
    def test_basic(self):
        result = roman_to_words("III")
        assert "üç" in result

    def test_xxi(self):
        result = roman_to_words("XXI əsrdə")
        assert "iyirmi" in result
        assert "bir" in result


# ---------------------------------------------------------------------------
# Abbreviations
# ---------------------------------------------------------------------------

class TestAbbreviations:
    def test_prof(self):
        result = expand_abbreviations("Prof. Əliyev")
        assert "Prof." not in result or "professor" in result.lower() or "Profesor" in result

    def test_dr(self):
        result = expand_abbreviations("Dr. Həsənov")
        assert "Dr." not in result or "doktor" in result.lower() or "Doktor" in result


# ---------------------------------------------------------------------------
# Symbol expansion
# ---------------------------------------------------------------------------

class TestSymbols:
    def test_manat_symbol(self):
        result = expand_symbols("150₼")
        assert "manat" in result

    def test_celsius(self):
        result = expand_symbols("25°C")
        assert ("dərəcə" in result or "selsi" in result.lower()
                or "Selsi" in result)

    def test_km(self):
        result = expand_symbols("120 km")
        assert "kilometr" in result


# ---------------------------------------------------------------------------
# Dates and times
# ---------------------------------------------------------------------------

class TestDatesAndTimes:
    def test_date_format(self):
        result = normalize_dates("15.06.2023")
        # Should contain day, month name, year in words
        assert "iyun" in result or "İyun" in result

    def test_time_format(self):
        result = normalize_times("09:30")
        assert "saat" in result
        assert "dəqiqə" in result

    def test_time_exact_hour(self):
        result = normalize_times("14:00")
        assert "saat" in result


# ---------------------------------------------------------------------------
# Punctuation and cleanup
# ---------------------------------------------------------------------------

class TestCleanup:
    def test_smart_quotes(self):
        result = normalize_punctuation("\u201ctest\u201d")
        assert '"' in result

    def test_ellipsis(self):
        result = normalize_punctuation("test\u2026")
        assert "..." in result

    def test_whitespace(self):
        assert clean_whitespace("  a   b  ") == "a b"


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------

class TestFullNormalization:
    def test_simple_text(self):
        result = normalize("Azərbaycan gözəl ölkədir.")
        # Should pass through without changes (no NSWs)
        assert "gözəl" in result

    def test_numbers_and_abbreviations(self):
        result = normalize("Prof. Əliyev 2024-cü ildə 3 kitab nəşr etdi.")
        assert "3" not in result or "üç" in result

    def test_currency(self):
        result = normalize("Qiymət 150₼-dır.")
        assert "manat" in result

    def test_date_sentence(self):
        result = normalize("O, 15.06.2023 tarixində doğulub.")
        assert "iyun" in result.lower() or "İyun" in result

    def test_idempotent_plain_text(self):
        text = "Salam dünya"
        assert normalize(text) == text
