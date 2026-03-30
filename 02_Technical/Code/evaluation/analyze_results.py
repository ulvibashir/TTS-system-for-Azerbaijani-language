"""
Evaluation Analysis Script — Computes MOS and WER statistics from collected data.

Reads:
  - mos_scores.json      (MOS ratings from 5 evaluators)
  - wer_transcriptions.json  (Transcriptions from 5 listeners)

Outputs:
  - Summary statistics matching dissertation Chapter 3 tables
  - Per-sentence breakdown
  - Per-evaluator breakdown

Usage:
    python analyze_results.py
    python analyze_results.py --output results_summary.json
"""

import sys
import os
import json
import math
import argparse
from pathlib import Path
from collections import defaultdict

# Fix Windows console encoding for Azerbaijani characters
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CODE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE_DIR))

from utils import word_error_rate

DATA_DIR = Path(__file__).parent


def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# MOS Analysis
# ---------------------------------------------------------------------------

def analyze_mos():
    """Compute MOS statistics from mos_scores.json."""
    data = load_json("mos_scores.json")
    evaluators = ["E1", "E2", "E3", "E4", "E5"]
    results = {}

    for condition in ["proposed", "baseline"]:
        all_scores = []
        per_evaluator = defaultdict(list)
        per_sentence = defaultdict(list)

        for entry in data["scores"][condition]:
            sid = entry["sentence_id"]
            for ev in evaluators:
                if ev in entry:
                    score = entry[ev]
                    all_scores.append(score)
                    per_evaluator[ev].append(score)
                    per_sentence[sid].append(score)

        n = len(all_scores)
        mean = sum(all_scores) / n if n else 0
        variance = sum((s - mean) ** 2 for s in all_scores) / n if n else 0
        std = math.sqrt(variance)

        # 95% CI: mean ± 1.96 * (std / sqrt(n))
        ci_half = 1.96 * (std / math.sqrt(n)) if n else 0
        ci_low = round(mean - ci_half, 1)
        ci_high = round(mean + ci_half, 1)

        # Per-evaluator means
        ev_means = {}
        for ev in evaluators:
            scores = per_evaluator[ev]
            ev_means[ev] = round(sum(scores) / len(scores), 2) if scores else 0

        # Per-sentence means
        sent_means = {}
        for sid, scores in per_sentence.items():
            sent_means[sid] = round(sum(scores) / len(scores), 2)

        results[condition] = {
            "n_ratings": n,
            "mean": round(mean, 1),
            "std": round(std, 1),
            "ci_95": [ci_low, ci_high],
            "per_evaluator": ev_means,
            "per_sentence": sent_means,
            "score_distribution": {
                str(s): all_scores.count(s) for s in range(1, 6)
            },
        }

    return results


# ---------------------------------------------------------------------------
# WER Analysis
# ---------------------------------------------------------------------------

def analyze_wer():
    """Compute WER statistics from wer_transcriptions.json."""
    data = load_json("wer_transcriptions.json")
    listeners = ["L1", "L2", "L3", "L4", "L5"]

    all_wers = []
    per_listener = defaultdict(list)
    per_sentence = defaultdict(list)
    error_sentences = []

    for entry in data["transcriptions"]:
        sid = entry["id"]
        ref = entry["reference"]

        for lis in listeners:
            if lis in entry:
                hyp = entry[lis]
                wer = word_error_rate(ref, hyp)
                all_wers.append(wer)
                per_listener[lis].append(wer)
                per_sentence[sid].append(wer)

                if wer > 0:
                    error_sentences.append({
                        "sentence_id": sid,
                        "listener": lis,
                        "reference": ref,
                        "hypothesis": hyp,
                        "wer": round(wer * 100, 1),
                    })

    n = len(all_wers)
    mean_wer = sum(all_wers) / n if n else 0
    variance = sum((w - mean_wer) ** 2 for w in all_wers) / n if n else 0
    std = math.sqrt(variance)

    # Per-listener means
    lis_means = {}
    for lis in listeners:
        wers = per_listener[lis]
        lis_means[lis] = round(sum(wers) / len(wers) * 100, 1) if wers else 0

    # Per-sentence means
    sent_means = {}
    for sid, wers in per_sentence.items():
        sent_means[sid] = round(sum(wers) / len(wers) * 100, 1)

    # Sentences with zero errors
    perfect_sents = [sid for sid, m in sent_means.items() if m == 0]

    return {
        "n_evaluations": n,
        "mean_wer_pct": round(mean_wer * 100, 1),
        "std_pct": round(std * 100, 1),
        "per_listener": lis_means,
        "per_sentence": sent_means,
        "perfect_sentences": len(perfect_sents),
        "sentences_with_errors": len(sent_means) - len(perfect_sents),
        "errors": error_sentences,
    }


# ---------------------------------------------------------------------------
# Print Report
# ---------------------------------------------------------------------------

def print_report(mos, wer):
    print("=" * 65)
    print("  Azerbaijani TTS — Evaluation Results Summary")
    print("=" * 65)

    print("\n--- MOS Results (Naturalness) ---")
    print(f"{'Condition':<35} {'Mean MOS':>10} {'Std':>8} {'95% CI':>15}")
    print("-" * 70)
    for cond in ["proposed", "baseline"]:
        r = mos[cond]
        ci = f"[{r['ci_95'][0]}, {r['ci_95'][1]}]"
        label = "Proposed system" if cond == "proposed" else "espeak-ng baseline"
        print(f"{label:<35} {r['mean']:>10.1f} {r['std']:>8.1f} {ci:>15}")

    print(f"\n  MOS improvement: delta = {mos['proposed']['mean'] - mos['baseline']['mean']:.1f}")

    print(f"\n  Per-evaluator MOS (proposed):")
    for ev, m in mos["proposed"]["per_evaluator"].items():
        print(f"    {ev}: {m:.2f}")

    print(f"\n  Score distribution (proposed): {mos['proposed']['score_distribution']}")

    print("\n--- WER Results (Intelligibility) ---")
    print(f"  Mean WER: {wer['mean_wer_pct']:.1f}%  (std: {wer['std_pct']:.1f}%)")
    print(f"  Total evaluations: {wer['n_evaluations']}")
    print(f"  Perfect sentences (0% WER): {wer['perfect_sentences']}/50")
    print(f"  Sentences with errors: {wer['sentences_with_errors']}/50")

    print(f"\n  Per-listener WER:")
    for lis, m in wer["per_listener"].items():
        print(f"    {lis}: {m:.1f}%")

    if wer["errors"]:
        print(f"\n  Error details ({len(wer['errors'])} transcription errors):")
        for err in wer["errors"][:15]:
            print(f"    [{err['sentence_id']:02d}] {err['listener']}: "
                  f"WER={err['wer']:.1f}%")
            print(f"         ref: {err['reference']}")
            print(f"         hyp: {err['hypothesis']}")

    print("\n" + "=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Analyze MOS and WER evaluation data")
    parser.add_argument("--output", "-o", help="Save results to JSON")
    args = parser.parse_args()

    mos = analyze_mos()
    wer = analyze_wer()

    print_report(mos, wer)

    if args.output:
        results = {"mos": mos, "wer": wer}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
