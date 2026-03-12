"""
Azerbaijani TTS System — Main Entry Point

Design and Development of a Rule-Based Text-to-Speech System
for the Azerbaijani Language

Usage examples:

    # Basic synthesis
    python main.py "Azərbaycan gözəl ölkədir."

    # Synthesis with output file
    python main.py --output out.wav "Salam dünya!"

    # Analysis only (no audio output)
    python main.py --analyze "Kitabı oxudunmu?"

    # Interactive mode
    python main.py --interactive

    # Demo mode (run built-in test sentences)
    python main.py --demo
"""

import argparse
import json
import sys
from pathlib import Path

from pipeline import AzTTSPipeline, PipelineConfig
from synthesizer import espeak_available
from utils import setup_logger


logger = setup_logger("az_tts.main")

# ---------------------------------------------------------------------------
# Demo sentences — covers key linguistic phenomena
# ---------------------------------------------------------------------------

DEMO_SENTENCES = [
    # Declarative
    ("Azərbaycan gözəl ölkədir.",
     "declarative — basic statement"),
    # Numbers and abbreviations
    ("Prof. Əliyev 2024-cü ildə 3 kitab nəşr etdi.",
     "numbers + abbreviation + ordinal"),
    # Question (yes/no)
    ("Sən bu kitabı oxudunmu?",
     "yes/no question with particle"),
    # Question (wh-)
    ("Kim bu işi görəcək?",
     "wh-question"),
    # Exclamatory
    ("Bu nə gözəl gündür!",
     "exclamatory"),
    # Negation
    ("O bu məktubu yazmadı.",
     "negation suffix -ma-"),
    # Postpositions and vowel harmony
    ("Uşaqlar məktəb üçün kitab aldılar.",
     "postposition üçün + agglutination"),
    # Special characters and currency
    ("Qiymət 150₼-dır.",
     "currency symbol"),
    # Soft-g (ğ) phoneme
    ("Dağlar yüksəkdir.",
     "ğ allophony — word-final lengthening"),
    # Palatal consonants
    ("Gəl, birlikdə gedək.",
     "g/k palatalization before front vowels"),
]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="az-tts",
        description="Rule-Based TTS System for Azerbaijani Language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("text", nargs="*",
                        help="Text to synthesize")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="Output WAV file (default: output.wav)")
    parser.add_argument("--analyze", action="store_true",
                        help="Print analysis at each pipeline stage (no audio)")
    parser.add_argument("--demo", action="store_true",
                        help="Run demo sentences through the pipeline")
    parser.add_argument("--interactive", action="store_true",
                        help="Interactive mode: enter text line by line")
    parser.add_argument("--style",
                        choices=["neutral", "formal", "conversational"],
                        default="neutral",
                        help="Speaking style (default: neutral)")
    parser.add_argument("--gender", choices=["male", "female"],
                        default="male",
                        help="Speaker gender for pitch baseline (default: male)")
    parser.add_argument("--speed", type=int, default=140,
                        help="Speech rate in words/min (default: 140)")
    return parser


def run_demo(pipeline: AzTTSPipeline, synthesize: bool) -> None:
    """Run all demo sentences through the pipeline."""
    print("=" * 65)
    print("  Azerbaijani TTS — Demo Mode")
    print("=" * 65)

    for i, (sent, description) in enumerate(DEMO_SENTENCES, 1):
        print(f"\n[{i:02d}] {description}")
        print(f"  Input : {sent}")

        result = pipeline.analyze(sent)
        print(f"  Norm  : {result['normalized']}")
        print(f"  IPA   : {result['ipa']}")
        print(f"  Stress: {result['stressed_ipa']}")
        print(f"  Type  : {result['sentence_type']}")

        if synthesize and espeak_available():
            out = Path(f"demo_{i:02d}.wav")
            pipeline.synthesize(sent, output=out)
            print(f"  Audio : {out.resolve()}")

    print("\n" + "=" * 65)
    if not espeak_available():
        print("NOTE: espeak-ng not found — audio synthesis skipped.")
        print("      Install espeak-ng to generate WAV files.")


def run_interactive(pipeline: AzTTSPipeline) -> None:
    """Interactive loop: read text from stdin, output analysis + WAV."""
    print("Azerbaijani TTS — Interactive Mode")
    print("Type Azerbaijani text and press Enter. Ctrl+C to quit.\n")

    counter = 0
    while True:
        try:
            text = input(">> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not text:
            continue

        result = pipeline.analyze(text)
        print(f"  Normalized : {result['normalized']}")
        print(f"  IPA        : {result['ipa']}")
        print(f"  Stressed   : {result['stressed_ipa']}")
        print(f"  Type       : {result['sentence_type']}")

        if espeak_available():
            counter += 1
            out = Path(f"interactive_{counter:03d}.wav")
            pipeline.synthesize(text, output=out)
            print(f"  Audio      : {out.resolve()}")
        print()


def run_analyze(pipeline: AzTTSPipeline, text: str) -> None:
    """Print detailed analysis to stdout as JSON."""
    result = pipeline.analyze(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    cfg = PipelineConfig(
        speaking_style=args.style,
        speaker_gender=args.gender,
        speed=args.speed,
    )
    pipeline = AzTTSPipeline(config=cfg)

    if args.demo:
        synthesize = espeak_available() and not args.analyze
        run_demo(pipeline, synthesize=synthesize)
        return 0

    if args.interactive:
        run_interactive(pipeline)
        return 0

    text = " ".join(args.text).strip() if args.text else ""
    if not text:
        parser.print_help()
        return 1

    if args.analyze:
        run_analyze(pipeline, text)
        return 0

    # Default: synthesize
    output = Path(args.output) if args.output else Path("output.wav")
    if espeak_available():
        pipeline.synthesize(text, output=output)
        print(f"Output: {output.resolve()}")
    else:
        print("WARNING: espeak-ng not installed. Running analysis only.\n")
        run_analyze(pipeline, text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
