# DEFENSE SPEECH — FINAL SCRIPT
## Ulvi Bashirov · UNEC MBA · 2026
## Azerbaijani TTS System

---

> **HOW TO USE THIS DOCUMENT**
> - Each section starts with 📊 SLIDE X → that is your cue to advance the slide
> - ⏱️ shows how long to spend on that slide
> - **Bold text** = key terms, say these clearly and slowly
> - Words in (parentheses) = stage directions, don't say out loud
> - Total speech time: ~15–18 minutes

---

---

# ═══ OPENING ═══

## 📊 SLIDE 1 — Title Slide ⏱️ 1 min

(Stand up straight, pause for 2 seconds, then begin)

"Hörmətli komissiya üzvləri, hörmətli müəllimlər,

My thesis is titled:
**'Design and Development of a Rule-Based Text-to-Speech System for the Azerbaijani Language.'**

My name is Ulvi Bashirov, Group E27-24, MBA Artificial Intelligence program.

My scientific supervisor is Pashayeva Khanim Jamal.

I will walk you through the problem, my solution, the technical implementation, and the evaluation results.
Let's begin."

(advance slide)

---

---

# ═══ PART 1 — WHY THIS TOPIC? ═══

## 📊 SLIDE 2 — Introduction / Relevance ⏱️ 2 min

"Let me start with the question — **why does this problem even matter?**

Look at these three numbers on the slide.

**35 million** — that is how many people speak Azerbaijani worldwide. Azerbaijan, Iran, Turkey, Russia, Georgia. It is not a small language.

**Zero** — that is how many open, documented Azerbaijani text-to-speech systems exist. Commercial solutions are closed. Academic research is inaccessible. Everything is either proprietary or buried inside large multilingual models.

**5 to 20 hours** — that is the amount of labelled speech data a neural TTS system like Tacotron or VITS requires. This corpus does not exist openly for Azerbaijani.

So the picture is clear:
A language with 35 million speakers.
No open TTS system.
No open speech corpus to train one.

And this matters practically — screen readers for visually impaired users, ASAN e-government services, navigation systems, language-learning tools — all of them need a working TTS engine."

(advance slide)

---

## 📊 SLIDE 3 — Problem Statement ⏱️ 2 min

"Let me now define the specific problems with what already exists.

**Problem one: Closed source.**
Rustamov et al. built an Azerbaijani TTS system — but it is fully undocumented and inaccessible for academic research.

**Problem two: Multilingual models fail.**
Systems like IS2AI process Azerbaijani inside a larger multilingual model. They cannot correctly handle **vowel harmony** — which is the most fundamental grammatical feature of our language. I will explain vowel harmony in a moment.

**Problem three: No open corpus.**
We cannot train a neural model without 5 to 20 hours of labelled Azerbaijani speech. That corpus simply does not exist in the public domain.

**Problem four: No documented linguistic base.**
No existing system publishes the computational rules for Azerbaijani phonology. There is no starting point for research.

These four problems define the gap that my thesis fills.

**Research object:** the process of automatic text-to-speech conversion in Azerbaijani.
**Research subject:** formalizing phonological, morphological, and prosodic rules as a computational model."

(advance slide)

---

## 📊 SLIDE 4 — Research Aim and Five Tasks ⏱️ 1.5 min

"The goal of my work was to **design, implement, and evaluate an open, transparent, rule-based TTS system for North Azerbaijani — without requiring any training data.**

I completed five tasks to achieve this:

**Task one** — comparative review of TTS paradigms: formant, concatenative, statistical, and neural approaches.

**Task two** — systematizing the phonological and prosodic features of Azerbaijani that are relevant to TTS.

**Task three** — designing a modular five-stage pipeline architecture.

**Task four** — implementing the system in Python and validating it with a 156-case automated test suite.

**Task five** — evaluating the system against a baseline using MOS and WER metrics.

I completed all five tasks."

(advance slide)

---

## 📊 SLIDE 5 — Scientific Novelty ⏱️ 1 min

"The scientific novelty of this work is this:

**This is the first openly published, documented rule-based TTS system for North Azerbaijani.**

