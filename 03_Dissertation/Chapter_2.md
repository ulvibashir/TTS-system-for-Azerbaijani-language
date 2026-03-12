# Chapter 2: Azerbaijani Language and System Design

## 2.1 Azerbaijani Phonetics and Phonology

### 2.1.1 Overview of the Azerbaijani Language

Azerbaijani (also called Azeri or Azerbaijani Turkish) belongs to the Oghuz branch of the Turkic language family, making it closely related to Turkish, Turkmen, and Gagauz. It is the official language of the Republic of Azerbaijan and is spoken by approximately 10 million people within Azerbaijan and an estimated 25 million people in northwestern Iran (South Azerbaijani). This dissertation addresses **North Azerbaijani**, the standard variety used in the Republic of Azerbaijan and codified in the Latin-based orthography adopted in 1992 following the dissolution of the Soviet Union.

As a Turkic language, Azerbaijani exhibits several typological features of direct relevance to TTS design: **agglutinative morphology** (words are formed by concatenating morphemes, each with a clearly defined function), **vowel harmony** (suffixal vowels must harmonize in frontness/backness with the root vowel), **verb-final word order** (SOV), and a predominantly suffixing morphological system. These properties have important consequences for G2P conversion, stress assignment, and prosodic phrasing.

### 2.1.2 Orthography

Since 1992, North Azerbaijani has been written in a 32-letter Latin alphabet. The orthography is broadly phonemic — there is a close, though not entirely one-to-one, correspondence between graphemes and phonemes — making it considerably more amenable to rule-based G2P conversion than languages such as English or French.

The Azerbaijani Latin alphabet is as follows:

> A, B, C, Ç, D, E, Ə, F, G, Ğ, H, X, I, İ, J, K, Q, L, M, N, O, Ö, P, R, S, Ş, T, U, Ü, V, Y, Z

Key orthographic features relevant to TTS:

- **ə** (schwa-like open front vowel) is distinct from **e** (close-mid front vowel). This distinction is phonemically contrastive and must be preserved in G2P conversion.
- **ı** (dotless i, close back unrounded) is distinct from **i** (close front unrounded). Both the uppercase forms (I and İ) and lowercase forms (ı and i) must be handled correctly.
- **ğ** (soft g) does not represent a consonant in the same way as other letters; its phonetic realization is highly context-dependent (see Section 2.1.4).
- **c** represents the affricate /dʒ/ (as in English "judge"), not the stop /k/.
- **x** represents the velar fricative /x/ (as in German "Bach"), not /ks/.
- **q** represents the uvular stop /ɢ/, distinct from the velar stop /k/—a phonemic distinction not found in English or most European languages.

### 2.1.3 Vowel System

Azerbaijani has **nine vowel phonemes**, organized along the dimensions of height (close, close-mid, open-mid, open), backness (front, back), and rounding. This nine-vowel system is richer than Turkish (which also has nine vowels) and considerably richer than most Indo-European languages.

| Grapheme | IPA | Height | Backness | Rounding | Example |
|---|---|---|---|---|---|
| a | /a/ | Open | Back | Unrounded | *alma* (apple) |
| e | /e/ | Close-mid | Front | Unrounded | *ev* (house) |
| ə | /æ/ | Near-open | Front | Unrounded | *əl* (hand) |
| ı | /ɯ/ | Close | Back | Unrounded | *ıldız* (star) |
| i | /i/ | Close | Front | Unrounded | *il* (year) |
| o | /o/ | Close-mid | Back | Rounded | *od* (fire) |
| ö | /ø/ | Close-mid | Front | Rounded | *öz* (self) |
| u | /u/ | Close | Back | Rounded | *uşaq* (child) |
| ü | /y/ | Close | Front | Rounded | *üz* (face) |

The acoustic properties of Azerbaijani vowels have been documented in detail by the Cambridge Core phonetic description of Azerbaijani (see References): formant frequencies for the nine vowels in a standard male speaker are approximately as given in published acoustic studies, with F1 (first formant, correlating with vowel height) and F2 (second formant, correlating with backness) values clearly separating the nine categories.

**Vowel length** is not phonemically contrastive in native Azerbaijani vocabulary, though the phoneme /ğ/ triggers compensatory lengthening of the preceding vowel at word boundaries and before consonants (see Section 2.1.4). Long vowels are denoted in IPA with the length mark /ː/.

### 2.1.4 Consonant System

