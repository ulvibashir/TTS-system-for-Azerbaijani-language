# Chapter 1: Text-to-Speech Synthesis — An Overview

## 1.1 General Text-to-Speech Systems

### 1.1.1 Definition and Historical Development

Text-to-speech (TTS) synthesis is the automatic conversion of written natural language text into intelligible, natural-sounding spoken audio. The goal is not merely to produce any sound corresponding to the input text, but to produce speech that is both **intelligible** — understood correctly by listeners — and **natural** — resembling the prosodic and phonetic properties of human speech.

The history of TTS synthesis spans nearly a century and is characterized by a succession of distinct technological paradigms, each achieving progressively greater quality at the cost of increasing complexity and, in recent decades, data requirements.

**Early mechanical speech synthesis (1930s–1950s).** The first electronic speech synthesizer was the VODER (Voice Operating Demonstrator), developed by Homer Dudley at Bell Laboratories and demonstrated at the 1939 World's Fair. The VODER was operated manually by a trained operator who controlled formant resonances using a keyboard and foot pedal, producing intelligible but robotic-sounding speech. This device established the fundamental insight that the essential perceptual information in speech can be captured by a small number of acoustic parameters — particularly the resonant frequencies of the vocal tract, which would later be formalized as formants.

**Formant synthesis (1960s–1990s).** The first fully automated TTS systems were based on *formant synthesis*, also known as *articulatory* or *parametric* synthesis. These systems modeled the human vocal tract as a series of acoustic tubes whose resonant frequencies — formants F1, F2, and F3 — determine vowel quality and consonant characteristics. The Klatt synthesizer, developed by Dennis Klatt at MIT in the late 1970s and 1980s, became the dominant formant synthesis architecture (Klatt, 1980) and formed the acoustic backbone of commercial products such as DECtalk, which was famously adopted by physicist Stephen Hawking as his communication device.

Formant synthesizers produce speech by computing acoustic waveforms according to a set of parametric rules. All phonological and prosodic knowledge must be encoded explicitly: the system designer must specify the formant frequencies for each phoneme, transitions between phonemes, pitch contour rules for different sentence types, and duration patterns for each phoneme class. The resulting speech is intelligible but unmistakably synthetic — often described as "robotic" — due to the difficulty of precisely modeling the complexity of natural acoustic-phonetic variation.

**Concatenative synthesis (1990s–2000s).** To address the naturalness limitations of formant synthesis, researchers developed *concatenative synthesis* systems, which construct speech by stitching together pre-recorded segments of natural human speech. Two main variants emerged:

- *Diphone synthesis* uses a database of approximately 1,000–2,000 diphone units (transitions from the midpoint of one phoneme to the midpoint of the next). MBROLA (Dutoit et al., 1993) is a widely used diphone synthesis system. Diphone systems achieve more natural phoneme quality than formant synthesis but introduce audible concatenation artifacts at unit boundaries.

- *Unit selection synthesis*, introduced by the Festival Speech Synthesis System (Taylor et al., 1998), selects and concatenates larger speech units (phones, diphones, syllables, words) from large corpora of recorded speech. A dynamic programming algorithm selects units that minimize a target cost (deviation from desired prosody) and a join cost (acoustic discontinuity at boundaries). Unit selection can achieve near-natural quality when the required phonetic context is well-covered in the database, but degrades unpredictably when it is not. Typical unit selection databases require 20–50 hours of recorded speech.

**Statistical parametric synthesis (2000s–2010s).** A significant shift came with the development of *statistical parametric speech synthesis* (SPSS) using Hidden Markov Models (HMMs), most fully realized in the HTS system (Zen et al., 2009). Rather than storing speech segments, HMM-based synthesis learns statistical models of acoustic features — mel-cepstral coefficients, fundamental frequency, and durations — from annotated training data. At synthesis time, the system generates smooth, averaged acoustic trajectories by traversing the learned models. HMM-based synthesis produces speech that is more consistent and robust than unit selection for unseen contexts, but is characterized by a distinctive "muffled" quality due to the over-smoothing inherent in statistical averaging.

**Neural TTS (2016–present).** The deep learning revolution produced a fundamental paradigm shift in TTS. Google's Tacotron (Wang et al., 2017) and Tacotron 2 (Shen et al., 2018) demonstrated that an end-to-end sequence-to-sequence model could learn to map character sequences directly to mel-spectrograms, bypassing explicit phonological analysis. Combined with a neural vocoder such as WaveNet (van den Oord et al., 2016) or, later, HiFi-GAN (Kong et al., 2020), these systems achieved mean opinion scores (MOS) indistinguishable from natural speech for English (MOS ≈ 4.5 on a 1–5 scale, versus approximately 4.6 for natural speech). Subsequent architectures including FastSpeech (Ren et al., 2019), VITS (Kim et al., 2021), and flow-matching models have further improved efficiency and controllability while maintaining state-of-the-art quality.

### 1.1.2 General Architecture of a TTS System

Despite the diversity of acoustic backends, all TTS systems share a broadly common **two-stage architecture**: a *linguistic front-end* that analyzes and enriches the input text, and an *acoustic back-end* that converts the linguistic representation to a waveform.