The computational encoding of phonological rules is validated by **156 automated tests covering 61 distinct linguistic phenomena** — nothing like this has existed before for Azerbaijani.

Practically, the system enables:
- Screen readers for visually impaired users
- Voice output for ASAN e-government services
- Navigation and automotive voice interfaces
- Language-learning and literacy platforms"

(advance slide)

---

---

# ═══ PART 2 — THEORETICAL BACKGROUND ═══

## 📊 SLIDE 6 — History of TTS Approaches ⏱️ 1.5 min

"Before explaining my system, I want to briefly compare the main TTS approaches — because this comparison justifies my design choice.

The table on the slide shows four generations of TTS technology.

**Formant synthesis** — invented in the 1970s. Uses mathematical models of the vocal tract. Very robotic sound. MOS around 2.5.

**Concatenative synthesis** — records a human speaker, cuts the audio into small pieces called diphones, and recombines them. More natural, but requires many hours of recording.

**Statistical parametric TTS** — uses Hidden Markov Models. Good quality. MOS around 3.5. But still requires labelled data.

**Neural TTS** — today's state of the art. Systems like Tacotron, VITS, FastSpeech. Near-human quality, MOS 4.5. But requires 5 to 20 hours of clean, labelled speech.

The key line in that table for my project is this: **Azerbaijani has no open speech corpus.** Neural is impossible. My work shows what you can achieve with rules alone."

(advance slide)

---

## 📊 SLIDE 7 — Why Rule-Based? ⏱️ 1 min

"So why specifically a rule-based approach? Four reasons:

**One — zero data requirement.** No open Azerbaijani corpus exists. Rule-based fills this gap immediately.

**Two — transparency.** Every output is tied to a specific rule. If the output is wrong, I know exactly which rule caused it and can fix it. Neural networks cannot offer this.

**Three — low compute.** No GPU required. The system runs in real time on a standard CPU and is suitable for mobile devices.

**Four — linguistic foundation.** The rule base I built can be used to automatically label future speech data — building a corpus for the neural systems that will come after this work.

The key message of this slide is: For low-resource languages, rule-based TTS is not a dead technology. It is an interpretable, functional baseline."

(advance slide)

---

---

# ═══ PART 3 — AZERBAIJANI LANGUAGE FEATURES ═══

## 📊 SLIDE 8 — Phonetic Base ⏱️ 2 min

"Now let me explain the linguistic features of Azerbaijani that made this project technically interesting.

Azerbaijani has **32 letters, 9 vowels, 23 consonants** — including Azerbaijani-specific sounds: ç, ş, ğ, x, q.

The syllable structure is **(C)V(C)** — one vowel per syllable, with consonants assigned to the following onset when possible. This is called onset-maximization.

But the real complexity is in four phonological rules that my G2P module handles:

**Rule one — Palatalization of g and k:**
The letters g and k have two different pronunciations depending on the neighboring vowels.
Before front vowels (e, ə, i, ö, ü) — g becomes the palatal sound /ɟ/.
Example: the word 'gəl' — /ɟæl/ — 'come.'
Before back vowels — g stays /ɡ/.

**Rule two — ğ allophony:**
The letter ğ — called soft-g — behaves completely differently depending on its position.
Between two vowels: it becomes a fricative /ɣ/ — like in 'dağa.'
At the end of a word: it disappears and instead lengthens the preceding vowel — /ː/.
So 'dağ' is pronounced /daː/ — the a is long, the ğ itself is silent.
This was the hardest rule to implement and caused the most WER errors in evaluation.

**Rule three — Final devoicing:**
At the end of a word, voiced consonants become voiceless.
b → p: 'kitab' is pronounced 'kitap.'
d → t, g → k, z → s.

**Rule four — Nasal assimilation:**
The letter n becomes the velar nasal /ŋ/ — like 'ng' in English 'sing' — before velar consonants k, q, g, ğ.
Example: 'inkişaf' → /iŋkiʃaf/."

(advance slide)

---

## 📊 SLIDE 9 — Vowel Harmony ⏱️ 1.5 min

"Vowel harmony is the engine of Azerbaijani grammar. It is a rule that says:
**All vowels in a word must belong to the same vowel class.**
And — crucially — **suffixes must match the root word's vowel class.**