Azerbaijani has **23 consonant phonemes**. The following table presents the complete consonant inventory with orthographic and IPA correspondences:

| Grapheme | IPA | Manner | Place | Voicing | Example |
|---|---|---|---|---|---|
| b | /b/ | Stop | Bilabial | Voiced | *baş* (head) |
| c | /dʒ/ | Affricate | Post-alveolar | Voiced | *can* (soul) |
| ç | /tʃ/ | Affricate | Post-alveolar | Voiceless | *çay* (tea/river) |
| d | /d/ | Stop | Alveolar | Voiced | *dağ* (mountain) |
| f | /f/ | Fricative | Labiodental | Voiceless | *fil* (elephant) |
| g | /ɡ/ ~ /c/ | Stop | Velar ~ Palatal | Voiced | *gül* (rose) |
| ğ | /ɣ/ ~ /ː/ | Fricative ~ length | Velar | Voiced | *dağ* (mountain) |
| h | /h/ | Fricative | Glottal | Voiceless | *hava* (air) |
| x | /x/ | Fricative | Velar | Voiceless | *xəbər* (news) |
| j | /ʒ/ | Fricative | Post-alveolar | Voiced | *jurnal* (journal) |
| k | /k/ ~ /c/ | Stop | Velar ~ Palatal | Voiceless | *kitab* (book) |
| q | /ɢ/ | Stop | Uvular | Voiced | *qız* (girl) |
| l | /l/ | Lateral | Alveolar | Voiced | *liman* (port) |
| m | /m/ | Nasal | Bilabial | Voiced | *meşə* (forest) |
| n | /n/ ~ /ŋ/ | Nasal | Alveolar ~ Velar | Voiced | *nə* (what) |
| p | /p/ | Stop | Bilabial | Voiceless | *paltar* (clothes) |
| r | /r/ | Trill | Alveolar | Voiced | *rəng* (color) |
| s | /s/ | Fricative | Alveolar | Voiceless | *su* (water) |
| ş | /ʃ/ | Fricative | Post-alveolar | Voiceless | *şəhər* (city) |
| t | /t/ | Stop | Alveolar | Voiceless | *torpaq* (soil) |
| v | /v/ | Fricative | Labiodental | Voiced | *vaxt* (time) |
| y | /j/ | Approximant | Palatal | Voiced | *yol* (road) |
| z | /z/ | Fricative | Alveolar | Voiced | *zaman* (time) |

**Context-sensitive consonant realizations** are among the most important phonological features to capture in G2P conversion:

**Palatalization of /k/ and /g/.** When the velar stops /k/ and /ɡ/ occur adjacent to front vowels (e, ə, i, ö, ü), they are realized as palatal stops /c/ and /c/ respectively (Salimi, n.d.; Cambridge Core, n.d.). For example:
- *gül* /cyl/ (rose) — /g/ before front vowel /ü/ → /c/
- *gəl* /cæl/ (come) — /g/ before front vowel /ə/ → /c/
- *kitab* /citab/ (book) — /k/ before front vowel /i/ → /c/
- Compare: *qız* /ɢɯz/ (girl) — /q/ (uvular) before back vowel /ı/ → /ɢ/

**The phoneme /ğ/ (soft g).** The letter *ğ* is orthographically exceptional in that it does not represent a consistent consonant across all contexts:
- **Between two vowels:** /ğ/ is realized as the voiced velar fricative /ɣ/ — e.g., *ağıl* /aɣɯl/ (reason)
- **Word-finally or before a consonant:** /ğ/ is typically realized as compensatory lengthening /ː/ of the preceding vowel — e.g., *dağ* /daː/ (mountain), *bağlı* /baːlɯ/ (closed)
- In rapid speech, the fricative realization may also occur in non-intervocalic positions in some dialects

**Final obstruent devoicing.** Azerbaijani, like Turkish and many other Turkic languages, exhibits word-final devoicing of voiced obstruents: /b/ → /p/, /d/ → /t/, /g/ → /k/ at word boundaries. However, this alternation is not consistently reflected in spelling (unlike in Turkish, which does reflect it orthographically in some cases), and its application is partly lexicalized. The current system applies final devoicing as a default rule.

**Nasal assimilation.** The nasal /n/ assimilates in place of articulation to a following velar consonant: /n/ → /ŋ/ before /k/, /q/, /g/, /ğ/ — e.g., *rəng* /ræŋ/ (color), *sənki* /sæŋci/ (as if).

