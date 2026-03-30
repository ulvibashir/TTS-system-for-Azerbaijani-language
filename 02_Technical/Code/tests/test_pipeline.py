"""Integration tests for pipeline.py — full TTS pipeline without audio synthesis."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import pytest
from pipeline import AzTTSPipeline, PipelineConfig


# ---------------------------------------------------------------------------
# Pipeline initialization
# ---------------------------------------------------------------------------

class TestPipelineInit:
    def test_default_config(self):
        p = AzTTSPipeline()
        assert p.config.speaking_style == "neutral"
        assert p.config.speaker_gender == "male"
        assert p.config.speed == 140

    def test_custom_config(self):
        cfg = PipelineConfig(speaking_style="formal", speaker_gender="female", speed=160)
        p = AzTTSPipeline(config=cfg)
        assert p.config.speaking_style == "formal"
        assert p.config.speaker_gender == "female"
        assert p.config.speed == 160


# ---------------------------------------------------------------------------
# Analysis mode (no audio synthesis required)
# ---------------------------------------------------------------------------

class TestPipelineAnalysis:
    def test_analyze_returns_dict(self):
        p = AzTTSPipeline()
        result = p.analyze("Azərbaycan gözəl ölkədir.")
        assert isinstance(result, dict)

    def test_analyze_has_required_keys(self):
        p = AzTTSPipeline()
        result = p.analyze("Salam dünya.")
        required_keys = ["input", "normalized", "words", "ipa",
                         "stressed_ipa", "sentence_type", "pauses_ms", "ssml"]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_analyze_input_preserved(self):
        text = "Azərbaycan gözəl ölkədir."
        p = AzTTSPipeline()
        result = p.analyze(text)
        assert result["input"] == text

    def test_analyze_normalized_text(self):
        p = AzTTSPipeline()
        result = p.analyze("Prof. Əliyev 3 kitab aldı.")
        # "3" should be normalized to "üç"
        assert "üç" in result["normalized"]

    def test_analyze_ipa_non_empty(self):
        p = AzTTSPipeline()
        result = p.analyze("Salam.")
        assert len(result["ipa"]) > 0

    def test_analyze_stressed_ipa_has_stress(self):
        p = AzTTSPipeline()
        result = p.analyze("Salam dünya.")
        assert "ˈ" in result["stressed_ipa"]

    def test_analyze_sentence_type_declarative(self):
        p = AzTTSPipeline()
        result = p.analyze("Bu bir testdir.")
        assert result["sentence_type"] == "declarative"

    def test_analyze_sentence_type_question(self):
        p = AzTTSPipeline()
        result = p.analyze("Kim gəldi?")
        assert result["sentence_type"] in ("wh_question", "yn_question")

    def test_analyze_sentence_type_exclamatory(self):
        p = AzTTSPipeline()
        result = p.analyze("Nə gözəldir!")
        assert result["sentence_type"] == "exclamatory"

    def test_analyze_ssml_valid(self):
        p = AzTTSPipeline()
        result = p.analyze("Salam dünya.")
        assert "<speak" in result["ssml"]
        assert "</speak>" in result["ssml"]


# ---------------------------------------------------------------------------
# text_to_ipa convenience method
# ---------------------------------------------------------------------------

class TestTextToIpa:
    def test_basic(self):
        p = AzTTSPipeline()
        ipa = p.text_to_ipa("salam")
        assert len(ipa) > 0

    def test_normalization_before_ipa(self):
        p = AzTTSPipeline()
        ipa = p.text_to_ipa("3 kitab")
        # "3" should be normalized to "üç" first, then converted
        assert len(ipa) > 5  # More than just the original

    def test_multi_word(self):
        p = AzTTSPipeline()
        ipa = p.text_to_ipa("gözəl ölkə")
        assert " " in ipa


# ---------------------------------------------------------------------------
# Tokenization edge cases
# ---------------------------------------------------------------------------

class TestTokenization:
    def test_trailing_punctuation(self):
        p = AzTTSPipeline()
        result = p.analyze("Salam!")
        assert "!" not in result["ipa"]  # Punctuation not in IPA

    def test_comma_separated(self):
        p = AzTTSPipeline()
        result = p.analyze("Gəl, gedək.")
        assert len(result["words"]) >= 2

    def test_empty_normalized_handled(self):
        p = AzTTSPipeline()
        # Simple text that shouldn't fail
        result = p.analyze("Test.")
        assert result is not None


# ---------------------------------------------------------------------------
# Run all 50 test sentences through analysis
# ---------------------------------------------------------------------------

class TestAllTestSentences:
    """Run all 50 phonetically balanced test sentences through the pipeline."""

    @pytest.fixture
    def test_sentences(self):
        sentences_path = Path(__file__).resolve().parent.parent / "evaluation" / "test_sentences.json"
        with open(sentences_path, encoding="utf-8") as f:
            data = json.load(f)
        return data["sentences"]

    def test_all_sentences_analyzable(self, test_sentences):
        p = AzTTSPipeline()
        failures = []
        for sent in test_sentences:
            try:
                result = p.analyze(sent["text"])
                assert result["ipa"], f"Empty IPA for sentence {sent['id']}"
            except Exception as e:
                failures.append(f"Sentence {sent['id']}: {e}")
        assert not failures, f"Failures:\n" + "\n".join(failures)

    def test_sentence_types_match(self, test_sentences):
        p = AzTTSPipeline()
        mismatches = []
        for sent in test_sentences:
            result = p.analyze(sent["text"])
            if result["sentence_type"] != sent["expected_type"]:
                mismatches.append(
                    f"Sentence {sent['id']}: expected {sent['expected_type']}, "
                    f"got {result['sentence_type']} — {sent['text']}"
                )
        # Allow some mismatches (sentence type detection is heuristic)
        # but flag them for review
        if mismatches:
            print(f"\nSentence type mismatches ({len(mismatches)}):")
            for m in mismatches:
                print(f"  {m}")
        # Require at least 80% accuracy
        accuracy = 1 - len(mismatches) / len(test_sentences)
        assert accuracy >= 0.8, (
            f"Sentence type accuracy {accuracy:.0%} < 80%. "
            f"Mismatches:\n" + "\n".join(mismatches)
        )

    def test_all_sentences_produce_stressed_ipa(self, test_sentences):
        p = AzTTSPipeline()
        for sent in test_sentences:
            result = p.analyze(sent["text"])
            assert len(result["stressed_ipa"]) > 0, (
                f"Sentence {sent['id']} produced empty stressed IPA"
            )
