# Design and Development of a Rule-Based TTS System for Azerbaijani Language

- **Institution:** Azerbaijan State Economic University (UNEC)
- **Program:** MBA in Artificial Intelligence
- **Type:** Master's Dissertation
- **Mentor:** Khanim Pashayeva (pashayeva-khanim@outlook.com)

---

## Overview

A fully rule-based text-to-speech synthesis pipeline for **North Azerbaijani** (Latin script). The system requires no speech training data and converts raw Azerbaijani text to spoken audio through five sequential modules.

### Pipeline

```mermaid
flowchart TD
    A([Raw Azerbaijani Text]) --> B

    B["<b>1. Text Normalization</b><br/><code>text_normalizer.py</code><br/>numbers · abbreviations · dates · symbols"]
    B --> C

    C["<b>2. G2P Conversion</b><br/><code>g2p_converter.py</code><br/>graphemes → IPA phonemes · syllabification"]
    C --> D

    D["<b>3. Stress Assignment</b><br/><code>stress_assigner.py</code><br/>lexical stress · phrasal stress · clitics"]
    D --> E

    E["<b>4. Prosody Engine</b><br/><code>prosody_engine.py</code><br/>pitch accents · durations · pauses · SSML"]
    E --> F

    F["<b>5. Synthesizer</b><br/><code>synthesizer.py</code><br/>espeak-ng backend"]
    F --> G([WAV Audio Output])

    style A fill:#e8f5e9,stroke:#388e3c
    style G fill:#e3f2fd,stroke:#1565c0
    style B fill:#fff8e1,stroke:#f9a825
    style C fill:#fff8e1,stroke:#f9a825
    style D fill:#fff8e1,stroke:#f9a825
    style E fill:#fff8e1,stroke:#f9a825
    style F fill:#fff8e1,stroke:#f9a825
```

---

## Live Demos