**Geminate consonants.** Double consonants in orthography represent long (geminate) consonants in pronunciation — e.g., *amma* /amːa/ (but/however), *əlli* /æliː/ (fifty).

### 2.1.5 Vowel Harmony

Vowel harmony is a defining typological feature of Turkic languages. In Azerbaijani, vowel harmony operates primarily on the front/back dimension: vowels within a word (root plus suffixes) must agree in frontness or backness. Rounded vowels additionally condition rounding harmony in certain suffix classes.

The vowel harmony classes are:
- **Back vowels:** a, ı, o, u
- **Front vowels:** e, ə, i, ö, ü

When a suffix is attached to a root, its vowel must match the harmony class of the root's final vowel. For example, the progressive suffix /-ır/-ir/-ur/-ür selects:
- *gəlir* (he/she comes) — root *gəl* has front vowel /ə/ → suffix vowel /i/ (front)
- *gedir* (he/she goes) — root *get* has front vowel /e/ → suffix vowel /i/ (front)
- *alır* (he/she takes) — root *al* has back vowel /a/ → suffix vowel /ı/ (back)
- *oxuyur* (he/she reads) — root *oxu* has back vowel /u/ → suffix vowel /u/ (back rounded)

Vowel harmony has two implications for TTS: (1) it is largely already encoded in the orthography, so the G2P module need not itself predict harmonized vowels for most words; (2) it provides a useful cross-check for identifying loanwords, which often violate harmony (e.g., *kompüter* — a back vowel /o/ followed by a front vowel /y/) and may require special handling.

### 2.1.6 Syllable Structure

The canonical Azerbaijani syllable structure is **(C)V(C)(C)**, where V is a vowel nucleus, and onset and coda consonants are optional. Key constraints:
- Every syllable has exactly one vowel nucleus.
- Complex onsets (CC-) are restricted to loanwords.
- Complex codas (up to -CC) occur in native vocabulary: *məktəb* (school) = /mæk.tæp/.
- Syllabification follows the **onset-maximization principle**: in a consonant cluster between two vowels, as many consonants as possible are assigned to the onset of the following syllable, subject to well-formedness constraints.

For stress assignment and prosodic modeling, accurate syllabification is essential.

### 2.1.7 Stress

Azerbaijani lexical stress is **primarily final** — the default stress position is on the last syllable of the word, a pattern shared with Turkish. However, Azerbaijani exhibits a larger set of systematic exceptions than Turkish (Salimi, n.d.):

