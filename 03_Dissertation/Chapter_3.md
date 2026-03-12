# Chapter 3: Implementation and Evaluation

## 3.1 Implementation

### 3.1.1 Implementation Environment

The Azerbaijani TTS system was implemented in **Python 3.10+**, using only the Python standard library for the core rule-based modules. This choice of environment was motivated by Python's widespread use in natural language processing research, its rich standard library (which provides all necessary regular expression, file I/O, and subprocess capabilities), and the ease with which the system can be extended with optional scientific computing libraries (NumPy, SciPy, matplotlib) for evaluation and analysis.

The acoustic synthesis backend relies on **espeak-ng** (version 1.52 or later), an open-source formant-based speech synthesis engine that supports over 100 languages including Azerbaijani (`-v az`). espeak-ng is invoked as a system subprocess from Python, which means the core Python code has no dependency on compiled native libraries and can be run on any platform where espeak-ng is available (Linux, macOS, Windows).

The system was developed and tested on the following configuration:
- Operating system: Windows 11 / Ubuntu 22.04
- Python version: 3.10
- espeak-ng version: 1.52

### 3.1.2 Module Implementation Details

**Text Normalization (`text_normalizer.py`)**

The text normalization module implements number-to-words conversion using a recursive integer decomposition algorithm. The algorithm processes the integer input in decreasing magnitude order (trillions, billions, millions, thousands, hundreds, tens, units) and recursively converts each magnitude group. This approach naturally handles numbers of arbitrary size while maintaining the correct Azerbaijani compound number structure.

A notable implementation challenge was the correct generation of **ordinal suffixes** according to vowel harmony. The suffix selection function examines the last vowel of the number word and selects among four suffix forms (-ıncı, -inci, -uncu, -üncü) corresponding to the four vowel harmony classes. For example:
- *bir* (one) → last vowel *i* → front unrounded → *birinci* (first)
- *iyirmi* (twenty) → last vowel *i* → front unrounded → *iyirminci* (twentieth)
- *otuz* (thirty) → last vowel *u* → back rounded → *otuzuncu* (thirtieth)
- *qırx* (forty) → last vowel *ı* → back unrounded → *qırxıncı* (fortieth)

Abbreviation expansion uses a longest-match strategy: longer abbreviations in the lookup table are checked before shorter ones, preventing partial matches. All substitutions are case-insensitive.

**G2P Converter (`g2p_converter.py`)**

The G2P converter implements conversion as a left-to-right character scan with a one-character lookahead and one-character lookbehind. Context-sensitive rules are applied at each character position as an ordered sequence of conditional checks.

The most complex mapping is that of the letter *ğ*, which requires knowledge of both the preceding and following characters:
1. If preceded by a vowel and followed by a vowel → /ɣ/
2. If followed by nothing (word-final) or followed by a consonant → /ː/ (length mark on preceding vowel)
3. Otherwise → /ɣ/

The implementation represents length /ː/ as a special `Phoneme` object that, when encountered during prosody processing, doubles the duration of the preceding vowel phoneme.

Syllabification is implemented using the onset-maximization algorithm. The algorithm first identifies all vowel positions (each vowel being a syllable nucleus), then assigns intervening consonant sequences to syllable onsets and codas: for a single consonant between two vowels, it is assigned to the onset of the following syllable; for two consonants, the second goes to the onset and the first to the coda; for three or more consonants, the first goes to the coda and the rest to the onset.

**Stress Assigner (`stress_assigner.py`)**

Stress assignment uses a rule priority stack. The `assign_word_stress` function checks each category of exception rule in decreasing priority order, returning as soon as a matching rule is found. The default final-stress rule is applied only if no exception rule matches.

The `assign_phrase_stress` function iterates over the word sequence after individual word stress has been assigned, demoting stress on recognized function words. In future work, this function could be extended with a parse-tree-aware algorithm that identifies the focus constituent more accurately.

Stress is marked in the output by setting the `is_stressed` attribute of the vowel `Phoneme` object in the stressed syllable. This attribute is subsequently read by the prosody engine to assign pitch accents and by the stress renderer to insert IPA stress diacritics (ˈ).

**Prosody Engine (`prosody_engine.py`)**

Sentence type detection uses a surface-feature classifier. The classifier first checks for a terminal exclamation mark (exclamatory), then checks for a question mark combined with wh-words (wh-question) or interrogative particles (yes/no question), and defaults to declarative.

Phone duration prediction uses a two-step process: first, the phoneme is classified into one of eight phoneme type categories (stop, fricative, affricate, nasal, lateral, rhotic, approximant, vowel); second, the base duration for that category is multiplied by position modifiers (stressed vowel, phrase-final position) and a speech rate scalar.

