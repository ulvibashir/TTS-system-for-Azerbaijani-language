"""
Synthesizer Module for Azerbaijani TTS

Converts prosodic annotations to audio using espeak-ng as the acoustic backend.
espeak-ng natively supports Azerbaijani (-v az) and can:
  - Read normalized text with Azerbaijani phoneme rules
  - Accept IPA phoneme sequences via [[...]] notation
  - Output WAV audio to file or stdout

This module:
  1. Accepts a SentenceAnnotation from the ProsodyEngine
  2. Builds an espeak-ng command with prosody parameters
  3. Invokes espeak-ng as a subprocess
  4. Returns the path to the generated WAV file or raw audio bytes

Dependencies:
  - espeak-ng must be installed and on PATH
    Linux/macOS: sudo apt install espeak-ng / brew install espeak
    Windows:     https://github.com/espeak-ng/espeak-ng/releases
  - Optional: sounddevice (for playback)
"""

import io
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

from prosody_engine import SentenceAnnotation, to_espeak_markup


# ---------------------------------------------------------------------------
# Availability check
# ---------------------------------------------------------------------------

def espeak_available() -> bool:
    """Return True if espeak-ng is installed and reachable."""
    return shutil.which("espeak-ng") is not None


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class SynthConfig:
    """Configuration for the speech synthesizer."""
    language: str = "az"           # espeak-ng voice code for Azerbaijani
    sample_rate: int = 22050       # Output sample rate (Hz)
    amplitude: int = 100           # Volume 0-200
    speed: int = 140               # Words per minute (default: 175)
    pitch: int = 50                # Pitch 0-99 (default: 50)
    gap: int = 10                  # Pause between words (ms units in espeak)
    use_ipa: bool = False          # Send IPA phonemes directly instead of text


# ---------------------------------------------------------------------------
# Core synthesizer
# ---------------------------------------------------------------------------

