"""
Generate Figure 14: Bar chart comparing proposed system MOS vs espeak-ng baseline
per sentence, ordered by sentence ID.

Run from the Code directory:
    python3 evaluation/plot_mos_chart.py
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

data_path = Path(__file__).parent / "results_summary.json"
with open(data_path, encoding="utf-8") as f:
    data = json.load(f)

proposed = data["mos"]["proposed"]["per_sentence"]
baseline = data["mos"]["baseline"]["per_sentence"]

# Sort by sentence ID (numeric)
ids = sorted(proposed.keys(), key=int)
x = np.arange(len(ids))
prop_vals = [proposed[i] for i in ids]
base_vals = [baseline[i] for i in ids]

width = 0.4

fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(x - width / 2, base_vals, width, label="espeak-ng baseline", color="#b0c4de")
ax.bar(x + width / 2, prop_vals, width, label="Proposed system", color="#2e6fad")

ax.set_xlabel("Sentence ID", fontsize=11)
ax.set_ylabel("Mean Opinion Score (MOS)", fontsize=11)
ax.set_title(
    "Figure 14: Per-sentence MOS — Proposed System vs espeak-ng Baseline",
    fontsize=12,
    fontweight="bold",
)
ax.set_xticks(x)
ax.set_xticklabels(ids, fontsize=8)
ax.set_ylim(1, 5)
ax.axhline(y=3, color="gray", linestyle="--", linewidth=0.8, alpha=0.6, label="MOS 3 (Fair)")
ax.legend(fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
out = Path(__file__).parent / "figure14_mos_per_sentence.png"
plt.savefig(out, dpi=300)
print(f"Saved: {out}")
plt.show()