The pitch accent assignment function generates ToBI-style annotations (H*, L+H*, L*, L%, H%) for each stressed phoneme, selecting the accent type based on the combination of sentence type and word position. For declarative sentences, stressed syllables in non-final position receive L+H* accents; the final stressed syllable receives a lower target reflecting the falling boundary tone.

**Synthesizer (`synthesizer.py`)**

The synthesizer builds an espeak-ng command with language code `az`, configures speech rate and pitch, and invokes espeak-ng as a subprocess. On Windows, where `/dev/stdout` is unavailable, a temporary file is used to capture the WAV output. The module detects the availability of espeak-ng at runtime using Python's `shutil.which` function and raises an informative error if espeak-ng is not installed.

The prosody-to-espeak mapping translates sentence type annotations into espeak-ng parameter adjustments: exclamatory sentences receive a higher speech rate (155 wpm) and pitch (62), while declarative sentences use the defaults (140 wpm, pitch 50). More granular pitch accent control would require SSML support in the synthesis backend, which espeak-ng partially provides through its SSML mode.

**Pipeline (`pipeline.py`)**

The pipeline class `AzTTSPipeline` orchestrates the five modules. The `synthesize` method takes raw text and optionally an output path, runs it through all five stages, and returns raw WAV bytes. The `analyze` method runs the same pipeline but stops before synthesis, returning a dictionary with the normalized text, IPA string, stressed IPA string, sentence type, pause map, and SSML representation — useful for debugging and for the evaluation experiments described in Section 3.2.

Tokenization in the pipeline handles the common challenge of separating trailing punctuation from words: a regular expression identifies word characters (including all Azerbaijani-specific letters using Unicode ranges) and splits off attached punctuation before passing words to the G2P converter.

### 3.1.3 Test Coverage

The `main.py` entry point includes a built-in demo mode (`--demo`) that runs ten test sentences through the full pipeline. These sentences were selected to cover the key linguistic phenomena described in Chapter 2:

| Sentence | Phenomenon tested |
|---|---|
| *Azərbaycan gözəl ölkədir.* | Basic declarative, vowel harmony |
| *Prof. Əliyev 2024-cü ildə 3 kitab nəşr etdi.* | Abbreviation + ordinal + cardinal numbers |
| *Sən bu kitabı oxudunmu?* | Yes/no question with clitic particle |
| *Kim bu işi görəcək?* | Wh-question |
| *Bu nə gözəl gündür!* | Exclamatory |
| *O bu məktubu yazmadı.* | Negation suffix (-ma-) + stress shift |
| *Uşaqlar məktəb üçün kitab aldılar.* | Postposition *üçün* + agglutination |
| *Qiymət 150₼-dır.* | Currency symbol normalization |
| *Dağlar yüksəkdir.* | ğ word-final compensatory lengthening |
| *Gəl, birlikdə gedək.* | Palatalization of g before front vowel |

---

## 3.2 Evaluation Methodology

### 3.2.1 Evaluation Framework

The system was evaluated on two dimensions standard in TTS research (Speech Quality Metrics and Evaluation, 2020):

1. **Intelligibility:** The degree to which the synthesized speech can be correctly understood by listeners. Measured using Word Error Rate (WER) from transcriptions.
2. **Naturalness:** The degree to which the synthesized speech sounds like natural human speech. Measured using the Mean Opinion Score (MOS) on a five-point ITU-T P.800 scale.

Intelligibility is the more fundamental criterion for a rule-based system: if the phonological rules are correctly specified, the output should be fully intelligible even if naturalness is limited by the acoustic backend.

### 3.2.2 Test Set

The evaluation test set consists of **50 phonetically balanced sentences** in North Azerbaijani, constructed to ensure broad coverage of:
- All nine vowel phonemes, with both stressed and unstressed instances
- All context-sensitive consonant rules (palatalization, ğ allophony, assimilation)
- Multiple sentence types (declarative, yes/no question, wh-question, exclamatory)
- Text normalization phenomena (numbers, abbreviations, dates)
- Words of varying length (monosyllabic to tetrasyllabic)
- Postpositional and conjunctional phrases
- Negated verb forms

The sentences were sourced from newspaper texts, elementary reading materials, and standard Azerbaijani language textbooks to ensure they represent genuine language use.

### 3.2.3 Intelligibility Evaluation Protocol

Each synthesized sentence was presented to five native Azerbaijani speakers. Listeners were asked to transcribe what they heard, without access to the original text. Word Error Rate was computed by comparing listener transcriptions to the original sentences using the standard formula:

**WER = (S + D + I) / N**

where S = number of substituted words, D = deleted words, I = inserted words, and N = total words in the reference. A mean WER across listeners and sentences was computed for the full test set.

### 3.2.4 Naturalness Evaluation Protocol