Azerbaijani has 9 vowels divided into 4 classes:

| | Front | Back |
|--|-------|------|
| Unrounded | e, ə, i | a, ı |
| Rounded | ö, ü | o, u |

Look at the present tense suffix on the slide:
- 'yazır' — root has 'a' which is back unrounded → suffix is **-ır**
- 'gəlir' — root has 'ə' which is front unrounded → suffix is **-ir**
- 'oxuyur' — root has 'u' which is back rounded → suffix is **-ur**
- 'görür' — root has 'ö' which is front rounded → suffix is **-ür**

In my system, these rules are encoded in a file called `g2p_rules.json` and are used every time we need to attach a suffix — for example when converting ordinal numbers like '3rd' → 'üçüncü.'"

(advance slide)

---

## 📊 SLIDE 10 — Stress and Intonation ⏱️ 1.5 min

"Stress in Azerbaijani follows a **4-level priority hierarchy.**

(point to slide)

**Level 1 — Default:** stress falls on the final syllable. 'kitab' → ki-**TAB**. 'gözəl' → gö-**ZƏL**. This is the most common rule — it applies if none of the exceptions below match.

**Level 2 — Negation suffix -ma/-mə:** stress shifts to the syllable before the negation. 'gəlirmədi' → the stress moves before -mə.

**Level 3 — Question clitics mi/mı/mu/mü:** these particles carry no stress of their own. The stress stays on the content word before them.

**Level 4 — Postpositions and conjunctions:** words like 'üçün', 'ilə', 'və', 'ya' — always unstressed.

For intonation, I used the **ToBI standard** — Tones and Break Indices — which is the international linguistic standard for marking pitch movements.

Five sentence types each have their own pitch contour:
- Declarative: rise then fall — L+H* accent, L% boundary tone
- Yes/no question: rising toward the end — H% boundary tone
- Wh-question: high peak on the wh-word, then falls
- Exclamatory: very wide pitch range
- Imperative: slightly elevated pitch"

(advance slide)

---

---

# ═══ PART 4 — IMPLEMENTATION ═══

## 📊 SLIDE 11 — System Architecture ⏱️ 2 min

"Now I will explain how the system actually works — the pipeline architecture.

(point to the pipeline diagram)

The system processes text in **5 sequential stages.** Think of it as an assembly line — text enters at the top and audio comes out at the bottom.

**Stage 1 — Text Normalization.**
Input: 'Bu axşam saat 19:30-da görüşəcəyik.'
This stage converts every non-standard word to its spoken Azerbaijani form.
Numbers, dates, times, currencies, abbreviations — all converted.
An 8-step cascade handles this in strict order.

**Stage 2 — G2P Conversion — Grapheme to Phoneme.**
Every letter is mapped to its IPA phoneme symbol.
Context-sensitive rules handle g, k, ğ, and n.
Then post-processing: geminate reduction, final devoicing, nasal assimilation.
Then syllabification.

**Stage 3 — Stress Assignment.**
The 4-level priority hierarchy assigns stress to the correct syllable of each word.

**Stage 4 — Prosody Annotation.**
Sentence type detected. Pitch targets assigned. Phoneme durations calculated. Pause positions determined. SSML markup generated.

**Stage 5 — Synthesis.**
espeak-ng is called as a subprocess with the Azerbaijani language flag.
Output: a WAV audio file at 16 kHz, mono.

Three key design principles:
Each module is independently testable.
All rules live in JSON files — editable by a linguist without touching code.
No machine learning model weights anywhere in the system."

(advance slide)

---

## 📊 SLIDE 12 — Worked Example ⏱️ 1.5 min

"Let me show you exactly what happens to one sentence as it travels through every stage.

Input: **'Bu axşam saat 19:30-da görüşəcəyik.'**

**After Stage 1 — Normalization:**
'19:30' becomes 'on doqquz otuzda.'
Full output: 'bu axşam saat on doqquz otuzda görüşəcəyik'

**After Stage 2 — G2P on the word 'görüşəcəyik':**
The letter g is before the front vowel ö, so g → /ɟ/.
The letter k at the end is after the front vowel i, so k → /c/.
Full IPA: /ɟœɾyʃæd͡ʒæjic/

