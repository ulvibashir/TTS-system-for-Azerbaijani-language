"""
Utility functions for the Azerbaijani TTS system.

Provides:
  - Azerbaijani-specific text utilities (vowel detection, syllable counting)
  - Audio file I/O helpers
  - Evaluation metrics (MOS logging, intelligibility helpers)
  - Logging setup
"""

import logging
import re
import wave
import struct
from pathlib import Path
from typing import List, Tuple, Optional, Union


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logger(name: str = "az_tts",
                 level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger for the TTS system."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s",
                                datefmt="%H:%M:%S")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = setup_logger()


# ---------------------------------------------------------------------------
# Azerbaijani character sets
# ---------------------------------------------------------------------------

AZ_VOWELS     = set("aeəıioöuü")
AZ_CONSONANTS = set("bcçdfgğhxjklmnpqrsştvyz")
AZ_ALPHABET   = AZ_VOWELS | AZ_CONSONANTS

FRONT_VOWELS  = set("eəiöü")
BACK_VOWELS   = set("aıou")


def is_vowel(char: str) -> bool:
    return char.lower() in AZ_VOWELS


def is_consonant(char: str) -> bool:
    return char.lower() in AZ_CONSONANTS


def count_syllables(word: str) -> int:
    """Count syllables by counting vowel characters."""
    return sum(1 for ch in word.lower() if ch in AZ_VOWELS)


def last_vowel(word: str) -> Optional[str]:
    """Return the last vowel in a word (used for vowel harmony)."""
    for ch in reversed(word.lower()):
        if ch in AZ_VOWELS:
            return ch
    return None


def vowel_harmony_class(word: str) -> str:
    """
    Return the vowel harmony class of the word based on its last vowel.

    Returns one of: 'back_unrounded', 'back_rounded',
                    'front_unrounded', 'front_rounded', 'unknown'
    """
    lv = last_vowel(word)
    if lv is None:
        return "unknown"
    if lv in ("a", "ı"):
        return "back_unrounded"
    if lv in ("o", "u"):
        return "back_rounded"
    if lv in ("e", "ə", "i"):
        return "front_unrounded"
    if lv in ("ö", "ü"):
        return "front_rounded"
    return "unknown"


def tokenize(text: str) -> List[str]:
    """
    Tokenize Azerbaijani text into words and punctuation tokens.
    Handles Azerbaijani-specific characters.
    """
    pattern = r"[a-zA-ZəğışöüçÉƏĞIŞÖÜÇ]+|[.,!?;:—\-\"\'()]"
    return re.findall(pattern, text, re.UNICODE)


def split_sentences(text: str) -> List[str]:
    """Split a paragraph into individual sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


# ---------------------------------------------------------------------------
# Audio helpers
# ---------------------------------------------------------------------------

def save_wav(audio_bytes: bytes, path: Union[str, Path],
             sample_rate: int = 22050,
             n_channels: int = 1,
             sample_width: int = 2) -> None:
    """
    Write raw PCM audio bytes to a WAV file.

    Parameters
    ----------
    audio_bytes : bytes
        Raw PCM audio data (little-endian 16-bit signed integers).
    path : str or Path
        Output file path.
    sample_rate : int
        Samples per second (default 22050 Hz).
    n_channels : int
        Number of audio channels (1 = mono).
    sample_width : int
        Bytes per sample (2 = 16-bit).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)
    logger.info(f"WAV saved: {path}")


def load_wav(path: Union[str, Path]) -> Tuple[bytes, int, int]:
    """
    Load a WAV file.

    Returns
    -------
    (audio_bytes, sample_rate, n_channels)
    """
    with wave.open(str(path), "rb") as wf:
        rate = wf.getframerate()
        channels = wf.getnchannels()
        frames = wf.readframes(wf.getnframes())
    return frames, rate, channels


def wav_duration_seconds(path: Union[str, Path]) -> float:
    """Return the duration of a WAV file in seconds."""
    with wave.open(str(path), "rb") as wf:
        return wf.getnframes() / wf.getframerate()


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def log_mos_score(system_name: str, text: str, score: float,
                  evaluator: str = "anonymous",
                  log_file: Optional[Path] = None) -> None:
    """
    Log a Mean Opinion Score (MOS) entry.

    MOS scale (ITU-T P.800):
      5 = Excellent, 4 = Good, 3 = Fair, 2 = Poor, 1 = Bad

    Parameters
    ----------
    system_name : str
        Identifier for the TTS system or condition being evaluated.
    text : str
        The input text that was synthesized.
    score : float
        MOS score (1.0 – 5.0).
    evaluator : str
        Evaluator identifier.
    log_file : Path, optional
        If provided, append entry to a CSV log file.
    """
    if not 1.0 <= score <= 5.0:
        raise ValueError("MOS score must be between 1.0 and 5.0")

    entry = (f"system={system_name!r}, evaluator={evaluator!r}, "
             f"mos={score:.1f}, text={text!r}")
    logger.info(f"MOS entry — {entry}")

    if log_file:
        log_file = Path(log_file)
        is_new = not log_file.exists()
        with open(log_file, "a", encoding="utf-8") as f:
            if is_new:
                f.write("system,evaluator,mos,text\n")
            text_escaped = text.replace('"', '""')
            f.write(f'"{system_name}","{evaluator}",{score:.1f},"{text_escaped}"\n')


def compute_mean_mos(scores: List[float]) -> Tuple[float, float]:
    """
    Compute mean and standard deviation of MOS scores.

    Returns
    -------
    (mean, std_dev)
    """
    if not scores:
        return 0.0, 0.0
    n = len(scores)
    mean = sum(scores) / n
    variance = sum((s - mean) ** 2 for s in scores) / n
    std = variance ** 0.5
    return round(mean, 3), round(std, 3)


def character_error_rate(reference: str, hypothesis: str) -> float:
    """
    Compute Character Error Rate (CER) between reference and hypothesis.
    Used for intelligibility evaluation.

    CER = (S + D + I) / N  where S=substitutions, D=deletions, I=insertions
    """
    ref = list(reference.lower())
    hyp = list(hypothesis.lower())
    n = len(ref)
    if n == 0:
        return 0.0

    # Dynamic programming (Levenshtein distance)
    dp = list(range(len(hyp) + 1))
    for i, r_ch in enumerate(ref):
        new_dp = [i + 1]
        for j, h_ch in enumerate(hyp):
            cost = 0 if r_ch == h_ch else 1
            new_dp.append(min(new_dp[-1] + 1,    # insertion
                              dp[j + 1] + 1,       # deletion
                              dp[j] + cost))        # substitution
        dp = new_dp

    return dp[-1] / n


def word_error_rate(reference: str, hypothesis: str) -> float:
    """
    Compute Word Error Rate (WER) between reference and hypothesis.
    """
    ref = reference.lower().split()
    hyp = hypothesis.lower().split()
    n = len(ref)
    if n == 0:
        return 0.0

    dp = list(range(len(hyp) + 1))
    for i, r_w in enumerate(ref):
        new_dp = [i + 1]
        for j, h_w in enumerate(hyp):
            cost = 0 if r_w == h_w else 1
            new_dp.append(min(new_dp[-1] + 1,
                              dp[j + 1] + 1,
                              dp[j] + cost))
        dp = new_dp

    return dp[-1] / n


# ---------------------------------------------------------------------------
# Missing import fix
# ---------------------------------------------------------------------------

from typing import Union