**Linguistic front-end** components typically include:

1. **Text normalization:** Conversion of non-standard words (NSWs) — numerals, abbreviations, symbols, dates, currency amounts — into their expanded, pronounceable form. For example, "15.06.2024" must be read as "on beşinci iyun iki min iyirmi dördüncü il" in Azerbaijani.

2. **Morphological analysis:** Segmentation of words into morphemes, assignment of part-of-speech labels, and resolution of lexical ambiguity.

3. **Grapheme-to-phoneme (G2P) conversion:** Mapping of orthographic characters to the phonemic representation (typically IPA). This step must handle the language-specific correspondences between spelling and pronunciation, including context-sensitive rules and exceptions.

4. **Prosody prediction:** Generation of the suprasegmental properties of speech — lexical stress, phrase-level pitch accents, intonation contours (pitch trajectories over time), phone durations, and pause locations.

**Acoustic back-end** components convert the phonemic and prosodic representation to audio. In rule-based systems this involves a formant synthesizer or concatenative system; in neural systems it involves acoustic model inference followed by vocoding (waveform generation).

The quality of a TTS system is typically measured using the **Mean Opinion Score (MOS)**, a subjective evaluation in which human listeners rate the naturalness of synthesized samples on a five-point scale from 1 (bad) to 5 (excellent). Intelligibility is assessed separately using transcription accuracy metrics such as word error rate (WER). For reference, natural human speech consistently achieves MOS scores in the range of 4.4–4.7 across languages; current neural TTS systems for English achieve MOS scores of 4.2–4.5 (Kim et al., 2021; Kong et al., 2020); rule-based systems typically achieve MOS scores of 3.0–3.8 depending on language and evaluator population.

---

## 1.2 Rule-Based Text-to-Speech Systems

### 1.2.1 Definition and Principle

A *rule-based TTS system* is one in which every decision in the conversion from text to speech is made by an explicitly programmed rule that encodes human linguistic knowledge. This contrasts with data-driven approaches, in which the system learns patterns statistically from annotated corpora (HMM-based synthesis) or from raw audio and text pairs (neural TTS), without explicit encoding of phonological or prosodic principles.

Rule-based TTS relies on the following foundational claim: the mapping from orthography to phonetics, and from phonetics to prosody, in a given language is sufficiently regular and well-understood that it can be captured in a finite, maintainable set of rules. For languages with a highly regular, phonemic orthography — such as Azerbaijani, Finnish, Spanish, and Turkish — this claim is substantially true. For languages with highly irregular orthographic traditions — such as English or French — it is significantly less tractable, which is one reason why neural approaches gained their earliest traction in English.

### 1.2.2 Formant Synthesis

Formant synthesis produces speech waveforms by mathematically modeling the resonant properties of the human vocal tract. The vocal tract is treated as a variable-length cylindrical tube — or, more precisely, as a cascade of cylindrical sections — whose cross-sectional areas at each point determine the resonant frequencies (formants) of the system.

The Klatt cascade-parallel formant synthesizer (Klatt, 1980) remains the definitive reference architecture. It models speech production using:
- A voicing source (either a buzz-like glottal pulse train for voiced sounds, or a noise source for unvoiced sounds)
- A cascade of resonator filters (for vowels and sonorant consonants), each resonator corresponding to one formant frequency
- A parallel bank of resonators (for obstruent consonants)
- A radiation filter and final gain control

The synthesizer is controlled by a time-varying parameter vector specifying, at each 5ms frame: voicing frequency (F0), voicing amplitude, aspiration amplitude, five formant frequencies (F1–F5) and their bandwidths, nasal pole and zero frequencies, and several additional parameters controlling voice quality and breathiness.

Generating natural-sounding speech requires specifying the correct parameter trajectories for every phoneme sequence in the target language — including the coarticulation transitions between phonemes, where neighboring sounds systematically influence each other's formant values. These specifications constitute the *synthesis rule set* and represent the core intellectual contribution of a formant TTS designer.

### 1.2.3 Rule-Based Concatenative Synthesis (MBROLA / Festival)

An alternative rule-based approach uses a *phoneme inventory* — a set of pre-recorded, isolated phoneme-length speech segments — as acoustic building blocks, concatenated according to a phoneme string produced by the G2P module and durational rules.

The MBROLA project (Dutoit et al., 1993) provides such phoneme inventories for dozens of languages, including Turkish. Given a sequence of (phoneme, duration, pitch) triplets, MBROLA synthesizes speech by time-scaling and pitch-modifying the corresponding inventory segments and concatenating them. The interface to MBROLA is purely rule-based: the calling system must supply exact phoneme durations and F0 targets according to its own rule set.

The Festival Speech Synthesis System (Taylor et al., 1998), developed at the University of Edinburgh, provides a complete rule-based TTS framework using the Lisp-derived language Scheme. Festival integrates text normalization, morphological analysis, G2P conversion, prosodic analysis, and multiple acoustic backends (including both unit selection and MBROLA). Its modular design and extensive documentation make it a standard reference architecture for TTS research.