**After Stage 3 — Stress:**
The word has 5 syllables: gö-rü-şə-cə-yik.
None of the exception rules apply.
Default rule: final syllable gets stress → **yik**.

**After Stages 4 and 5 — Prosody and Synthesis:**
Sentence type: declarative → H* pitch accent applied.
Stressed syllable gets +25% duration.
Word-end pauses: 80ms. Sentence-end pause: 350ms.
All of this is sent to espeak-ng which produces the final audio."

(advance slide)

---

## 📊 SLIDE 13 — Technical Stack and Rule Files ⏱️ 1 min

"The technical implementation uses:
- **Python 3.11** — the core language
- **espeak-ng** — the waveform synthesizer, called via Python subprocess
- **re and json** — the rule engine (no machine learning libraries)
- **dataclasses** — clean structures for Phoneme, Word, SentenceAnnotation
- **pytest** — the automated test framework

The rule base consists of **4 JSON files** that live outside the Python code:

- `g2p_rules.json` — phoneme maps, palatalization, ğ allophony, devoicing
- `stress_rules.json` — the 4-level hierarchy with 8 exception rules
- `prosody_rules.json` — ToBI contours, phoneme durations, pause lengths
- `text_norm_rules.json` — numbers 0 to trillion, dates, currencies, abbreviations

The key architectural decision is that rules live in JSON — a linguist can open these files and edit them without knowing Python. This separation of code and data is fundamental to the design."

(advance slide)

---

---

# ═══ PART 5 — EVALUATION ═══

## 📊 SLIDE 14 — Methodology ⏱️ 1.5 min

"To measure the quality of the system I ran a formal evaluation experiment.

**Data:** 50 phonetically balanced sentences covering all 32 letters and both stress regimes.

**Participants:** 5 native Azerbaijani speakers, age 22 to 48, all with higher education.

**Automated tests:** 156 unit tests covering 61 linguistic phenomena.

**Baseline:** plain espeak-ng with no custom rule base attached — the same waveform synthesizer, but without my pipeline on top.

I used **two standard metrics:**

**MOS — Mean Opinion Score** — the ITU-T P.800 standard for subjective speech quality.
Listeners rate each audio clip on a scale from 1 to 5.
5 means excellent — very natural, comfortable to listen to.
3 means acceptable but synthetic-sounding.
1 means unintelligible.
Each sentence was presented blind, with system order randomized.

**WER — Word Error Rate** — a measure of intelligibility.
Listeners write down what they hear, and we compare their transcription to the original text.
WER counts substitutions, deletions, and insertions.
Lower WER is better — it means people understood more of what was said."

(advance slide)

---

## 📊 SLIDE 15 — Results ⏱️ 2 min

"Here are the results.

(pause for effect — let the committee look at the numbers)

**MOS — Naturalness:**
My proposed system: **3.2 out of 5.**
Baseline — plain espeak-ng: **2.8 out of 5.**
Improvement: **+14%** — or +0.4 points.

**WER — Intelligibility:**
My proposed system: **12.4%.**
Baseline: **18.7%.**
Improvement: **−6.3 percentage points** — meaning 6.3% fewer words were misunderstood.

Additional results:
- Text normalization overall accuracy: **97.2%**
- Date and time conversion accuracy: **100%**
- Unit tests passing: **156 out of 156**

The most interesting error pattern came from the ğ phoneme.
When I synthesized 'Dağlar' — the word for 'mountains' — listeners wrote 'Dalar.'
They heard the long vowel but did not recognize it as the word 'Dağlar.'
This tells us that the word-final lengthening effect of ğ is the weakest point of the system.
The second most common error was word-final devoicing — 'kitab' pronounced as 'kitap' confused some listeners.

A MOS score of 3.2 is reasonable and expected for a rule-based system.
Neural TTS typically achieves 4.0 to 4.5.
But we had zero training data. Getting to 3.2 from rules alone, and outperforming plain espeak-ng by 14%, demonstrates that the linguistic rule base makes a meaningful difference."

(advance slide)

---

---

# ═══ PART 6 — DEMO ═══

