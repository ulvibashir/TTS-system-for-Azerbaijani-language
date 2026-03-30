"""
Evaluation Runner for Azerbaijani TTS System

Runs the 50 phonetically balanced test sentences through the pipeline
and generates evaluation reports:
  - Text normalization accuracy
  - G2P conversion output (for manual verification)
  - Sentence type detection accuracy
  - Pipeline analysis for each sentence
  - Summary statistics

Usage:
    python run_evaluation.py                # Full evaluation report
    python run_evaluation.py --output report.json   # Save to JSON
    python run_evaluation.py --synthesize   # Also generate WAV files (requires espeak-ng)
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add Code directory to path
CODE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE_DIR))

from pipeline import AzTTSPipeline, PipelineConfig
from synthesizer import espeak_available
from utils import word_error_rate, character_error_rate


SENTENCES_PATH = Path(__file__).parent / "test_sentences.json"


def load_test_sentences():
    with open(SENTENCES_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data["sentences"]


def run_analysis_evaluation(pipeline, sentences):
    """Run all sentences through analysis and collect results."""
    results = []
    type_correct = 0
    type_total = 0
    errors = []

    for sent in sentences:
        sid = sent["id"]
        text = sent["text"]
        expected_type = sent["expected_type"]

        start = time.perf_counter()
        try:
            analysis = pipeline.analyze(text)
            elapsed = time.perf_counter() - start

            detected_type = analysis["sentence_type"]
            type_match = detected_type == expected_type
            type_total += 1
            if type_match:
                type_correct += 1

            results.append({
                "id": sid,
                "input": text,
                "normalized": analysis["normalized"],
                "ipa": analysis["ipa"],
                "stressed_ipa": analysis["stressed_ipa"],
                "sentence_type_expected": expected_type,
                "sentence_type_detected": detected_type,
                "sentence_type_match": type_match,
                "phenomena": sent["phenomena"],
                "processing_time_ms": round(elapsed * 1000, 1),
                "status": "ok",
            })
        except Exception as e:
            errors.append({"id": sid, "text": text, "error": str(e)})
            results.append({
                "id": sid,
                "input": text,
                "status": "error",
                "error": str(e),
            })

    return results, type_correct, type_total, errors


def run_synthesis_evaluation(pipeline, sentences, output_dir):
    """Synthesize all sentences to WAV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    synth_results = []

    for sent in sentences:
        sid = sent["id"]
        text = sent["text"]
        wav_path = output_dir / f"sentence_{sid:02d}.wav"

        start = time.perf_counter()
        try:
            wav_bytes = pipeline.synthesize(text, output=wav_path)
            elapsed = time.perf_counter() - start
            synth_results.append({
                "id": sid,
                "wav_path": str(wav_path),
                "wav_size_bytes": len(wav_bytes),
                "synthesis_time_ms": round(elapsed * 1000, 1),
                "status": "ok",
            })
        except Exception as e:
            synth_results.append({
                "id": sid,
                "status": "error",
                "error": str(e),
            })

    return synth_results


def generate_report(analysis_results, type_correct, type_total, errors,
                    synth_results=None):
    """Generate a summary evaluation report."""
    ok_results = [r for r in analysis_results if r["status"] == "ok"]
    avg_time = (sum(r["processing_time_ms"] for r in ok_results) / len(ok_results)
                if ok_results else 0)

    # Count phenomena coverage
    all_phenomena = set()
    for r in ok_results:
        all_phenomena.update(r.get("phenomena", []))

    report = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "total_sentences": len(analysis_results),
            "successful_analyses": len(ok_results),
            "errors": len(errors),
            "espeak_available": espeak_available(),
        },
        "sentence_type_detection": {
            "correct": type_correct,
            "total": type_total,
            "accuracy_pct": round(type_correct / type_total * 100, 1) if type_total else 0,
        },
        "performance": {
            "avg_analysis_time_ms": round(avg_time, 1),
            "min_time_ms": round(min(r["processing_time_ms"] for r in ok_results), 1) if ok_results else 0,
            "max_time_ms": round(max(r["processing_time_ms"] for r in ok_results), 1) if ok_results else 0,
        },
        "phenomena_coverage": {
            "unique_phenomena_tested": len(all_phenomena),
            "phenomena_list": sorted(all_phenomena),
        },
        "detailed_results": analysis_results,
    }

    if errors:
        report["errors"] = errors

    if synth_results:
        ok_synth = [r for r in synth_results if r["status"] == "ok"]
        report["synthesis"] = {
            "total": len(synth_results),
            "successful": len(ok_synth),
            "avg_synthesis_time_ms": round(
                sum(r["synthesis_time_ms"] for r in ok_synth) / len(ok_synth), 1
            ) if ok_synth else 0,
            "details": synth_results,
        }

    return report