class Synthesizer:
    """
    Converts text or prosodic annotations to speech via espeak-ng.
    """

    def __init__(self, config: Optional[SynthConfig] = None):
        self.config = config or SynthConfig()
        self._check_espeak()

    def _check_espeak(self):
        if not espeak_available():
            raise RuntimeError(
                "espeak-ng is not installed or not on PATH.\n"
                "Install: https://github.com/espeak-ng/espeak-ng/releases\n"
                "Linux:   sudo apt install espeak-ng\n"
                "macOS:   brew install espeak"
            )

    def synthesize_text(self, text: str,
                        output_path: Optional[Union[str, Path]] = None
                        ) -> bytes:
        """
        Synthesize raw normalized Azerbaijani text to WAV audio.

        Parameters
        ----------
        text : str
            Normalized Azerbaijani text (output of TextNormalizer).
        output_path : str or Path, optional
            If provided, write WAV to this file.

        Returns
        -------
        bytes
            Raw WAV audio data.
        """
        cmd = self._build_command(text, use_ipa=False)
        return self._run(cmd, output_path)

    def synthesize_annotation(self, annotation: SentenceAnnotation,
                               output_path: Optional[Union[str, Path]] = None
                               ) -> bytes:
        """
        Synthesize from a ProsodyEngine annotation.

        Converts the annotation to espeak markup text and invokes espeak-ng
        with adjusted prosody parameters.

        Parameters
        ----------
        annotation : SentenceAnnotation
        output_path : str or Path, optional

        Returns
        -------
        bytes
            Raw WAV audio data.
        """
        markup = to_espeak_markup(annotation)

        # Adjust speed/pitch based on sentence type
        cfg = SynthConfig(
            language=self.config.language,
            sample_rate=self.config.sample_rate,
            amplitude=self.config.amplitude,
            speed=self._speed_for_type(annotation.sentence_type),
            pitch=self._pitch_for_type(annotation.sentence_type),
            gap=self.config.gap,
        )
        cmd = self._build_command(markup, config=cfg, use_ipa=False)
        return self._run(cmd, output_path)

    def synthesize_ipa(self, ipa_string: str,
                       output_path: Optional[Union[str, Path]] = None
                       ) -> bytes:
        """
        Synthesize from an IPA phoneme string using espeak-ng's IPA mode.

        Parameters
        ----------
        ipa_string : str
            IPA phoneme string (space-separated words).
        output_path : str or Path, optional

        Returns
        -------
        bytes
            Raw WAV audio data.
        """
        # espeak-ng IPA notation: wrap in [[ ]]
        formatted = "[[" + ipa_string + "]]"
        cmd = self._build_command(formatted, use_ipa=True)
        return self._run(cmd, output_path)

    # --- espeak-ng command builder ------------------------------------------

    def _build_command(self, text: str,
                       config: Optional[SynthConfig] = None,
                       use_ipa: bool = False) -> List[str]:
        """Build the espeak-ng subprocess command."""
        cfg = config or self.config
        cmd = [
            "espeak-ng",
            "-v", cfg.language,
            "-s", str(cfg.speed),
            "-p", str(cfg.pitch),
            "-a", str(cfg.amplitude),
            "-g", str(cfg.gap),
            "--ipa=3" if use_ipa else "",
            "-w", "/dev/stdout",    # WAV to stdout (overridden if file given)
        ]
        # Remove empty strings
        cmd = [c for c in cmd if c]
        cmd += [text]
        return cmd

    def _run(self, cmd: List[str],
             output_path: Optional[Union[str, Path]]) -> bytes:
        """Execute espeak-ng and capture WAV output."""
        if output_path:
            # Replace /dev/stdout with actual file path
            cmd = [
                c if c != "/dev/stdout" else str(output_path)
                for c in cmd
            ]
            # Replace -w /dev/stdout with -w <file>
            w_idx = cmd.index("-w")
            cmd[w_idx + 1] = str(output_path)
            subprocess.run(cmd, check=True,
                           stderr=subprocess.DEVNULL)
            with open(output_path, "rb") as f:
                return f.read()
        else:
            # On Windows /dev/stdout doesn't work; use a temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                cmd_file = [
                    c if c != "/dev/stdout" else tmp_path
                    for c in cmd
                ]
                w_idx = cmd_file.index("-w")
                cmd_file[w_idx + 1] = tmp_path
                subprocess.run(cmd_file, check=True,
                               stderr=subprocess.DEVNULL)
                with open(tmp_path, "rb") as f:
                    return f.read()
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

    # --- prosody-type modifiers ---------------------------------------------

    @staticmethod
    def _speed_for_type(sentence_type: str) -> int:
        return {
            "declarative": 140,
            "yn_question": 145,
            "wh_question": 140,
            "exclamatory": 155,
            "imperative":  148,
        }.get(sentence_type, 140)

    @staticmethod
    def _pitch_for_type(sentence_type: str) -> int:
        return {
            "declarative": 50,
            "yn_question": 58,
            "wh_question": 55,
            "exclamatory": 62,
            "imperative":  54,
        }.get(sentence_type, 50)


# ---------------------------------------------------------------------------
# Playback helper (requires sounddevice + scipy)
# ---------------------------------------------------------------------------

def play_audio(wav_bytes: bytes) -> None:
    """Play WAV bytes through the default audio device."""
    try:
        import io
        import sounddevice as sd
        import scipy.io.wavfile as wav

        rate, data = wav.read(io.BytesIO(wav_bytes))
        sd.play(data, rate)
        sd.wait()
    except ImportError:
        raise ImportError(
            "playback requires: pip install sounddevice scipy"
        )


# ---------------------------------------------------------------------------
# CLI usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if not espeak_available():
        print("ERROR: espeak-ng is not installed.")
        print("  Linux:   sudo apt install espeak-ng")
        print("  macOS:   brew install espeak")
        print("  Windows: https://github.com/espeak-ng/espeak-ng/releases")
        sys.exit(1)

    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "Azərbaycan gözəl ölkədir."

    synth = Synthesizer()
    output = Path("output.wav")
    print(f"Synthesizing: {text!r}")
    synth.synthesize_text(text, output_path=output)
    print(f"Saved to: {output.resolve()}")