| Demo | Description | Link |
|------|-------------|------|
| **Rule-Based TTS** | Full pipeline — this dissertation's system (espeak-ng backend) | [tts-system-for-azerbaijani-language-1.onrender.com](https://tts-system-for-azerbaijani-language-1.onrender.com/) |
| **Azure Neural TTS** | Reference comparison — Microsoft Azure Cognitive Services (BanuNeural / BabekNeural) | [tts-system-for-azerbaijani-language.onrender.com](https://tts-system-for-azerbaijani-language.onrender.com/) |

> Both apps share the same UI. The rule-based demo runs the Python pipeline described in Chapter III. The Azure demo uses a cloud neural voice for perceptual comparison only.

---

## Key Results

| Metric | Proposed System | espeak-ng Baseline | Improvement |
|--------|:-:|:-:|:-:|
| **MOS** (naturalness, 1-5 scale) | **3.2** (std 0.5) | 2.8 (std 0.4) | +0.4 |
| **WER** (intelligibility) | **12.4%** (std 15.3%) | 18.7% (std 5.2%) | -6.3 pp |
| **G2P PER** (native vocabulary) | **2.8%** | — | — |
| **Sentence type detection** | **100%** (50/50) | — | — |
| **Text norm accuracy** | **97.5%** (118/121) | — | — |

> Evaluated on 50 phonetically balanced test sentences by 5 native Azerbaijani speakers.

---

## Linguistic Coverage

| Feature | Status | Details |
|---------|:------:|---------|
| 9-vowel system | done | a, e, ə, ı, i, o, ö, u, ü → IPA |
| Vowel harmony | done | Back/front suffix alternation |
| Palatalization (k/g) | done | /k/→/c/, /g/→/ɟ/ before front vowels |
| /ğ/ allophony | done | Intervocalic /ɣ/, word-final /ː/ |
| Final devoicing | done | b→p, d→t, z→s, g→k at word boundary |
| Nasal assimilation | done | /n/→/ŋ/ before velars, /n/→/m/ before bilabials |
| Geminate consonants | done | CC → Cː |
| Default final stress | done | With 8 exception categories |
| Sentence type detection | done | Declarative, YN-question, WH-question, exclamatory |
| Number-to-words | done | Cardinals, ordinals, vowel-harmony-correct suffixes |
| Date/time/abbreviation/currency | done | Full NSW normalization pipeline |

---

## Quick Start

**Requirements:** Python 3.10+ and [espeak-ng](https://github.com/espeak-ng/espeak-ng/releases)

```bash
# Install espeak-ng (Linux)
sudo apt install espeak-ng

cd 02_Technical/Code

# Run demo (10 test sentences covering key linguistic phenomena)
python -X utf8 main.py --demo

# Synthesize a sentence
python -X utf8 main.py "Azərbaycan gözəl ölkədir." --output out.wav

# Analyze pipeline stages without audio output
python -X utf8 main.py --analyze "Kitabı oxudunmu?"

# Interactive mode
python -X utf8 main.py --interactive
```

> On Windows, use `python -X utf8` to ensure correct Unicode handling in the terminal.

---

## Testing & Evaluation

```bash
cd 02_Technical/Code

# Run full test suite (156 tests)
pip install pytest
python -m pytest tests/ -v

# Run evaluation on 50 phonetically balanced sentences
python evaluation/run_evaluation.py

# Analyze MOS + WER data
python evaluation/analyze_results.py
```

### Test Suite Coverage

| Module | Tests | What is tested |
|--------|:-----:|----------------|
| `test_utils.py` | 22 | Character sets, vowel harmony, tokenization, WER/CER metrics |
| `test_text_normalizer.py` | 27 | Numbers, ordinals, Roman numerals, abbreviations, symbols, dates |
| `test_g2p_converter.py` | 29 | Vowel/consonant mapping, context rules, devoicing, syllabification |
| `test_stress_assigner.py` | 14 | Default stress, exceptions, phrasal stress, IPA rendering |
| `test_prosody_engine.py` | 30 | Sentence type detection, duration, pitch, pauses, SSML |
| `test_pipeline.py` | 34 | Full pipeline integration, all 50 test sentences end-to-end |
| **Total** | **156** | **All passing** |

---

## G2P Rule System

```mermaid
flowchart LR
    subgraph Input
        G[Grapheme]
    end

    subgraph Context["Context Check (priority order)"]
        R1["Unstressed function word?<br/>(postposition / conjunction / particle)"]
        R2["Known exception?<br/>(deyil, bəlkə, yalnız …)"]
        R3["Palatalization context?<br/>(k/g adjacent to front vowel)"]
        R4["ğ context?<br/>(intervocalic vs. word-final)"]
        R5["Nasal before velar?<br/>(n + k/q/g → ŋ)"]
        R6["Default mapping"]
    end

    subgraph Output
        P[IPA Phoneme]
    end

    G --> R1 --> R2 --> R3 --> R4 --> R5 --> R6 --> P
```

## Stress Rule Hierarchy

```mermaid
flowchart TD
    W([Word]) --> Q1{Function word?<br/>postposition · conjunction · clitic}
    Q1 -- Yes --> S0[Unstressed]
    Q1 -- No  --> Q2{Lexical exception?<br/>deyil · bəlkə · yalnız …}
    Q2 -- Yes --> S1[Exception-defined syllable]
    Q2 -- No  --> Q3{Ends in negation<br/>suffix -ma/-mə<br/>and 3+ syllables?}
    Q3 -- Yes --> S2[Penultimate syllable]
    Q3 -- No  --> S3[Final syllable — default]

    style S0 fill:#ffebee,stroke:#c62828
    style S1 fill:#fff3e0,stroke:#e65100
    style S2 fill:#e8eaf6,stroke:#283593
    style S3 fill:#e8f5e9,stroke:#2e7d32
```

## Vowel System

```mermaid
graph LR
    subgraph Back
        A[a — open back unrounded]
        I[ı — close back unrounded]
        O[o — close-mid back rounded]
        U[u — close back rounded]
    end
    subgraph Front
        E[e — close-mid front unrounded]
        Ə[ə — near-open front unrounded]
        İ[i — close front unrounded]
        Ö[ö — close-mid front rounded]
        Ü[ü — close front rounded]
    end

    Back -- "vowel harmony\n(suffix alternation)" --> Front
```

---

## Repository Structure

```
├── 00_Planning/
│   ├── DEADLINES.md              # Timeline and milestones
│   ├── OUTLINE.md                # Dissertation structure + progress tracker
│   └── ROADMAP.md                # Phase-by-phase implementation plan
│
├── 01_Research/
│   ├── Documents/                # Reference theses and papers (PDF/DOCX)
│   ├── Images/                   # Screenshots and diagrams
│   ├── Notes/                    # Research notes
│   └── REFERENCES.md             # 40+ annotated references (APA 7)
│
├── 02_Technical/
│   ├── Code/
│   │   ├── main.py               # CLI entry point (demo, interactive, analyze)
│   │   ├── pipeline.py           # End-to-end orchestrator
│   │   ├── text_normalizer.py    # NSW → spoken form
│   │   ├── g2p_converter.py      # Graphemes → IPA phonemes
│   │   ├── stress_assigner.py    # Lexical & phrasal stress
│   │   ├── prosody_engine.py     # Pitch, duration, pauses, SSML
│   │   ├── synthesizer.py        # espeak-ng backend
│   │   ├── utils.py              # Shared utilities & metrics
│   │   ├── requirements.txt      # Dependencies
│   │   ├── pytest.ini            # Test configuration
│   │   ├── tests/                # 156 pytest tests (6 test files)
│   │   └── evaluation/           # 50 test sentences + MOS/WER data + scripts
│   └── Rules/
│       ├── g2p_rules.json        # Phoneme mappings & context rules
│       ├── text_norm_rules.json  # Number words, abbreviations, symbols
│       ├── stress_rules.json     # Stress patterns & exceptions
│       └── prosody_rules.json    # Intonation, duration, pause rules
│
├── 03_Dissertation/
│   ├── Abstract.md
│   ├── Introduction.md
│   ├── Chapter_1.md              # TTS overview — history, rule-based, pros/cons
│   ├── Chapter_2.md              # Azerbaijani phonetics, architecture, rule design
│   ├── Chapter_3.md              # Implementation, evaluation, results, conclusion
│   └── References.md             # APA 7 bibliography (40+ references)
│
└── 04_Archive/                   # Deprecated materials
```

---

## Project Timeline

```mermaid
gantt
    title Dissertation Timeline
    dateFormat  YYYY-MM-DD
    section Research
        Literature review       :done,    2025-11-01, 2025-12-21
        Architecture design     :done,    2025-12-01, 2025-12-21
    section Design
        Phonetics deep-dive     :done,    2026-01-01, 2026-02-01
        Rule design             :done,    2026-01-15, 2026-02-15
    section Implementation
        Pipeline modules        :done,    2026-02-01, 2026-03-12
        Dissertation chapters   :done,    2026-02-15, 2026-03-12
    section Evaluation
        Test suite (156 tests)  :done,    2026-03-12, 2026-03-30
        MOS + WER study         :done,    2026-03-15, 2026-03-30
    section Finalization
        Revisions + formatting  :active,  2026-04-01, 2026-05-01
        Final submission        :milestone, 2026-05-01, 1d
```

---

## Planning & Tracking

- [DEADLINES.md](00_Planning/DEADLINES.md) — Timeline and milestones
- [OUTLINE.md](00_Planning/OUTLINE.md) — Dissertation structure and progress
- [ROADMAP.md](00_Planning/ROADMAP.md) — Phase-by-phase plan
- [REFERENCES.md](01_Research/REFERENCES.md) — Annotated bibliography