The espeak-ng system (originally developed by Jonathan Duddington as eSpeak) takes a different approach: it uses a compact, hand-crafted formant synthesis model with phoneme definitions specified in text configuration files. espeak-ng supports over 100 languages, including Azerbaijani, and is the acoustic backend used in the present system.

---

## 1.3 Advantages and Disadvantages of Rule-Based TTS

The choice of a rule-based approach for the present system is deliberate and motivated by the specific circumstances of Azerbaijani TTS development. This section presents a systematic assessment of the advantages and disadvantages of rule-based synthesis, contextualizing them against the competing paradigms.

### 1.3.1 Advantages

**1. No speech data requirements.** Neural TTS systems require between 1 and 50+ hours of high-quality, professionally recorded, transcribed speech data in the target language. For low-resource languages like Azerbaijani, where no such corpus is publicly available, this requirement is prohibitive. Rule-based systems require only linguistic expertise and, for concatenative backends, a small set of isolated phoneme recordings.

**2. Full interpretability and transparency.** Every output of a rule-based system is the direct consequence of an explicitly stated rule. When the system mispronounces a word or generates incorrect prosody, the source of the error can be identified and corrected by examining and updating the relevant rule. Neural systems, by contrast, are opaque: when a neural TTS system fails, it is generally not possible to determine *why* it failed or to make targeted corrections without re-training.

**3. Deterministic and consistent behavior.** Given the same input, a rule-based system always produces exactly the same output. This consistency is valuable in deployment contexts where reproducibility is required — for instance, in accessibility applications or standardized language learning tools. Neural systems may exhibit output variability due to stochastic sampling during inference.

**4. Direct incorporation of linguistic knowledge.** Linguists who study a language can directly encode their knowledge into a rule-based TTS system. This creates a productive collaboration between linguistics and engineering that is largely absent in the neural paradigm, where linguistic knowledge is implicitly learned from data rather than explicitly specified.

**5. Low computational requirements.** Rule-based synthesis can run in real time on commodity hardware without a GPU, using only a few megabytes of memory. This makes it suitable for embedded systems, mobile devices, and offline applications. Neural TTS systems, particularly those using large transformer models, may require significant GPU resources for real-time synthesis.

**6. Easy domain adaptation.** Adding new words, specialized terminology, or pronunciation variants to a rule-based system requires only editing the relevant rules or exceptions dictionary. Adapting a neural system to new vocabulary requires either retraining or careful fine-tuning.

**7. No intellectual property constraints from training data.** Neural TTS systems trained on commercial speech recordings may carry licensing restrictions. A rule-based system built entirely from linguist-specified rules has no such encumbrances.

### 1.3.2 Disadvantages

**1. Lower naturalness.** The primary disadvantage of rule-based TTS is the quality ceiling imposed by the acoustic modeling paradigm. Formant synthesizers and MBROLA-style concatenative systems produce speech that is readily recognizable as synthetic. Modern neural TTS systems, trained on sufficient data, can produce speech that is perceptually indistinguishable from natural human speech. For applications where naturalness is paramount — audiobooks, voice assistants — this gap is significant. Empirically, rule-based systems typically achieve MOS scores of 3.0–3.8, compared to 4.2–4.5 for state-of-the-art neural systems (Kim et al., 2021; Oyucu, 2023).

**2. High development effort for complex languages.** While Azerbaijani has a relatively regular orthography, its agglutinative morphology and context-sensitive phonological rules require substantial engineering effort to handle correctly. Designing, testing, and refining rules for a complete language requires deep linguistic expertise and is time-consuming.

**3. Difficulty handling exceptions and variation.** Natural language is full of irregular forms, loanwords with non-native phonological patterns, and stylistic variation. Rule-based systems handle these through exception lists and special-case rules, which must be manually maintained. Neural systems learn these patterns implicitly from data.

**4. Prosodic expressiveness limitations.** Generating natural-sounding prosody — pitch contours that sound genuinely human, appropriate rhythmic variation, subtle emphasis — is extremely difficult to encode in explicit rules. Neural prosody models, trained on natural speech data, capture the statistical regularities of human prosody in ways that rule-based systems cannot fully replicate.

**5. Coarticulation modeling.** In natural speech, the acoustic properties of each phoneme are strongly influenced by neighboring phonemes through coarticulation. Rule-based systems model coarticulation through transition rules and formant interpolation, which approximate but do not fully capture the complexity of natural coarticulation.

### 1.3.3 Summary Comparison

| Criterion | Rule-Based | Neural TTS |
|---|---|---|
| Speech naturalness (MOS) | 3.0–3.8 | 4.2–4.5 |
| Data requirements | None | 1–50+ hours |
| Transparency | Full | Opaque |
| Computational cost | Low (CPU, real-time) | High (GPU preferred) |
| Development effort | High (linguistic) | High (data collection) |
| Consistency | Deterministic | May vary |
| Low-resource feasibility | High | Low |
| Domain adaptation | Easy | Difficult |

For Azerbaijani — a low-resource language with a well-documented, regular phonological system — the rule-based paradigm offers the best feasible path to a functional, transparent, and extensible TTS system at this stage of the language's technological development.