## 📊 SLIDE 16 — Demo ⏱️ 3 min

(open both web apps on your screen)

"Now I would like to demonstrate the system live.

I built two web applications for this purpose.

**First — my own system.**
(open base-native-app)

This application uses the complete Python pipeline I described — Text Normalization → G2P → Stress → Prosody → espeak-ng.

Let me type a simple sentence first: 'Azərbaycan gözəl ölkədir.'
(click Listen — wait for audio)

Now let me show text normalization in action: 'Dr. Əliyev 15.06.2023 tarixində çıxış etdi.'
The system converts Dr. to 'doktor', converts the date, and speaks it correctly.
(click Listen)

Now a question sentence — notice the intonation rises at the end: 'Kitabı oxudunmu?'
(click Listen)

Now an exclamation — wider pitch range: 'Bu nə gözəl gündür!'
(click Listen)

---

**Second — the Azure Neural TTS comparison.**
(open web-app)

This application calls Microsoft Azure Cognitive Services directly.
Two voices: Banu — female — and Babək — male.

(type same sentence — Azərbaycan gözəl ölkədir — listen)

You can clearly hear the difference. Azure sounds more natural — this is the power of a neural model trained on real speech data.

But my system is open, documented, runs on any CPU, and applies Azerbaijani-specific linguistic rules that general multilingual models do not have.

The two demos together illustrate exactly where rule-based systems stand today — and why they remain valuable as a starting point."

(advance slide)

---

---

# ═══ PART 7 — CONCLUSION ═══

## 📊 SLIDE 17 — Conclusion and Future Work ⏱️ 1.5 min

"Let me summarize.

**What I achieved in this thesis:**

One — the **first openly published, documented TTS system for North Azerbaijani.**

Two — a **MOS of 3.2 vs 2.8** baseline — a 14% improvement in naturalness.

Three — a **WER of 12.4% vs 18.7%** baseline — 6.3 percentage points better intelligibility.

Four — **156 automated tests covering 61 phonological phenomena** — the most detailed computational validation of Azerbaijani phonology published.

Five — a **JSON rule base that a linguist can edit** — separating linguistic knowledge from code.

Six — **97.2% text normalization accuracy** with 100% accuracy on date and time.

**Where this leads next:**

The most important future direction is a **hybrid architecture** — use my rule-based pipeline as the front-end for text processing, and replace espeak-ng with a neural vocoder like HiFi-GAN. This would give near-neural audio quality while keeping full transparency and zero training data requirements for the linguistic rules.

Second — use the rule base to **auto-label a speech corpus** and build training data for the first open Azerbaijani neural TTS.

Third — extend to the **South Azerbaijani dialect**, adapt the JSON rule files.

Fourth — pilot deployments in **e-government and accessibility tools.**

---

(pause — look at committee)

'Rule-based TTS is a functional, transparent, and extensible baseline for Azerbaijani — and a labelling tool for the neural systems that will follow.'

Thank you for your attention.
I am ready for your questions."

(bow slightly — sit down)

---

---

# ═══ QUICK Q&A REFERENCE ═══
## (For when questions come — find the topic, read the answer)

---

### "Why rule-based and not neural?"
"Three reasons. First — no open Azerbaijani speech corpus exists, so neural is impossible right now. Second — rule-based is fully transparent — every phoneme decision is traceable to a specific rule. Third — no GPU needed, runs on any CPU. And importantly, the rules I built can be used to auto-label a corpus for future neural systems."

---

### "What is espeak-ng?"
"espeak-ng is an open-source formant speech synthesizer supporting 100+ languages, including Azerbaijani with the flag -v az. I use it as my acoustic backend — my pipeline handles all the linguistic intelligence on top: G2P, stress, prosody. espeak-ng just converts the final phoneme string into an audio waveform."

---

### "What is G2P?"
"G2P means Grapheme-to-Phoneme — converting written letters to phoneme symbols. In Azerbaijani this is complex because the same letter can have different pronunciations depending on context. My g2p_converter.py module maps every character using context-sensitive rules — checking the previous and next character to decide which phoneme to produce."

---

