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
├── 03_Dissertation/          ← ONE .txt FILE PER SECTION — edit these, paste into Word
│   ├── References.md         ← Master reference list (APA 7)
│   ├── Chapter_1/
│   │   ├── result-1.1.txt        ← DONE
│   │   ├── result-1.2.txt        ← DONE
│   │   └── result-1.3.txt        ← DONE (+ Ch1 references)
│   ├── Chapter_2/
│   │   ├── result-2.1.txt        ← DONE
│   │   ├── result-2.2.txt        ← DONE
│   │   └── result-2.3.txt        ← DONE (+ Ch2 references)
│   └── Chapter_3/
│       ├── result-3.1.txt        ← [placeholder]
│       ├── result-3.2.txt        ← [placeholder]
│       └── result-3.3.txt        ← [placeholder]
│
├── 04_Archive/               ← Deprecated materials, ignore
│
└── 05_Result/                ← Front matter and conclusion files
    ├── TTS-Dissertation.docx     ← User's Word file (do not edit)
    ├── result-abstract.txt       ← DONE
    ├── result-introduction.txt   ← DONE
    └── result-conclusion.txt     ← [placeholder]
```

---

## 3. The Dissertation Structure (Advisor-Required)

All dissertation content lives in `03_Dissertation/` chapter folders and `05_Result/` front-matter files, and must follow this exact structure in **English**:

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

## 4. Current Project Status (as of 2026-04-03)

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
- `03_Dissertation/Chapter_1/` — **All three sections fully written and revised** (1.1, 1.2, 1.3 + references)
  - All 10 subsections meet the 2-page minimum (≥550 words each)
  - 1.3.1 citations added to all strength items (S1–S6)
  - 1.3.2 cleaned: weaknesses now describe internal limitations only (O/T framing removed)
  - New citations added: Allen et al. (1987), Chomsky & Halle (1968)
- `03_Dissertation/Chapter_2/` — **All three sections fully written** (2.1, 2.2, 2.3 + references)
- `05_Result/result-abstract.txt` — **DONE** (soft-wrapped, cited, full content)
- `05_Result/result-introduction.txt` — **DONE** (soft-wrapped, all 7 advisor-required sections)

### What is STILL TODO:
- `03_Dissertation/Chapter_3/` — **Chapter III not yet written** (all three sections placeholder)
- `05_Result/result-conclusion.txt` — **not yet written** (placeholder)
- Chapter III: comparative analysis with other Azerbaijani TTS systems needs
  expansion (Rustamov, IS2AI, Aida-Zade 2010)
- `03_Dissertation/Chapter_1/` and `03_Dissertation/Chapter_2/` txt files — **hard-wrapped at 72 chars** (pending reformat to soft-wrap)
  - When pasted into Word, each line break becomes a visible line break → paragraphs break into short lines
  - Fix: rewrite paragraph text as single long lines; only use newlines for blank lines, headings, bullets, table rows
  - `result-abstract.txt` and `result-introduction.txt` are already soft-wrapped correctly
- Chapter III: comparative analysis with other Azerbaijani TTS systems needs expansion (Rustamov, IS2AI, Aida-Zade 2010)
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
- **ALL dissertation writing** (`05_Result/` section files) is in **ENGLISH**
- All code, comments, filenames, and technical docs are in **English**
- References use **APA 7** format throughout
- Citations must include URLs

### Dissertation writing workflow:
- **AI writes content into section `.txt` files** in `03_Dissertation/` (chapters) and `05_Result/` (front matter + conclusion)
- **User pastes the text into Word manually**, applying formatting and adding images
- Each section is a separate file — one file per section (e.g. `result-2.1.txt`)
- Unwritten sections contain `[placeholder]` markers
- When writing a section, read the matching `03_Dissertation/` chapter file as source
- Include `[Figure X.Y: description]` and `[Table X.Y: description]` markers
  with `[Source: ...]` lines so the user knows where to insert images/tables in Word
- References go at the end of the last section file of each chapter

### CRITICAL — txt file formatting (soft-wrap):
- **Paragraphs must be written as a single long unbroken line** — no manual line
  breaks inside a paragraph. Word wraps lines visually; a newline in the txt file
  becomes a visible line break when pasted into Word.
- Only use actual newlines for: blank lines between paragraphs, heading lines,
  bullet/list items, table rows, and figure/source caption lines.
- DO NOT hard-wrap at 72 characters (old habit — causes broken lines in Word).

### Mentor feedback (Khanim Pashayeva) — active rules:
- **Every subsection must be a minimum of 2 pages** (~550+ words). Check word
  count before finalising any section.
- **All paragraphs must have citations** — no uncited factual claims.
- **SWOT sections must be strictly categorised**: Strengths/Weaknesses describe
  internal system properties only; Opportunities/Threats describe external
  environmental factors only. Do not mix framing across categories.

### Memory files location:
- `/Users/basirovulvi/.claude/projects/-Users-basirovulvi-Desktop-TTS-system-for-Azerbaijani-language/memory/`
- Check `MEMORY.md` there for any additional saved context

---

## 8. Key Source Files to Read for Context

When working on dissertation content, read these in order:

1. `01_Research/REFERENCES.md` — all 40+ citations with URLs
2. `03_Dissertation/References.md` — master APA 7 reference list
3. `02_Technical/Code/evaluation/results_summary.json` — real evaluation numbers
4. `02_Technical/Code/evaluation/report.json` — full test run details
5. `01_Research/Notes/NOTES.md` — known gaps and issues
6. Existing completed sections (e.g. `03_Dissertation/Chapter_1/result-1.3.txt`) for style and citation conventions

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
# === TECHNICAL ===

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

*Last updated: 2026-04-03 — File restructure completed: chapter folders moved from 05_Result/ to 03_Dissertation/. Abstract.md, Introduction.md, Chapter_1.md, Chapter_2.md, Chapter_3.md deleted. result-abstract.txt and result-introduction.txt written in full (soft-wrapped, cited). Chapter I fully revised: all subsections ≥550 words, 1.3.1 citations added (S1–S6), 1.3.2 O/T framing removed. Chapter III still placeholder. Conclusion still placeholder.*