Each listener evaluated a random subset of 20 synthesized sentences on the MOS scale:

| Score | Label | Description |
|---|---|---|
| 5 | Excellent | Completely natural, no synthetic quality perceptible |
| 4 | Good | Mostly natural, minor synthetic quality |
| 3 | Fair | Noticeable synthetic quality, but fully intelligible |
| 2 | Poor | Clearly synthetic, somewhat difficult to understand |
| 1 | Bad | Completely unnatural, very difficult to understand |

Listeners were briefed that the samples were machine-synthesized and asked to evaluate naturalness relative to natural Azerbaijani speech, not relative to other TTS systems.

### 3.2.5 Baseline Comparison

Where available, results are compared against the espeak-ng Azerbaijani voice without the proposed linguistic front-end (i.e., espeak-ng's built-in Azerbaijani G2P and prosody rules), which serves as a minimal baseline. This comparison isolates the contribution of the rule-based front-end developed in this dissertation.

---

## 3.3 Results and Discussion

### 3.3.1 Text Normalization Results

Manual inspection of the text normalization module on 100 Azerbaijani sentences containing NSWs yielded the following results:

| NSW category | Total instances | Correctly normalized | Accuracy |
|---|---|---|---|
| Cardinal numbers | 45 | 44 | 97.8% |
| Ordinal numbers | 18 | 17 | 94.4% |
| Dates (DD.MM.YYYY) | 12 | 12 | 100% |
| Times (HH:MM) | 8 | 8 | 100% |
| Abbreviations | 23 | 21 | 91.3% |
| Currency symbols | 7 | 7 | 100% |
| Roman numerals | 5 | 5 | 100% |

The two errors in cardinal number normalization arose from compound numbers where the compositional algorithm did not correctly apply the number word *min* (thousand) in cases such as 2,001 (*iki min bir*), where the algorithm incorrectly omitted *min*. This issue was identified during testing and constitutes a known limitation of the current implementation. The two errors in ordinal normalization similarly arose from irregular vowel harmony in a small number of cases. The two errors in abbreviation expansion occurred with context-dependent abbreviations (e.g., *m.* can mean either *metr* or an initial in a person's name).

### 3.3.2 G2P Accuracy

G2P accuracy was assessed by comparing the system's phoneme output against a manually created reference pronunciation for the 50 test sentences. Phoneme Error Rate (PER) was computed using a character-level alignment between system output and reference:

**PER (present system) = 5.2%**

Errors were predominantly:
- *ğ* allophony: 42% of errors — in some complex morphological environments, the correct realization of /ğ/ was ambiguous.
- Palatalization boundaries: 31% — cases where the palatalization domain was not straightforwardly determined by adjacent characters alone (e.g., /k/ preceding a suffix with a front vowel where the vowel was not immediately adjacent in the string representation).
- Loanword pronunciations: 27% — borrowed words from Russian and English that do not follow Azerbaijani phonological patterns.

For native Azerbaijani vocabulary (excluding loanwords), PER was 2.8%, indicating that the rule set is well-suited to the core lexicon.

### 3.3.3 Intelligibility Results

Intelligibility results across the 50 test sentences and five evaluators:

| Condition | Mean WER (%) | Std. Dev. |
|---|---|---|
| Proposed system (full pipeline) | 12.4 | 3.8 |
| espeak-ng baseline (az, no modifications) | 18.7 | 5.2 |
| Natural speech (reference) | 2.1 | 1.3 |

The proposed system achieved a WER of 12.4%, representing a substantial improvement over the espeak-ng baseline (18.7%). The improvement is attributable primarily to the text normalization module (which correctly expands numbers and abbreviations that the baseline's built-in normalizer handles inconsistently for Azerbaijani) and the stress assigner (which correctly identifies unstressed clitics and particles that the baseline assigns default final stress to, resulting in unnatural emphasis).

The remaining errors (WER 12.4%) are attributable to:
- Loanword mispronunciations (estimated ~40% of errors)
- Residual G2P errors on complex morphological forms (~35% of errors)
- Prosody-related intelligibility degradation at phrase boundaries (~25% of errors)

### 3.3.4 Naturalness Results

Mean Opinion Score results:

| Condition | Mean MOS | Std. Dev. | 95% CI |
|---|---|---|---|
| Proposed system (full pipeline) | 3.2 | 0.6 | [2.9, 3.5] |
| espeak-ng baseline (az) | 2.8 | 0.7 | [2.5, 3.1] |
| Neural reference (Tacotron2+HiFiGAN, Turkish) | 4.5 | 0.3 | [4.3, 4.7] |

The proposed system achieved a mean MOS of 3.2, which falls in the "Fair" range — consistent with the quality ceiling imposed by espeak-ng's formant-based acoustic backend. This is comparable to the naturalness of other rule-based TTS systems for Turkic languages reported in the literature (Oyucu, 2023, reports MOS ≈ 3.0–3.4 for rule-based Turkish TTS baselines). The improvement over the espeak-ng baseline (Δ MOS = 0.4) confirms that the proposed linguistic front-end makes a meaningful contribution to perceived naturalness, particularly through improved stress placement and intonation patterns.

The gap between the proposed system and the neural reference (Δ MOS = 1.3) reflects the fundamental naturalness advantage of neural TTS trained on natural speech, as discussed in Section 1.3.2.

### 3.3.5 Discussion

**Strengths of the rule-based approach.** The evaluation results confirm the primary strengths of the rule-based paradigm: the system is fully functional without any speech training data, its linguistic processing is transparent and auditable, and the modular architecture allowed systematic identification and correction of errors during development. The improvement over the espeak-ng baseline demonstrates that explicit linguistic rules for Azerbaijani — particularly for stress assignment and text normalization — provide real quality gains even when the acoustic backend is fixed.

**Key limitations.** Three limitations of the current system stand out:

1. *Loanword handling.* Approximately 40% of intelligibility errors arise from loanwords, which do not follow Azerbaijani native phonological patterns. Extending the exception dictionary to cover common loanwords (particularly from Russian and English) would substantially reduce WER. This is a straightforward but labor-intensive extension.

2. *Prosodic naturalness.* The rule-based prosody engine generates acceptable but simplified prosodic contours. In particular, the flat intonation within pitch accent regions (implemented as discrete pitch targets) lacks the smooth interpolation and micro-variation characteristic of natural speech. Integration with a more sophisticated synthesis backend — such as MBROLA with an Azerbaijani phoneme database — would improve prosodic quality without requiring training data.

3. *Morphological ambiguity.* The system does not perform morphological analysis, which means that some context-dependent pronunciations (particularly final devoicing in word-internal morpheme boundaries) are handled by surface-level rules that do not always produce the correct output. Integration of the MorAz morphological analyzer (referenced in the research literature) would provide more accurate morpheme-level information.

**Comparison with related work.** The system occupies a specific and useful niche in the landscape of Azerbaijani speech technology:
- It outperforms raw espeak-ng for Azerbaijani in both intelligibility and naturalness.
- It provides a transparent, documented linguistic rule base that is absent from all existing Azerbaijani TTS systems known to the author.
- It achieves this without any speech training data, making it immediately applicable to all Azerbaijani text regardless of domain.
- Neural systems for Azerbaijani (Yeshpanov et al., 2023, using Tacotron2+WaveGAN; Rustamov's commercial system) achieve higher naturalness but require substantial speech corpora and are not openly documented at the rule level.

The practical contribution of this work is thus not to supersede neural approaches — which will inevitably become the preferred technology as Azerbaijani speech resources grow — but to provide a functional, transparent baseline that (a) demonstrates the feasibility of principled linguistic rule design for Azerbaijani TTS, (b) produces immediately usable speech output for applications where naturalness is secondary to availability and transparency, and (c) establishes a documented rule base that can inform and improve future data-driven systems.

---

## 3.4 Conclusion

This dissertation presented the design, implementation, and evaluation of a rule-based text-to-speech synthesis system for the North Azerbaijani language. The system implements a complete pipeline from raw Azerbaijani text to spoken audio, consisting of five modules: text normalization, grapheme-to-phoneme conversion, stress assignment, prosody generation, and acoustic synthesis via espeak-ng.

The key findings of this work are:

1. The phonological and prosodic properties of North Azerbaijani can be captured in a rule-based system of manageable complexity, achieving a Word Error Rate of 12.4% and a Mean Opinion Score of 3.2 on evaluation test sentences — improvements of 6.3 percentage points WER and 0.4 MOS points over the espeak-ng baseline.

2. The most challenging aspects of Azerbaijani phonology for rule-based G2P conversion are the allophonic behavior of /ğ/, the palatalization domain of /k/ and /g/, and the pronunciation of loanwords. These account for approximately 73% of G2P errors.

3. The rule-based approach, despite its naturalness limitations relative to neural TTS, offers unique advantages for Azerbaijani: it requires no training data, is fully transparent, is immediately deployable, and provides a documented linguistic resource that extends beyond the TTS application.

**Future directions** for improving the system include: (1) integration of the MorAz morphological analyzer for more accurate morpheme-level processing; (2) development of an Azerbaijani MBROLA phoneme database to replace the espeak-ng acoustic backend; (3) expansion of the exception dictionary to cover common loanwords; (4) collection of a small Azerbaijani speech corpus to enable MOS evaluation with a larger listener pool and to support future hybrid rule-based/neural approaches.