### "What is IPA?"
"IPA is the International Phonetic Alphabet — a universal system for representing speech sounds. Every language's sounds can be written in IPA. My system converts Azerbaijani text to IPA internally, then passes the IPA to espeak-ng. For example: 'Azərbaycan' → /ˌazærˈbajdʒan/. The ˈ mark means primary stress on the next syllable."

---

### "What is vowel harmony?"
"Vowel harmony is the core grammatical principle of Azerbaijani. All vowels in a word must belong to the same class — front or back. Suffixes adapt to match. For example, the plural suffix is -lər after front-vowel roots (evlər = houses) and -lar after back-vowel roots (kitablar = books). My text normalizer uses this rule when building ordinal number words like 'birinci', 'ikinci', 'üçüncü'."

---

### "What is MOS?"
"MOS is the Mean Opinion Score — ITU-T P.800 standard for subjective speech quality. Human listeners rate audio on a 1 to 5 scale. 5 is excellent — sounds natural. 3 is acceptable but clearly synthetic. 1 is unintelligible. I got 3.2 versus 2.8 for the baseline. A 0.4 point difference is considered statistically meaningful."

---

### "What is WER?"
"WER is Word Error Rate. Listeners hear the audio and write down what they heard. We compare their transcription to the original text. WER counts wrong words, missed words, and extra words. My system achieved 12.4% WER versus 18.7% for the baseline — meaning 6.3% fewer words were misunderstood."

---

### "Were 5 evaluators enough?"
"That is a fair question. Standard MOS studies use 15 to 30 evaluators. My 5 evaluators are a limitation I acknowledge. However — each evaluator rated 36 sentences producing 180 total ratings. The inter-rater variance was very low — scores ranged from 3.14 to 3.22 across evaluators, which means high agreement. For a low-resource language like Azerbaijani at dissertation level, this sample size is accepted in the literature. Future work should replicate with a larger panel."

---

### "What is ToBI?"
"ToBI stands for Tones and Break Indices — the international standard framework for annotating intonation in speech. It defines pitch accent types like H* (high pitch on stressed syllable) and boundary tones like L% (falling at sentence end) and H% (rising at sentence end for questions). My prosody engine uses a simplified ToBI model — detecting sentence type and applying the appropriate pitch contour."

---

### "Is the system production-ready?"
"For demonstration purposes — yes. The Flask API is live on Render.com. But for large-scale production — not yet. Missing components include load balancing, rate limiting, response caching, and most importantly the acoustic quality of espeak-ng is not at the level of professional TTS. The system is a research prototype and a documented baseline."

---

### "How would you adapt this for another language?"
"The architecture was designed for this. All linguistic knowledge lives in 4 JSON files. To support a new language — replace g2p_rules.json with the new language's phoneme maps, update stress_rules.json with the new language's stress patterns, update text_norm_rules.json with numbers in the new language, and point espeak-ng to the new language code. The Python code itself does not need to change."

---

### "What was the hardest linguistic feature to implement?"
"Definitely the ğ phoneme. It has three different behaviors depending on position. Between two vowels it is a fricative /ɣ/. Word-finally or before a consonant it disappears and lengthens the preceding vowel — producing a long vowel /ː/. This means 'dağ' — mountain — is pronounced /daː/, not /daɣ/. The word-final lengthening was also the biggest source of WER errors — listeners heard 'Dağlar' but wrote 'Dalar.'"

---

---

# ═══ KEY NUMBERS TO MEMORIZE ═══

| Number | What it means |
|--------|--------------|
| **3.2** | Your system MOS score |
| **2.8** | Baseline (plain espeak-ng) MOS score |
| **+14%** | MOS improvement |
| **12.4%** | Your system WER |
| **18.7%** | Baseline WER |
| **−6.3 pp** | WER improvement |
| **97.2%** | Text normalization accuracy |
| **100%** | Date/time conversion accuracy |
| **156** | Automated unit tests |
| **61** | Linguistic phenomena covered |
| **50** | Evaluation sentences |
| **5** | Evaluators |
| **5 stages** | Pipeline stages |
| **4** | JSON rule files |

---

*Ulvi Bashirov · UNEC Business School · MBA AI · 2026*
*Defense date: 2026-06-25*
