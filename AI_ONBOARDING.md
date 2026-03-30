# AI Agent Onboarding — Azerbaijani TTS Dissertation Project

> **READ THIS FILE FIRST** at the start of every conversation.
> **UPDATE THIS FILE** whenever meaningful new work is completed, files are added,
> decisions are made, or the project state changes. Keep it as the single source
> of truth for any AI agent joining this project.

---

## 1. What This Project Is

A **Master's dissertation** (UNEC MBA — AI specialization) that designs and
implements a **rule-based Text-to-Speech (TTS) system for the North Azerbaijani
language**, then documents it in full academic dissertation format.

The project has **two parallel tracks**:
- **Technical track** — a working Python TTS pipeline
- **Academic track** — a full MBA dissertation written in **English**

The dissertation advisor provided a required structure. All writing must follow
it exactly and be in **English**. Code and technical files are also in **English**.

---

## 2. Repository Structure

```
/
├── AI_ONBOARDING.md          ← YOU ARE HERE — read every session, update when needed
├── README.md                 ← Public-facing project overview
│
├── 00_Planning/
│   ├── ROADMAP.md            ← Phase-based plan with completion status
│   ├── OUTLINE.md            ← Dissertation structure progress tracker
│   └── DEADLINES.md
│
├── 01_Research/
│   ├── REFERENCES.md         ← 40+ APA 7 citations with URLs — use these
│   ├── Documents/
│   │   ├── Diplom example (Tunzale).docx   ← Style/format reference
│   │   ├── Yusif Aghalarli Thesis Final.pdf ← Another TTS thesis (ADA Uni)
│   │   ├── AZERBAIJAN TEXT-TO-SPEECH SYNTHESIS SYSTEM.pdf  ← Aida-Zade 2010
│   │   └── Design and Development of a Rule-Based TTS System...docx
│   ├── Images/
│   └── Notes/
│       └── NOTES.md          ← Known gaps and issues to address
│
├── 02_Technical/
│   └── Code/
│       ├── main.py           ← CLI entry point
│       ├── pipeline.py       ← Orchestrator (AzTTSPipeline)
│       ├── text_normalizer.py
│       ├── g2p_converter.py
│       ├── stress_assigner.py
│       ├── prosody_engine.py
│       ├── synthesizer.py    ← espeak-ng wrapper
│       ├── utils.py
│       ├── requirements.txt
│       ├── pytest.ini
│       ├── Rules/
│       │   ├── g2p_rules.json
│       │   ├── stress_rules.json
│       │   ├── prosody_rules.json
│       │   └── text_norm_rules.json
│       ├── tests/            ← pytest suite — 156 tests, all passing
│       │   ├── test_g2p_converter.py
│       │   ├── test_text_normalizer.py
│       │   ├── test_stress_assigner.py
│       │   ├── test_prosody_engine.py
│       │   ├── test_pipeline.py
│       │   ├── test_utils.py
│       │   └── conftest.py
│       └── evaluation/       ← Automated evaluation framework
│           ├── run_evaluation.py
│           ├── test_sentences.json   ← 50 phonetically balanced sentences
│           ├── report.json           ← Latest evaluation run output
│           ├── results_summary.json  ← MOS + WER final results
│           ├── mos_scores.json       ← Per-evaluator MOS data
│           ├── wer_transcriptions.json
│           └── analyze_results.py
│
├── 03_Dissertation/          ← Source chapter files (English, detailed)
│   ├── Abstract.md
│   ├── Introduction.md
│   ├── Chapter_1.md          ← TTS overview, rule-based theory
│   ├── Chapter_2.md          ← Azerbaijani phonetics + system architecture
│   ├── Chapter_3.md          ← Implementation + evaluation results
│   └── References.md
│
├── 04_Archive/               ← Deprecated materials, ignore
│
└── 05_Result/
    ├── result.txt            ← MAIN DISSERTATION FILE (plain text, English) ← ACTIVE
    └── TTS Dissertation.docx ← Final formatted Word document (work in progress)
```

---

## 3. The Dissertation Structure (Advisor-Required)

All content in `05_Result/result.txt` must follow this exact structure in **English**:

