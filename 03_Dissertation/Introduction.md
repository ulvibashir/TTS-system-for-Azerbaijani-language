# Introduction

## Motivation

Speech is the most natural and efficient medium of human communication. The ability to convert written text to spoken language automatically — text-to-speech (TTS) synthesis — has become a critical component of modern human-computer interaction, enabling accessibility tools for visually impaired users, voice assistants, audiobook generation, navigation systems, and language learning applications. For the majority of the world's languages, however, high-quality TTS technology remains unavailable. Azerbaijani, the official language of the Republic of Azerbaijan and spoken by approximately 35 million people worldwide, is one such language.

While neural TTS systems developed over the last decade have achieved near-human speech quality for major languages such as English, Mandarin Chinese, and German, these systems depend on the availability of large, carefully recorded speech corpora and substantial computational infrastructure for training. For Azerbaijani, such resources are extremely limited. A handful of commercial and research systems exist (most notably the system developed by Samir Rustamov and the multilingual Turkic TTS system from IS2AI; see References), but no openly available, well-documented system with a transparent linguistic foundation has been published.

This dissertation addresses this gap by developing a rule-based TTS system for North Azerbaijani. The rule-based paradigm was selected deliberately: it requires no speech training data, its internal workings are fully transparent and linguistically grounded, and it can be developed and refined by anyone with knowledge of Azerbaijani phonology — without access to GPU clusters or large datasets. It also provides a meaningful academic contribution by documenting, for the first time in a single system, the phonological and prosodic rules of Azerbaijani as they apply to speech synthesis.

## Research Questions

This dissertation is guided by three central research questions:

1. **To what extent can the phonological and prosodic properties of North Azerbaijani be encoded as explicit computational rules sufficient for intelligible TTS synthesis?**
2. **What are the principal linguistic challenges specific to Azerbaijani that a rule-based TTS system must address, and how can they be resolved systematically?**
3. **How does the intelligibility and naturalness of a rule-based Azerbaijani TTS system compare against available baselines?**

## Scope and Limitations

This work focuses on **North Azerbaijani** as spoken in the Republic of Azerbaijan, using the Latin-based orthography adopted in 1992. South Azerbaijani (spoken in Iran) and dialectal variation are outside the scope of this dissertation. The system targets read speech in standard register and does not model speaking style variation, emotional prosody, or speaker identity.

The acoustic synthesis backend relies on espeak-ng, an open-source formant-based synthesis engine, which places a ceiling on the naturalness of the output that is characteristic of all formant synthesizers. The primary contribution of this work is the linguistic front-end — the rule system governing text normalization, G2P conversion, stress assignment, and prosody generation — rather than acoustic modeling per se.

## Contributions

The principal contributions of this dissertation are:

1. A fully implemented, open-source, rule-based TTS pipeline for North Azerbaijani.
2. A comprehensive, formally specified Azerbaijani G2P rule set derived from phonological literature.
3. A documented Azerbaijani stress assignment system encoding both default and exception patterns.
4. A prosody rule base encoding Azerbaijani sentence-type-specific intonation, duration, and pause patterns.
5. An Azerbaijani text normalization module covering numbers, ordinals, abbreviations, dates, times, and symbols.
6. An evaluation of the system's intelligibility on a phonetically balanced test set.

## Dissertation Structure

The remainder of this dissertation is organized as follows. **Chapter 1** reviews the general field of TTS synthesis, tracing its evolution from rule-based formant synthesis to modern neural approaches, and discusses the advantages and limitations of the rule-based paradigm. **Chapter 2** describes the Azerbaijani language as it pertains to speech synthesis — its phonological inventory, morphological structure, stress patterns, and prosodic characteristics — and presents the architecture and linguistic rule design of the proposed system. **Chapter 3** details the implementation, presents the evaluation methodology and results, and discusses the findings in the context of related work. The dissertation concludes with a summary of contributions and directions for future research.
