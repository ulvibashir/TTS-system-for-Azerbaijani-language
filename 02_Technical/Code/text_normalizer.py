"""
Text Normalization Module for Azerbaijani TTS

Converts non-standard words (NSWs) to their spoken form:
  - Numbers (cardinal, ordinal)
  - Abbreviations and acronyms
  - Currency and unit symbols
  - Dates and times
  - Roman numerals
  - Special characters
"""

import re
import json
from pathlib import Path


RULES_PATH = Path(__file__).parent.parent / "Rules" / "text_norm_rules.json"


def load_rules() -> dict:
    with open(RULES_PATH, encoding="utf-8") as f:
        return json.load(f)


RULES = load_rules()


# ---------------------------------------------------------------------------
# Number-to-words conversion
# ---------------------------------------------------------------------------

def _int_to_words(n: int) -> str:
    """Convert a non-negative integer to Azerbaijani words."""
    if n == 0:
        return RULES["digits"]["0"]

    if n < 0:
        return "mənfi " + _int_to_words(-n)

    digits  = RULES["digits"]
    tens    = RULES["tens"]
    large   = RULES["large_numbers"]
    parts   = []

    if n >= 1_000_000_000_000:
        t = n // 1_000_000_000_000
        parts.append(_int_to_words(t) + " " + large["1000000000000"])
        n %= 1_000_000_000_000

    if n >= 1_000_000_000:
        b = n // 1_000_000_000
        parts.append(_int_to_words(b) + " " + large["1000000000"])
        n %= 1_000_000_000

    if n >= 1_000_000:
        m = n // 1_000_000
        parts.append(_int_to_words(m) + " " + large["1000000"])
        n %= 1_000_000

    if n >= 1000:
        k = n // 1000
        prefix = "" if k == 1 else (_int_to_words(k) + " ")
        parts.append(prefix + large["1000"])
        n %= 1000

    if n >= 100:
        h = (n // 100) * 100
        hundreds = RULES["hundreds"]
        parts.append(hundreds[str(h)])
        n %= 100

    if n >= 10:
        t_key = str((n // 10) * 10)
        parts.append(tens[t_key])
        n %= 10

    if n > 0:
        parts.append(digits[str(n)])

    return " ".join(parts)


def _last_vowel(word: str) -> str:
    """Return the last vowel in the word (for vowel harmony in ordinals)."""
    vowels = "aeəıioöuü"
    for ch in reversed(word.lower()):
        if ch in vowels:
            return ch
    return "a"


def _ordinal_suffix(word: str) -> str:
    """Return the correct ordinal suffix by vowel harmony."""
    lv = _last_vowel(word)
    sr = RULES["ordinal_suffixes"]
    if lv in ("a", "ı"):
        return sr["back_unrounded"]
    if lv in ("e", "ə", "i"):
        return sr["front_unrounded"]
    if lv in ("o", "u"):
        return sr["back_rounded"]
    return sr["front_rounded"]  # ö, ü


def cardinal_to_words(text: str) -> str:
    """Replace cardinal numbers with Azerbaijani words."""
    def replace(match):
        raw = match.group(0).replace(",", "").replace(".", "")
        try:
            return _int_to_words(int(raw))
        except ValueError:
            return match.group(0)

    return re.sub(r"\b\d[\d,\.]*\d|\b\d\b", replace, text)


def ordinal_to_words(text: str) -> str:
    """Replace ordinal numbers (e.g., 1-ci, 2-inci) with Azerbaijani words."""
    def replace(match):
        num_str = match.group(1)
        try:
            word = _int_to_words(int(num_str))
            suffix = _ordinal_suffix(word)
            return word + suffix
        except ValueError:
            return match.group(0)

    # Patterns: 1-ci, 2-inci, 3-üncü, etc.
    return re.sub(r"\b(\d+)-(?:ci|cü|cu|cı|inci|ıncı|uncu|üncü|nci|ncı|ncu|ncü)\b",
                  replace, text)


# ---------------------------------------------------------------------------
# Roman numeral conversion
# ---------------------------------------------------------------------------

_ROMAN_PATTERN = re.compile(
    r"\b(M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b"
)

_ROMAN_VALUES = [
    ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
    ("C",  100), ("XC",  90), ("L",  50), ("XL",  40),
    ("X",   10), ("IX",   9), ("V",   5), ("IV",   4), ("I", 1)
]


def _roman_to_int(s: str) -> int:
    result, i = 0, 0
    for numeral, value in _ROMAN_VALUES:
        while s[i:i+len(numeral)] == numeral:
            result += value
            i += len(numeral)
    return result


def roman_to_words(text: str) -> str:
    """Replace Roman numerals with Azerbaijani words where unambiguous."""
    def replace(match):
        roman = match.group(0)
        if not roman:
            return roman
        val = _roman_to_int(roman)
        if val == 0:
            return roman
        return _int_to_words(val)

    return _ROMAN_PATTERN.sub(replace, text)


# ---------------------------------------------------------------------------
# Abbreviation and symbol expansion
# ---------------------------------------------------------------------------

def expand_abbreviations(text: str) -> str:
    """Replace known abbreviations with their full spoken form."""
    abbrevs = RULES["abbreviations"]
    for abbr, expansion in sorted(abbrevs.items(), key=lambda x: -len(x[0])):
        pattern = re.escape(abbr)
        text = re.sub(r"(?<!\w)" + pattern + r"(?!\w)", expansion, text,
                      flags=re.IGNORECASE)
    return text


def expand_symbols(text: str) -> str:
    """Replace currency symbols, unit symbols and special characters."""
    for sym, word in RULES["currency_symbols"].items():
        text = text.replace(sym, " " + word + " ")

    for sym, word in RULES["unit_symbols"].items():
        # Only replace when immediately after a number
        text = re.sub(r"(\d)\s*" + re.escape(sym) + r"\b",
                      r"\1 " + word, text)

    for sym, word in RULES["special_chars"].items():
        text = text.replace(sym, " " + word + " ")

    return text


# ---------------------------------------------------------------------------
# Date and time normalization
# ---------------------------------------------------------------------------

def normalize_dates(text: str) -> str:
    """Convert date patterns (DD.MM.YYYY) to spoken Azerbaijani."""
    months = RULES["date_months"]

    def replace_dmy(match):
        day   = int(match.group(1))
        month = match.group(2).zfill(2)
        year  = match.group(3)
        day_word   = _int_to_words(day) + _ordinal_suffix(_int_to_words(day))
        month_word = months.get(month, month)
        year_word  = _int_to_words(int(year)) + "-ci il"
        return f"{day_word} {month_word} {year_word}"

    text = re.sub(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b", replace_dmy, text)
    return text


def normalize_times(text: str) -> str:
    """Convert HH:MM time patterns to spoken Azerbaijani."""
    def replace_time(match):
        h = int(match.group(1))
        m = int(match.group(2))
        h_word = _int_to_words(h) + " saat"
        if m == 0:
            return h_word
        m_word = _int_to_words(m) + " dəqiqə"
        return h_word + " " + m_word

    return re.sub(r"\b(\d{1,2}):(\d{2})\b", replace_time, text)


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def clean_whitespace(text: str) -> str:
    """Collapse multiple spaces and strip leading/trailing whitespace."""
    return re.sub(r" {2,}", " ", text).strip()


def normalize_punctuation(text: str) -> str:
    """Normalize punctuation: smart quotes → straight, ellipsis, etc."""
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u2026", "...")
    text = text.replace("\u2013", "-").replace("\u2014", "—")
    return text


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """
    Run full text normalization pipeline on Azerbaijani input text.

    Processing order:
        1. Punctuation normalization
        2. Symbol expansion (currency, units, special chars)
        3. Date normalization
        4. Time normalization
        5. Ordinal number expansion
        6. Cardinal number expansion
        7. Roman numeral expansion
        8. Abbreviation expansion
        9. Whitespace cleanup

    Parameters
    ----------
    text : str
        Raw Azerbaijani input text.

    Returns
    -------
    str
        Normalized text ready for G2P conversion.
    """
    text = normalize_punctuation(text)
    text = expand_symbols(text)
    text = normalize_dates(text)
    text = normalize_times(text)
    text = ordinal_to_words(text)
    text = cardinal_to_words(text)
    text = roman_to_words(text)
    text = expand_abbreviations(text)
    text = clean_whitespace(text)
    return text


# ---------------------------------------------------------------------------
# CLI usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    samples = [
        "Azərbaycan 1991-ci ildə müstəqilliyini bərpa etdi.",
        "Dr. Əliyev 15.06.2023 tarixində saat 09:30-da çıxış etdi.",
        "Kitab 25₼ dəyərindədir.",
        "Bakı şəhərinin əhalisi 2.300.000 nəfərdir.",
        "XXI əsrdə süni intellekt sürətlə inkişaf edir.",
        "Temperatur -5°C-dir.",
        "3-cü mərhələ uğurla başa çatdı.",
    ]
    inputs = sys.argv[1:] if len(sys.argv) > 1 else samples
    for inp in inputs:
        print(f"IN:  {inp}")
        print(f"OUT: {normalize(inp)}")
        print()
