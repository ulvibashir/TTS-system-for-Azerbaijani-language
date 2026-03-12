# Design and Development of a Rule-Based TTS System for Azerbaijani Language

- **Institution:** Azerbaijan State Economic University (UNEC)
- **Program:** MBA in Artificial Intelligence
- **Type:** Master's Dissertation
- **Target Length:** 51-75 pages
- **Citation Style:** APA 7
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

### G2P Rule System

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

### Stress Rule Hierarchy

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

### Vowel System

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

## Quick Start

**Requirements:** Python 3.10+ and [espeak-ng](https://github.com/espeak-ng/espeak-ng/releases)

```bash
# Install espeak-ng (Linux)
sudo apt install espeak-ng

# Run demo (10 test sentences covering key linguistic phenomena)
cd 02_Technical/Code
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

## Repository Structure

```
├── 00_Planning/
│   ├── DEADLINES.md          # Timeline and milestones
│   ├── OUTLINE.md            # Dissertation structure + progress tracker
│   └── ROADMAP.md            # Phase-by-phase implementation plan
│
├── 01_Research/
│   ├── Documents/            # Reference theses and papers (PDF/DOCX)
│   ├── Images/               # Screenshots and diagrams
│   ├── Notes/                # Research notes
│   └── REFERENCES.md         # 40+ annotated references (APA 7)
│
├── 02_Technical/
│   ├── Code/
│   │   ├── main.py           # CLI entry point
│   │   ├── pipeline.py       # End-to-end orchestrator
│   │   ├── text_normalizer.py
│   │   ├── g2p_converter.py
│   │   ├── stress_assigner.py
│   │   ├── prosody_engine.py
│   │   ├── synthesizer.py
│   │   ├── utils.py
│   │   └── requirements.txt
│   └── Rules/
│       ├── g2p_rules.json
│       ├── text_norm_rules.json
│       ├── stress_rules.json
│       └── prosody_rules.json
│
├── 03_Dissertation/
│   ├── Abstract.md
│   ├── Introduction.md
│   ├── Chapter_1.md          # TTS overview — history, rule-based synthesis, pros/cons
│   ├── Chapter_2.md          # Azerbaijani phonetics, system architecture, rule design
│   ├── Chapter_3.md          # Implementation, evaluation methodology, results
│   └── References.md         # APA 7 bibliography
│
└── 04_Archive/               # Deprecated materials
```

---

## Linguistic Coverage

| Feature | Handled |
|---|---|
| 9-vowel system (a, e, ə, ı, i, o, ö, u, ü) | ✅ |
| Vowel harmony (back/front classes) | ✅ |
| Palatalization of /k/ and /g/ before front vowels | ✅ |
| /ğ/ allophony (intervocalic → /ɣ/, word-final → /ː/) | ✅ |
| Final obstruent devoicing | ✅ |
| Nasal assimilation (/n/ → /ŋ/ before velars) | ✅ |
| Geminate consonants | ✅ |
| Default final-syllable stress | ✅ |
| Stress exceptions (deyil, -ma/-mə, particles, postpositions) | ✅ |
| Sentence type detection (declarative, YN-question, WH-question, exclamatory) | ✅ |
| Number-to-words (cardinal, ordinal, vowel-harmony-correct suffixes) | ✅ |
| Dates, times, abbreviations, currency, unit symbols | ✅ |

---

## Project Status

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
        MOS + WER study         :active,  2026-03-12, 2026-04-01
    section Finalization
        Revisions + formatting  :         2026-04-01, 2026-05-01
        Final submission        :milestone, 2026-05-01, 1d
```

---

## Planning & Tracking

- [DEADLINES.md](00_Planning/DEADLINES.md) — Timeline and milestones
- [OUTLINE.md](00_Planning/OUTLINE.md) — Dissertation structure and progress
- [ROADMAP.md](00_Planning/ROADMAP.md) — Phase-by-phase plan
- [REFERENCES.md](01_Research/REFERENCES.md) — Annotated bibliography
