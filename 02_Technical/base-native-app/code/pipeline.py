"""
Main TTS Pipeline for Azerbaijani

Orchestrates the full text-to-speech conversion pipeline:

  Input text
      │
      ▼
  [1] Text Normalization     (text_normalizer.py)
      │  numbers, abbreviations, symbols → written-out words
      ▼
  [2] Tokenization           (utils.tokenize)
      │  split into words and punctuation
      ▼
  [3] G2P Conversion         (g2p_converter.py)
      │  graphemes → IPA phonemes + syllabification
      ▼
  [4] Stress Assignment      (stress_assigner.py)
      │  mark primary stress per word + phrasal stress
      ▼
  [5] Prosody Annotation     (prosody_engine.py)
      │  pitch targets, phone durations, pause insertion
      ▼
  [6] Speech Synthesis       (synthesizer.py)
      │  espeak-ng → WAV audio
      ▼
  Output WAV

Usage:
    from pipeline import AzTTSPipeline
    pipeline = AzTTSPipeline()
    pipeline.synthesize("Azərbaycan gözəl ölkədir.", output="out.wav")
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from text_normalizer import normalize
from g2p_converter import AzerbaijaniG2P, Word, text_to_words
from stress_assigner import StressAssigner, assign_stress, stressed_ipa
from prosody_engine import ProsodyEngine, SentenceAnnotation, to_ssml
from synthesizer import Synthesizer, SynthConfig, espeak_available
from utils import setup_logger, split_sentences, tokenize


logger = setup_logger("az_tts.pipeline")


# ---------------------------------------------------------------------------
# Pipeline configuration
# ---------------------------------------------------------------------------

@dataclass
class PipelineConfig:
    """Global configuration for the TTS pipeline."""
    speaking_style: str = "neutral"     # neutral | formal | conversational
    speaker_gender: str = "male"        # male | female
    language_code: str = "az"           # espeak-ng language code
    sample_rate: int = 22050            # output sample rate
    speed: int = 140                    # words per minute
    pitch: int = 50                     # espeak-ng pitch (0-99)
    amplitude: int = 100                # espeak-ng amplitude (0-200)
    output_format: str = "wav"          # wav (only option for now)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

class AzTTSPipeline:
    """
    End-to-end rule-based TTS pipeline for North Azerbaijani.

    Parameters
    ----------
    config : PipelineConfig, optional
        Pipeline-wide settings. Defaults to neutral style, male voice.
    """

    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        self.g2p     = AzerbaijaniG2P()
        self.sa      = StressAssigner()
        self.pe      = ProsodyEngine(
            speaking_style=self.config.speaking_style,
            speaker_gender=self.config.speaker_gender
        )
        self._synth: Optional[Synthesizer] = None

    @property
    def synth(self) -> Synthesizer:
        """Lazy-initialize synthesizer (avoids error if espeak-ng absent)."""
        if self._synth is None:
            synth_cfg = SynthConfig(
                language=self.config.language_code,
                sample_rate=self.config.sample_rate,
                speed=self.config.speed,
                pitch=self.config.pitch,
                amplitude=self.config.amplitude,
            )
            self._synth = Synthesizer(synth_cfg)
        return self._synth

    # --- public interface ---------------------------------------------------

    def synthesize(self, text: str,
                   output: Optional[Union[str, Path]] = None) -> bytes:
        """
        Convert Azerbaijani text to speech.

        Parameters
        ----------
        text : str
            Raw Azerbaijani input text (may contain numbers, abbreviations, etc.)
        output : str or Path, optional
            If provided, write WAV to this path.

        Returns
        -------
        bytes
            Raw WAV audio bytes.
        """
        logger.info(f"Synthesizing: {text!r}")

        # 1. Text normalization
        normalized = normalize(text)
        logger.debug(f"  [norm]   {normalized!r}")

        # 2. Sentence splitting
        sentences = split_sentences(normalized)
        all_wav = b""

        for sent in sentences:
            wav = self._process_sentence(sent)
            all_wav += wav

        if output:
            Path(output).write_bytes(all_wav)
            logger.info(f"  [output] {Path(output).resolve()}")

        return all_wav

    def analyze(self, text: str) -> dict:
        """
        Analyze text through the pipeline without synthesizing audio.

        Returns a dict with intermediate representations at each stage,
        useful for debugging and dissertation evaluation.

        Parameters
        ----------
        text : str
            Raw Azerbaijani input text.

        Returns
        -------
        dict with keys:
            'input', 'normalized', 'words', 'ipa', 'stressed_ipa',
            'sentence_type', 'pauses_ms'
        """
        normalized = normalize(text)
        words = self._tokenize_and_convert(normalized)
        words = assign_stress(words)
        annotation = self.pe.annotate(words)

        return {
            "input":        text,
            "normalized":   normalized,
            "words":        [w.graphemes for w in words],
            "ipa":          " ".join(
                                "".join(ph.symbol for ph in w.phonemes)
                                for w in words if w.graphemes not in
                                (".", ",", "!", "?", ";", ":", "—")
                            ),
            "stressed_ipa": stressed_ipa(words),
            "sentence_type": annotation.sentence_type,
            "pauses_ms":    annotation.pauses_ms,
            "ssml":         to_ssml(annotation),
        }

    def text_to_ipa(self, text: str) -> str:
        """Convenience: normalize + convert to IPA string."""
        normalized = normalize(text)
        words = self._tokenize_and_convert(normalized)
        return " ".join(
            "".join(ph.symbol for ph in w.phonemes)
            for w in words
            if w.graphemes not in (".", ",", "!", "?", ";", ":", "—")
        )

    # --- internal helpers ---------------------------------------------------

    def _process_sentence(self, sentence: str) -> bytes:
        """Process a single sentence through G2P → stress → prosody → synth."""
        words = self._tokenize_and_convert(sentence)
        words = assign_stress(words)
        annotation = self.pe.annotate(words)

        if espeak_available():
            return self.synth.synthesize_annotation(annotation)
        else:
            logger.warning("espeak-ng not available; returning empty audio.")
            return b""

    def _tokenize_and_convert(self, text: str) -> list:
        """Tokenize text and run G2P on each token."""
        tokens = re.split(r"(\s+|(?<=[^\s])([,\.!?;:—])(?=[^\s]|$)|"
                          r"(?<=[^\s])\s+([,\.!?;:—]))", text)

        words = []
        for tok in re.split(r"\s+", text):
            tok = tok.strip()
            if not tok:
                continue
            # Separate trailing punctuation
            match = re.match(r"^([\w\u0400-\u04FFəğışöüçƏĞIŞÖÜÇ]+)([,\.!?;:—]*)$",
                             tok, re.UNICODE)
            if match:
                word_part  = match.group(1)
                punct_part = match.group(2)
                if word_part:
                    words.append(self.g2p.convert_word(word_part))
                for p in punct_part:
                    words.append(Word(graphemes=p))
            else:
                if re.match(r"^[,\.!?;:—]+$", tok):
                    words.append(Word(graphemes=tok))
                else:
                    words.append(self.g2p.convert_word(tok))

        return words


# ---------------------------------------------------------------------------
# CLI usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import json

    pipeline = AzTTSPipeline()

    if "--analyze" in sys.argv:
        sys.argv.remove("--analyze")
        text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
            "Azərbaycan gözəl ölkədir."
        result = pipeline.analyze(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "Azərbaycan gözəl ölkədir."
    output_path = Path("output.wav")

    if espeak_available():
        pipeline.synthesize(text, output=output_path)
        print(f"Synthesized: {output_path.resolve()}")
    else:
        print("espeak-ng not found — running analysis only:\n")
        result = pipeline.analyze(text)
        for key, val in result.items():
            print(f"  {key}: {val}")