```
ABSTRACT
  - Research objectives
  - Methodological approach
  - Key findings and contributions

INTRODUCTION
  - Relevance and motivation of the research
  - Importance of TTS for low-resource languages
  - Rationale for selecting a rule-based approach
  - Research aim and objectives
  - Research object and subject
  - Scientific novelty and practical significance
  - Structure of the thesis

CHAPTER I. Theoretical Foundations of Text-to-Speech Systems
  1.1 General Overview of Text-to-Speech Systems
      - Definition and purpose of TTS technology
      - Core components of TTS systems
      - Historical development of TTS technologies
  1.2 Rule-Based Text-to-Speech Systems
      - Concept and principles of rule-based TTS
      - Linguistic rule formulation and phonetic modeling
      - Comparison with statistical and neural TTS approaches
  1.3 Advantages and Limitations of Rule-Based TTS: A SWOT Analysis
      - Strengths: transparency, linguistic control, low data dependency
      - Weaknesses: limited naturalness, scalability challenges
      - Opportunities and threats in the context of Azerbaijani

CHAPTER II. Linguistic and Technical Analysis for Azerbaijani TTS
  2.1 Phonetic and Morphological Characteristics of Azerbaijani
      - Phoneme inventory and sound structure
      - Vowel harmony and consonant behavior
      - Impact of agglutinative morphology on speech synthesis
  2.2 Text Normalization and Linguistic Rule Design
      - Normalization of numbers, abbreviations, dates, symbols
      - Syllabification and stress assignment rules
      - Prosodic and intonation modeling
  2.3 Architecture of the Rule-Based Azerbaijani TTS System
      - Overall system architecture
      - Module decomposition
      - Data flow and rule execution logic

CHAPTER III. Design, Implementation, and Evaluation
  3.1 System Design and Development Methodology
      - Software engineering approach
      - Justification for Python-based implementation
      - Tools, libraries, and development environment
  3.2 Implementation of the Rule-Based TTS Prototype
      - Rule engine development
      - Phoneme mapping and pronunciation generation
      - Audio signal generation and output processing
  3.3 Experimental Evaluation and Performance Analysis
      - Testing scenarios and datasets
      - Speech intelligibility and quality evaluation metrics
      - Comparative analysis with existing TTS solutions

CONCLUSION
  - Summary of research findings
  - Scientific and practical contributions
  - Limitations of the proposed system
  - Directions for future research (hybrid and neural TTS integration)
```

---

## 4. Current Project Status (as of 2026-03-30)

### Phase completion (from ROADMAP.md):
- [x] Phase 1 — Foundation (Nov–Dec 2025): research, literature review, architecture
- [x] Phase 2 — Research & Design (Jan–Feb 2026): phonetics, G2P rules, prosody
- [x] Phase 3 — Implementation (Feb–Mar 2026): all 5 pipeline modules built
- [x] Phase 4 — Evaluation & Writing (Mar–Apr 2026): tests, MOS/WER, results
- [ ] Phase 5 — Finalization (Apr–May 2026): advisor review, UNEC formatting, slides

### What is DONE:
- Full Python TTS pipeline (5 modules, ~2,438 lines of code)
- 4 JSON rule bases (G2P, stress, prosody, text normalization)
- **pytest suite: 156 tests, all passing** (added in latest merge)
- **Evaluation framework: 50 test sentences, automated runner** (added in latest merge)
- MOS evaluation: 5 native speakers, 180 ratings → **MOS = 3.2** (CI: [3.1, 3.3])
- Baseline MOS (espeak-ng raw): **2.8** — our system is +0.4 better
- WER evaluation: **12.4%** (baseline: 18.7%)
- Sentence type detection: **100% accuracy** on 50 test sentences
- Pipeline avg analysis time: **0.3 ms** per sentence
- 61 unique linguistic phenomena covered in test set
- `05_Result/result.txt` — **Chapter I fully written** in English with all citations
- `05_Result/result.txt` — **Chapter II fully written** in English with all citations
- `03_Dissertation/` — Chapters 1–3 written in detailed English (use as source material)

### What is STILL TODO:
- `05_Result/result.txt` — **Chapter III not yet written** (placeholder only)
- `05_Result/result.txt` — **Chapter III not yet written** (placeholder only)
- `05_Result/result.txt` — **Abstract not yet written** (placeholder only)

- `05_Result/result.txt` — **Introduction not yet written** (placeholder only)
- `05_Result/result.txt` — **Conclusion not yet written** (placeholder only)
- Introduction missing sections: "Research aim and objectives", "Research object
  and subject", "Scientific novelty and practical significance"
- Chapter I: SWOT Opportunities and Threats section must be present
- Chapter III: comparative analysis with other Azerbaijani TTS systems needs
  expansion (Rustamov, IS2AI, Aida-Zade 2010)
- `05_Result/TTS Dissertation.docx` — final formatted document (pending)
- Phase 5: advisor review, UNEC formatting, presentation slides

---

## 5. Key Technical Facts (use these numbers in writing)

| Metric | Our System | Baseline (espeak-ng raw) |
|---|---|---|
| MOS (naturalness) | **3.2** (CI: [3.1, 3.3]) | 2.8 (CI: [2.7, 2.9]) |
| WER (intelligibility) | **12.4%** (±3.8%) | 18.7% (±5.2%) |
| Phoneme Error Rate (PER) | **5.2%** (native vocab: 2.8%) | — |
| Sentence type detection | **100%** (50/50) | — |
| Avg pipeline analysis time | **0.3 ms** | — |
| Test suite | **156 tests, all passing** | — |
| Phenomena covered | **61 unique phenomena** | — |
| Neural reference (Tacotron2+HiFiGAN Turkish) | — | MOS 4.5 |