def print_summary(report):
    """Print a human-readable summary to stdout."""
    meta = report["metadata"]
    stype = report["sentence_type_detection"]
    perf = report["performance"]
    phenom = report["phenomena_coverage"]

    print("=" * 65)
    print("  Azerbaijani TTS System — Evaluation Report")
    print("=" * 65)
    print(f"\n  Date: {meta['timestamp']}")
    print(f"  Sentences: {meta['total_sentences']}")
    print(f"  Successful: {meta['successful_analyses']}")
    print(f"  Errors: {meta['errors']}")
    print(f"  espeak-ng: {'available' if meta['espeak_available'] else 'NOT available'}")

    print(f"\n--- Sentence Type Detection ---")
    print(f"  Accuracy: {stype['accuracy_pct']}% ({stype['correct']}/{stype['total']})")

    print(f"\n--- Performance ---")
    print(f"  Avg analysis time: {perf['avg_analysis_time_ms']} ms")
    print(f"  Min: {perf['min_time_ms']} ms  |  Max: {perf['max_time_ms']} ms")

    print(f"\n--- Phenomena Coverage ---")
    print(f"  Unique phenomena: {phenom['unique_phenomena_tested']}")

    if "synthesis" in report:
        synth = report["synthesis"]
        print(f"\n--- Synthesis ---")
        print(f"  Synthesized: {synth['successful']}/{synth['total']}")
        print(f"  Avg synthesis time: {synth['avg_synthesis_time_ms']} ms")

    # Print mismatches
    mismatches = [r for r in report["detailed_results"]
                  if r.get("status") == "ok" and not r.get("sentence_type_match", True)]
    if mismatches:
        print(f"\n--- Sentence Type Mismatches ({len(mismatches)}) ---")
        for m in mismatches:
            print(f"  [{m['id']:02d}] expected={m['sentence_type_expected']}, "
                  f"got={m['sentence_type_detected']}")
            print(f"       {m['input']}")

    # Print errors
    if report.get("errors"):
        print(f"\n--- Errors ---")
        for e in report["errors"]:
            print(f"  [{e['id']:02d}] {e['error']}")
            print(f"       {e['text']}")

    print("\n" + "=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Azerbaijani TTS Evaluation Runner")
    parser.add_argument("--output", "-o", help="Save report to JSON file")
    parser.add_argument("--synthesize", action="store_true",
                        help="Generate WAV files (requires espeak-ng)")
    parser.add_argument("--wav-dir", default="evaluation_output",
                        help="Directory for WAV files (default: evaluation_output)")
    parser.add_argument("--style", default="neutral",
                        choices=["neutral", "formal", "conversational"])
    parser.add_argument("--gender", default="male", choices=["male", "female"])
    args = parser.parse_args()

    sentences = load_test_sentences()
    print(f"Loaded {len(sentences)} test sentences.\n")

    cfg = PipelineConfig(speaking_style=args.style, speaker_gender=args.gender)
    pipeline = AzTTSPipeline(config=cfg)

    # Analysis evaluation
    print("Running analysis evaluation...")
    analysis_results, type_correct, type_total, errors = \
        run_analysis_evaluation(pipeline, sentences)

    # Synthesis evaluation (optional)
    synth_results = None
    if args.synthesize:
        if espeak_available():
            print("Running synthesis evaluation...")
            synth_results = run_synthesis_evaluation(pipeline, sentences, args.wav_dir)
        else:
            print("WARNING: espeak-ng not available, skipping synthesis.")

    # Generate and display report
    report = generate_report(analysis_results, type_correct, type_total,
                             errors, synth_results)
    print_summary(report)

    # Save to file
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\nReport saved to: {output_path.resolve()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
