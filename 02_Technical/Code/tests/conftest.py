"""
Shared pytest fixtures for Azerbaijani TTS test suite.
"""

import sys
from pathlib import Path

# Add the Code directory to sys.path so module imports work
CODE_DIR = Path(__file__).resolve().parent.parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import pytest
from g2p_converter import AzerbaijaniG2P, Word
from stress_assigner import StressAssigner
from prosody_engine import ProsodyEngine


@pytest.fixture
def g2p():
    return AzerbaijaniG2P()


@pytest.fixture
def stress_assigner():
    return StressAssigner()


@pytest.fixture
def prosody_engine():
    return ProsodyEngine(speaking_style="neutral", speaker_gender="male")


@pytest.fixture
def sample_words(g2p, stress_assigner):
    """A set of common Azerbaijani words converted and stress-assigned."""
    words_text = ["alma", "kitab", "gözəl", "Azərbaycan", "məktəb"]
    words = []
    for w in words_text:
        word = g2p.convert_word(w)
        stress_assigner.assign_word_stress(word)
        words.append(word)
    return words