### Text normalization accuracy (100 sentences):
| Category | Accuracy |
|---|---|
| Cardinal numbers | 97.8% (44/45) |
| Ordinal numbers | 94.4% (17/18) |
| Dates (DD.MM.YYYY) | 100% |
| Times (HH:MM) | 100% |
| Abbreviations | 91.3% (21/23) |
| Currency symbols | 100% |
| Roman numerals | 100% |

### G2P error breakdown:
- ğ allophony: 42% of errors
- Palatalization boundary: 31%
- Loanword pronunciations: 27%

---

## 6. The Pipeline (Technical Summary)

```
Raw Text
  → text_normalizer.py    Numbers, dates, abbreviations, symbols → words
  → g2p_converter.py      Graphemes → IPA phonemes (9 vowels, 23 consonants)
  → stress_assigner.py    Lexical + phrasal stress (default: final syllable)
  → prosody_engine.py     Pitch accents, durations, pauses (ToBI-lite)
  → synthesizer.py        espeak-ng subprocess → WAV bytes
  → WAV output
```

Key linguistic rules implemented:
- G2P: palatalization of /k/ /g/ before front vowels, /ğ/ allophony
  (intervocalic → /ɣ/, word-final → /ː/), nasal assimilation, final devoicing
- Stress: final syllable default; exceptions for clitics, *deyil*, negation -ma/-mə
- Prosody: ToBI-style H*, L+H*, L%, H% by sentence type
- Normalization: vowel harmony-aware ordinal suffix selection

---

## 7. Important Conventions

### Language rules:
- **ALL dissertation writing** (`05_Result/result.txt`) is in **ENGLISH**
- All code, comments, filenames, and technical docs are in **English**
- References use **APA 7** format throughout
- Citations must include URLs

### result.txt rules:
- The file lives at `05_Result/result.txt` — this is the **only master dissertation file**
- It is plain text now; will become `05_Result/TTS Dissertation.docx` at the end
- Chapters are written section by section; the rest remain as `[placeholder]`
- When writing a chapter, use `03_Dissertation/` files as source material and expand
- Include `[Figure X.Y: description]` and `[Table X.Y: description]` placeholders
  with source references for all figures and tables

### Memory files location:
- `/Users/basirovulvi/.claude/projects/-Users-basirovulvi-Desktop-TTS-system-for-Azerbaijani-language/memory/`
- Check `MEMORY.md` there for any additional saved context

---

## 8. Key Source Files to Read for Context

When working on dissertation content, read these in order:

1. `01_Research/REFERENCES.md` — all 40+ citations with URLs
2. `03_Dissertation/Chapter_1.md` — detailed English source for Chapter I
3. `03_Dissertation/Chapter_2.md` — detailed English source for Chapter II
4. `03_Dissertation/Chapter_3.md` — detailed English source for Chapter III
5. `02_Technical/Code/evaluation/results_summary.json` — real evaluation numbers
6. `02_Technical/Code/evaluation/report.json` — full test run details
7. `01_Research/Notes/NOTES.md` — known gaps and issues

---

## 9. How to Update This File

Update `AI_ONBOARDING.md` whenever:
- A new chapter or section is written in `result.txt`
- New code, tests, or evaluation results are added
- The project status changes (tasks completed, new tasks discovered)
- A decision is made that affects future work
- A new file or folder is added to the repository

When updating:
- Change the status in Section 4 (mark done items, add new todo items)
- Update Section 5 if evaluation numbers change
- Add new files to Section 2 if the structure changes
- Keep Section 4 "Current Status" date accurate

---

## 10. Collaborators

- **Student/Owner**: ulvibashir (GitHub)
- **University**: UNEC — Azerbaijan State Economic University, MBA in Artificial Intelligence
- **Dissertation type**: Master's Dissertation, target length 51–75 pages
- **Citation style**: APA 7
- **Mentor**: Khanim Pashayeva (pashayeva-khanim@outlook.com)
- **Repository**: https://github.com/ulvibashir/TTS-system-for-Azerbaijani-language
- **Branch workflow**: feature branches → PRs → main

---

## 11. Quick Commands

```bash
# Run full test suite
cd 02_Technical/Code && python -m pytest tests/ -v

# Run demo synthesis (requires espeak-ng)
cd 02_Technical/Code && python -X utf8 main.py --demo

# Run evaluation
cd 02_Technical/Code && python evaluation/run_evaluation.py

# Analyze a sentence (no audio needed)
cd 02_Technical/Code && python -X utf8 main.py --analyze "Azərbaycan gözəl ölkədir."

# Synthesize to WAV
cd 02_Technical/Code && python -X utf8 main.py "Salam dünya." --output out.wav
```

---

*Last updated: 2026-03-30 — result.txt moved to 05_Result/result.txt. Dissertation
language confirmed as English. Mentor: Khanim Pashayeva. Evaluation framework and
pytest suite (156 tests) added. Chapter I and Chapter II fully written in English
in result.txt. Chapters III, Abstract, Introduction, and Conclusion still as
placeholders.*