- **Interrogative clitic particles** (*mi*, *mı*, *mu*, *mü*) do not receive stress; stress remains on the word they attach to.
- **The negative copula** *deyil* (is not) is stressed on the first syllable: *DEY-il*.
- **Negation suffix** *-ma/-mə* shifts stress to the penultimate syllable: *get-mə-di* → *GET-mə-di* (didn't go).
- **Certain postpositions** (*üçün*, *ilə*, *kimi*, etc.) are phonologically clitic and unstressed.
- **Some discourse particles and adverbs** (*yalnız*, *bəlkə*, *heç*) carry initial stress.
- **Loanwords** (especially from Russian and English) may retain their original stress pattern.

---

## 2.2 System Architecture

### 2.2.1 Design Philosophy

The proposed system follows the **modular pipeline** architecture that has been standard in TTS research since the Festival system (Taylor et al., 1998). In this architecture, the conversion from text to speech is decomposed into a sequence of independent modules, each with a well-defined input/output interface. This design offers several advantages for a rule-based system:

- Each module can be developed, tested, and improved independently.
- The intermediate representations between modules (normalized text, phoneme sequences, stress-annotated sequences, prosodic annotations) are human-readable and interpretable.
- New linguistic rules can be added to a specific module without affecting other modules.
- The system can be partially run (e.g., to produce IPA output without audio) for linguistic analysis purposes.

### 2.2.2 Pipeline Overview

The system consists of five processing stages, as illustrated in the following pipeline:

```
Input Text (Azerbaijani)
        │
        ▼
┌───────────────────────┐
│  1. Text Normalization │  text_normalizer.py
│  Numbers, abbrevs,    │
│  symbols → words      │
└──────────┬────────────┘
           │  Normalized text
           ▼
┌───────────────────────┐
│  2. G2P Conversion    │  g2p_converter.py
│  Graphemes → IPA      │
│  Syllabification      │
└──────────┬────────────┘
           │  Word objects with phoneme sequences
           ▼
┌───────────────────────┐
│  3. Stress Assignment │  stress_assigner.py
│  Lexical + phrasal    │
│  stress marking       │
└──────────┬────────────┘
           │  Stress-annotated words
           ▼
┌───────────────────────┐
│  4. Prosody Engine    │  prosody_engine.py
│  Pitch accents,       │
│  durations, pauses    │
└──────────┬────────────┘
           │  Prosody annotations (SSML / espeak markup)
           ▼
┌───────────────────────┐
│  5. Synthesizer       │  synthesizer.py
│  espeak-ng backend    │
│  WAV audio output     │
└──────────┬────────────┘
           │
           ▼
      Output WAV
```

### 2.2.3 Module Descriptions

**Module 1: Text Normalization (`text_normalizer.py`)**

This module converts non-standard words (NSWs) in the input text to their fully expanded, pronounceable Azerbaijani form. NSWs are lexical items that cannot be pronounced by a phoneme-level G2P converter without first being expanded: numerals, abbreviations, symbols, dates, times, and Roman numerals.

The text normalizer applies the following processing steps in order:

1. *Punctuation normalization:* Converts Unicode quotation marks, dashes, and ellipses to normalized ASCII equivalents.
2. *Symbol expansion:* Replaces currency symbols (₼, $, €), unit symbols (km, °C), and special characters (&, @, #) with their Azerbaijani spoken forms.
3. *Date normalization:* Converts DD.MM.YYYY patterns to their spoken form (e.g., *15.06.2024 → on beşinci iyun iki min iyirmi dördüncü il*).
4. *Time normalization:* Converts HH:MM patterns to spoken form (e.g., *09:30 → doqquz saat otuz dəqiqə*).
5. *Ordinal number expansion:* Converts numbers with ordinal suffixes (e.g., *1-ci, 3-üncü*) to their word form.
6. *Cardinal number expansion:* Converts standalone cardinal numbers to Azerbaijani number words.
7. *Roman numeral expansion:* Converts Roman numerals in unambiguous contexts to their Arabic-digit equivalent and then to words.
8. *Abbreviation expansion:* Replaces known abbreviations with their full forms.

The number-to-words conversion for Azerbaijani follows a simple compositional structure: Azerbaijani numbers are built from units, tens, hundreds, thousands, and millions in a left-to-right, most-significant-first order. For example, 1,947 → *min doqquz yüz qırx yeddi*. Ordinal suffixes are selected by vowel harmony with the last vowel of the number word.

**Module 2: G2P Converter (`g2p_converter.py`)**

The G2P converter maps the normalized Azerbaijani text to IPA phoneme sequences. It processes the input character by character, applying:

- *Base phoneme mapping:* Each vowel and consonant grapheme is mapped to its default IPA phoneme (9 vowels, 23 consonants).
- *Context-sensitive rules:* Palatalization of /g/ and /k/ before front vowels; allophonic rules for /ğ/ (intervocalic → /ɣ/, word-final → /ː/); nasal velarization (/n/ → /ŋ/ before velars).
- *Post-processing rules:* Geminate consonant merging (double letters → long consonant); final obstruent devoicing; nasal assimilation before bilabials.
- *Syllabification:* Division of the phoneme sequence into syllables using the onset-maximization algorithm.

The output is a sequence of `Word` objects, each containing a list of `Phoneme` objects annotated with their IPA symbol, vowel/consonant status, and syllable index.

**Module 3: Stress Assigner (`stress_assigner.py`)**

The stress assigner operates on the `Word` objects produced by the G2P converter. It applies a priority-ordered rule hierarchy:

1. *Unstressed function words:* Postpositions, conjunctions, and clitic particles are marked as unstressed.
2. *Lexical exceptions:* Words with irregular stress patterns (e.g., *deyil* → first syllable) are handled by an exception list.
3. *Negation suffix rule:* Words ending in *-ma/-mə* (negation) receive stress on the penultimate syllable.
4. *Default rule:* All remaining words receive stress on the final syllable.

The stress assigner additionally applies *phrasal stress* rules: demoting function words, identifying the focus position (the content word immediately before the main verb), and applying appropriate pitch accent labels.

**Module 4: Prosody Engine (`prosody_engine.py`)**

The prosody engine generates suprasegmental annotations for the stress-marked word sequence:

- *Sentence type detection:* Classification into declarative, yes/no question, wh-question, exclamatory, or imperative based on surface markers.
- *Intonation pattern selection:* Each sentence type is associated with a ToBI-style intonation pattern specifying boundary tones (L%, H%) and pitch accent types (H*, L+H*, L*).
- *Phone duration prediction:* Each phoneme is assigned a duration estimate based on phoneme type, stress, position in syllable, and position in phrase, scaled by the selected speaking rate.
- *Pause insertion:* Pauses of appropriate duration are inserted at punctuation boundaries, conjunction positions, and long-phrase boundaries.

**Module 5: Synthesizer (`synthesizer.py`)**

The synthesizer translates the prosodic annotations into audio using the espeak-ng speech synthesis engine. espeak-ng is invoked as a subprocess, receiving either:
- The normalized text with espeak markup (pause and stress annotations), or
- A direct IPA phoneme string in espeak's IPA input mode.

espeak-ng produces WAV audio at the configured sample rate (22,050 Hz by default). The module adjusts espeak-ng parameters (speed, pitch, amplitude) based on the sentence type and speaking style configuration.

### 2.2.4 Data Representations

The system uses three intermediate data structures as interchange formats between modules:

**`Phoneme`:** A single phoneme with fields: `symbol` (IPA string), `grapheme` (source character), `is_vowel`, `is_stressed`, `syllable_index`.

**`Word`:** A word with fields: `graphemes` (original form), `phonemes` (list of Phoneme), `syllables` (list of phoneme lists), `stressed_syllable` (index of stressed syllable, -1 if unstressed).

**`SentenceAnnotation`:** Full prosodic annotation for a sentence: `words`, `sentence_type`, `phone_annotations` (list of ProsodyAnnotation), `pauses_ms` (mapping of word index to pause duration).

---

## 2.3 Linguistic Rule Design

### 2.3.1 G2P Rule Design Principles

The G2P rule set was designed according to the following principles:

1. **Completeness:** Every character in the Azerbaijani Latin alphabet must have a well-defined mapping, including context-sensitive alternatives.
2. **Priority ordering:** When multiple rules could apply to the same character, rules are ordered by specificity: context-sensitive rules take priority over default mappings.
3. **Phonological grounding:** Every rule must be justified by phonological evidence from published descriptions of Azerbaijani (Salimi, n.d.; Cambridge Core, n.d.; Comparative Analysis of Azerbaijani and English Phonetic Systems, 2024).
4. **Loanword handling:** The default rules handle native Azerbaijani vocabulary; loanwords that deviate from native phonological patterns may require an exception dictionary in future work.

The context-sensitive rules are specified as ordered conditions: the rule checks a phoneme's left and right neighbors (and, for some rules, position in word) before applying the context-sensitive mapping.

### 2.3.2 Stress Rule Design

The stress rule hierarchy was derived from:
- The default final-syllable pattern documented in Azerbaijani grammars and phonological descriptions.
- Exception patterns documented in Salimi (n.d.) and corroborated by native speaker intuitions.
- Morphological considerations: negation suffixes, interrogative clitics, and postpositions are well-documented categories in Azerbaijani morphology (Comrie, 1981; various Azerbaijani grammars).

The rule hierarchy is implemented using a priority-ordered list: lower-priority rules (default final-stress) are only applied if no higher-priority rule matches the input word.

### 2.3.3 Prosody Rule Design

The prosody rules were designed to reflect the following features of Azerbaijani intonation, based on available phonetic descriptions:

- **Declarative sentences** in Azerbaijani typically exhibit a rise-fall pattern: pitch rises on or before the focused constituent and falls toward the end of the sentence (a pattern consistent with L+H* accents with L% boundary tone).
- **Yes/no questions**, marked by the interrogative particle *mi/mı/mu/mü*, exhibit a rising boundary tone (H%) — a pattern consistent with cross-linguistic typological tendencies for polar questions.
- **Wh-questions** typically exhibit a high peak on the wh-word followed by a falling tail, similar to declarative intonation.
- **Exclamatory sentences** exhibit a wider pitch range and a sharp fall at the sentence boundary.

Phone durations were estimated based on cross-linguistic patterns for Turkic languages (Multilingual Speech Recognition for Turkic Languages, 2023), scaled to match the phoneme type classifications documented in the prosody rules file. Speaking rate was set at 140 words per minute for the neutral style, consistent with measured Azerbaijani read speech rates.
