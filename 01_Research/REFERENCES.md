# Research References

## Key Papers

### Rule-Based TTS
- 

### Azerbaijani Phonetics
- 

### Grapheme-to-Phoneme (G2P)
- 

### Prosody & Stress
- 

---

## Useful Links

### TTS Systems
- https://samirrustamov.com/en/products/

### Azerbaijani Language Resources
-

### Tools & Libraries
-

### Research Papers
- https://ieeexplore.ieee.org/document/8747154

---

## Citation Format
Using **APA 7** style for all references.

---

---
1. RULE-BASED TTS SYSTEMS (2020-2024)

1. A Novel End-to-End Turkish Text-to-Speech (TTS) System via Deep Learning

- Authors: Saadin Oyucu
- Year: 2023
- Venue: Electronics (MDPI), 12(8):1900
- DOI/URL: https://doi.org/10.3390/electronics12081900
- Relevance: First documented deep learning-based TTS system for Turkish using Tacotron 2 + HiFi-GAN structure, achieving MOS of 4.49. Highly relevant for understanding modern Turkish TTS which shares linguistic
features with Azerbaijani.

2. Towards Controllable Speech Synthesis in the Era of Large Language Models: A Survey

- Authors: Various (December 2024)
- Year: 2024
- Venue: arXiv
- DOI/URL: https://arxiv.org/html/2412.06602v1
- Relevance: Comprehensive survey covering evolution from rule-based TTS to neural approaches, providing historical context and comparison of rule-based formant synthesis with modern neural methods.

3. A Survey on Neural Speech Synthesis

- Authors: Xu Tan, Tao Qin, Frank Soong, Tie-Yan Liu
- Year: 2021
- Venue: arXiv:2106.15561
- DOI/URL: https://arxiv.org/abs/2106.15561
- Relevance: Comprehensive overview of TTS evolution from rule-based (formant synthesis, HMM-based) to neural approaches, essential for understanding architectural choices in TTS design.

---
2. AZERBAIJANI LANGUAGE TTS & NLP

4. Multilingual Text-to-Speech Synthesis for Turkic Languages Using Transliteration

- Authors: Rustem Yeshpanov, Saida Mussakhojayeva, Yerbolat Khassanov
- Year: 2023
- Venue: Interspeech 2023
- DOI/URL: https://github.com/IS2AI/TurkicTTS
- Relevance: Directly addresses Azerbaijani TTS using Tacotron2 + WaveGAN architecture for 10 Turkic languages including Azerbaijani, with IPA-based conversion module.

5. A Generative Phonology of Azerbaijani

- Authors: Hosseingholi Salimi
- Year: N/A (Dissertation)
- Venue: University of Florida
- DOI/URL: https://ufdcimages.uflib.ufl.edu/AA/00/05/27/76/00001/generativephonol00sali.pdf
- Relevance: Foundational linguistic analysis of Azerbaijani phonology essential for developing phonological rules for rule-based TTS system.

6. Comparative Analysis of Azerbaijani and English Phonetic Systems

- Authors: Various
- Year: 2024
- Venue: ResearchGate
- DOI/URL: https://www.researchgate.net/publication/384969855_Comparative_Analysis_of_Azerbaijani_and_English_Phonetic_Systems
- Relevance: Recent phonetic analysis of Azerbaijani's 9-vowel system and consonant inventory, critical for developing G2P conversion rules.

7. Azerbaijani (Phonetic Description)

- Authors: Various
- Year: N/A
- Venue: Journal of the International Phonetic Association, Cambridge Core
- DOI/URL: https://www.cambridge.org/core/journals/journal-of-the-international-phonetic-association/article/azerbaijani/EC9EF0910D4B8B6C24937E5C49F59A82
- Relevance: Authoritative IPA-based phonetic description of Azerbaijani with detailed acoustic analysis including F1, F2, F3 formant frequencies.

8. Open Foundation Models for Azerbaijani Language

- Authors: Various
- Year: 2024
- Venue: arXiv:2407.02337
- DOI/URL: https://arxiv.org/html/2407.02337v1
- Relevance: Recent work on Azerbaijani NLP introducing DOLLMA corpus (651.1M words) and datasets useful for text normalization and linguistic analysis.

9. MorAz: An Open-source Morphological Analyzer for Azerbaijani Turkish

- Authors: Various
- Year: 2019
- Venue: ResearchGate
- DOI/URL: https://www.researchgate.net/publication/331168185_MorAz_an_Open-source_Morphological_Analyzer_for_Azerbaijani_Turkish
- Relevance: Essential tool for handling Azerbaijani's agglutinative morphology, critical for text analysis in TTS preprocessing.

---
3. TURKISH/TURKIC LANGUAGE TTS (2018-2024)

10. Vowel Harmony: A Comparative Study of Turkey's and Azerbaijani Turkish

- Authors: Various
- Year: 2013
- Venue: Procedia - Social and Behavioral Sciences (ScienceDirect)
- DOI/URL: https://www.sciencedirect.com/science/article/pii/S1877042813001419
- Relevance: Comparative analysis of vowel harmony rules in Turkish and Azerbaijani, essential for developing phonological rules in rule-based TTS.

11. Multilingual Speech Recognition for Turkic Languages

- Authors: Various
- Year: 2023
- Venue: Information (MDPI), 14(2):74
- DOI/URL: https://www.mdpi.com/2078-2489/14/2/74
- Relevance: Recent work on Turkic language speech processing including phonetic patterns and acoustic modeling approaches applicable to TTS.

12. Multilingual End-to-End ASR for Low-Resource Turkic Languages with Common Alphabets

- Authors: Various
- Year: 2024
- Venue: Scientific Reports, Nature
- DOI/URL: https://www.nature.com/articles/s41598-024-64848-1
- Relevance: Recent 2024 research on phonetic and acoustic characteristics of Turkic languages including Azerbaijani, with insights on phoneme modeling.

13. The Development and Experimental Evaluation of a Multilingual Speech Corpus for Low-Resource Turkic Languages

- Authors: Various
- Year: 2024
- Venue: Applied Sciences (MDPI), 15(24):12880
- DOI/URL: https://www.mdpi.com/2076-3417/15/24/12880
- Relevance: Recent corpus development for Turkic languages providing data resources and evaluation methodologies for TTS systems.

14. Analytical Review of Phonological Patterns Across Turkic Languages

- Authors: Various
- Year: Recent
- Venue: Лингвоспектр (Lingvospektr)
- DOI/URL: https://lingvospektr.uz/index.php/lngsp/article/view/199
- Relevance: Comprehensive analysis of phonological patterns shared across Turkic languages, useful for understanding Azerbaijani phonology.

---
4. GRAPHEME-TO-PHONEME CONVERSION (2019-2024)

15. A Survey of Grapheme-to-Phoneme Conversion Methods

- Authors: Various
- Year: 2024
- Venue: Applied Sciences (MDPI), 14(24):11790
- DOI/URL: https://www.mdpi.com/2076-3417/14/24/11790
- Relevance: Comprehensive 2024 survey covering rule-based and data-driven G2P methods, essential for designing G2P component of rule-based TTS.

16. Grapheme-to-Phoneme Conversion with a Multilingual Transformer Model

- Authors: Vesik et al.
- Year: 2020
- Venue: SIGMORPHON 2020, ACL Anthology
- DOI/URL: https://aclanthology.org/2020.sigmorphon-1.7/
- Relevance: Transformer-based approach to G2P for multiple languages including insights applicable to agglutinative languages.

17. T5G2P: Text-to-Text Transfer Transformer Based Grapheme-to-Phoneme Conversion

- Authors: Various
- Year: 2024
- Venue: IEEE/ACM Transactions on Audio, Speech and Language Processing
- DOI/URL: https://dl.acm.org/doi/abs/10.1109/TASLP.2024.3426332
- Relevance: State-of-the-art 2024 G2P model achieving high accuracy across multiple languages, providing modern comparison baseline.

18. One Model to Pronounce Them All: Multilingual Grapheme-to-Phoneme Conversion With a Transformer Ensemble

- Authors: Various
- Year: 2020
- Venue: ResearchGate
- DOI/URL: https://www.researchgate.net/publication/343301889_One_Model_to_Pronounce_Them_All_Multilingual_Grapheme-to-Phoneme_Conversion_With_a_Transformer_Ensemble
- Relevance: Multilingual G2P approach relevant for low-resource languages, includes discussion of agglutinative language challenges.

19. PolyIPA - Multilingual Phoneme-to-Grapheme Conversion Model

- Authors: Various
- Year: 2024
- Venue: arXiv:2412.09102
- DOI/URL: https://arxiv.org/html/2412.09102v1
- Relevance: Recent 2024 model for phoneme-grapheme conversion using IPA, useful for understanding bidirectional G2P relationships.

20. Morpheme-Based Grapheme to Phoneme Conversion Using Phonetic Patterns

- Authors: Various
- Year: N/A
- Venue: ResearchGate
- DOI/URL: https://www.researchgate.net/publication/220316730_Morpheme-Based_Grapheme_to_Phoneme_Conversion_Using_Phonetic_Patterns_and_Morphophonemic_Connectivity_Information
- Relevance: Morpheme-based G2P approach specifically designed for agglutinative languages, highly relevant for Azerbaijani.

---
5. PROSODY & STRESS (2018-2024)

21. Voice Synthesis Improvement by Machine Learning of Natural Prosody

- Authors: Various
- Year: 2024
- Venue: Sensors (MDPI), 24(5):1624
- DOI/URL: https://www.mdpi.com/1424-8220/24/5/1624
- Relevance: Recent 2024 work on prosody modeling using LSTM neural networks, applicable to prosody prediction in rule-based systems.

22. PitchFlow: Adding Pitch Control to a Flow-matching Based TTS Model

- Authors: Sadekova et al.
- Year: 2024
- Venue: Interspeech 2024
- DOI/URL: https://www.isca-archive.org/interspeech_2024/sadekova24_interspeech.pdf
- Relevance: State-of-the-art 2024 research on pitch contour modeling and F0 control in TTS systems.

23. Technical Report: Impact of Duration Prediction on Speaker-specific TTS for Indian Languages

- Authors: Various
- Year: 2024
- Venue: arXiv:2507.16875
- DOI/URL: https://arxiv.org/html/2507.16875
- Relevance: Recent analysis of duration prediction strategies for agglutinative/morphologically complex languages similar to Azerbaijani.

24. The Interaction Between Vowel Quality and Intensity in Loudness Perception of Short Vowels in Mongolian

- Authors: Various
- Year: 2024
- Venue: Journal of Speech, Language, and Hearing Research
- DOI/URL: https://pubs.asha.org/doi/10.1044/2024_JSLHR-24-00366
- Relevance: 2024 study on stress perception in agglutinative language (Mongolian) providing insights for stress assignment rules.

---
6. TEXT NORMALIZATION (2019-2024)

25. PolyNorm: Few-Shot LLM-Based Text Normalization for Text-to-Speech

- Authors: Apple Machine Learning Research
- Year: 2024
- Venue: arXiv:2511.03080
- DOI/URL: https://arxiv.org/abs/2511.03080
- Relevance: Cutting-edge 2024 LLM-based approach to text normalization, showing evolution beyond rule-based methods for number-to-text, abbreviations.

26. Text Normalization and Inverse Text Normalization with NVIDIA NeMo

- Authors: NVIDIA
- Year: 2020-2024
- Venue: NVIDIA Technical Blog
- DOI/URL: https://developer.nvidia.com/blog/text-normalization-and-inverse-text-normalization-with-nvidia-nemo/
- Relevance: Production-grade text normalization system using weighted finite state transducers (WFST), essential reference for rule-based text preprocessing.

27. Text Normalization for Text-to-Speech

- Authors: Zhaorui Zhang
- Year: 2023
- Venue: Uppsala University (Thesis)
- DOI/URL: https://uu.diva-portal.org/smash/get/diva2:1764605/FULLTEXT01.pdf
- Relevance: Recent comprehensive thesis on text normalization specifically for TTS, covering number-to-text, abbreviations, special characters.

---
7. LOW-RESOURCE LANGUAGE TTS (2020-2024)

28. LRSpeech: Extremely Low-Resource Speech Synthesis and Recognition

- Authors: Xu, Tan et al.
- Year: 2020
- Venue: KDD 2020
- DOI/URL: https://www.semanticscholar.org/paper/LRSpeech:-Extremely-Low-Resource-Speech-Synthesis-Xu-Tan/fde4e53ba166567f3b9b977a866020f10a996c02
- Relevance: Seminal 2020 work on TTS for low-resource languages achieving 98% intelligibility with pre-training and transfer learning techniques.

29. Text-to-Speech System for Low-Resource Language Using Cross-Lingual Transfer Learning and Data Augmentation

- Authors: Various
- Year: 2021
- Venue: EURASIP Journal on Audio, Speech, and Music Processing
- DOI/URL: https://asmp-eurasipjournals.springeropen.com/articles/10.1186/s13636-021-00225-4
- Relevance: Practical approach using only 30 minutes of target language data, highly relevant for low-resource Azerbaijani TTS development.

30. CML-TTS: A Multilingual Dataset for Speech Synthesis in Low-Resource Languages

- Authors: Various
- Year: 2023
- Venue: Text, Speech, and Dialogue (Springer)
- DOI/URL: https://arxiv.org/abs/2306.10097
- Relevance: Recent 2023 dataset (3,176 hours) for low-resource TTS with methodology applicable to Azerbaijani corpus development.

31. Transfer Learning for Low-Resource, Multi-Lingual, and Zero-Shot Multi-Speaker Text-to-Speech

- Authors: Various
- Year: 2024
- Venue: IEEE/ACM Transactions on Audio, Speech and Language Processing
- DOI/URL: https://dl.acm.org/doi/10.1109/TASLP.2024.3364085
- Relevance: State-of-the-art 2024 transfer learning framework for multilingual low-resource TTS using self-supervised representations.

---
8. NEURAL TTS ARCHITECTURES (Comparison & Context)

32. VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech

- Authors: Kim et al.
- Year: 2021
- Venue: ICML 2021
- DOI/URL: https://arxiv.org/pdf/2106.06103
- Relevance: Influential end-to-end TTS model achieving MOS comparable to ground truth, important baseline for comparing with rule-based approaches.

33. Fine Tuning and Comparing Tacotron 2, Deep Voice 3, and FastSpeech 2 TTS Models in a Low Resource Environment

- Authors: Various
- Year: 2022
- Venue: IEEE Conference
- DOI/URL: https://ieeexplore.ieee.org/document/9915932/
- Relevance: Comparative study of neural TTS architectures in low-resource settings, finding Tacotron 2 achieved MOS 4.25±0.17.

34. HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis

- Authors: Various
- Year: 2020
- Venue: NeurIPS 2020
- DOI/URL: Referenced in multiple sources
- Relevance: State-of-the-art neural vocoder (MOS=4.36) achieving real-time performance, important for understanding modern vocoder architecture.

---
9. SPEECH QUALITY EVALUATION

35. Speech Quality Metrics and Evaluation: Measuring TTS Performance

- Authors: Various
- Year: 2020-2024
- Venue: Industry Resources
- DOI/URL: https://indextts2.online/blog/speech-quality-metrics-evaluation
- Relevance: Comprehensive guide to MOS, intelligibility, naturalness, and expressivity evaluation for TTS systems.

---
10. FOUNDATIONAL & SEMINAL WORKS

36. The Architecture of the Festival Speech Synthesis System

- Authors: Paul Taylor, Alan W. Black, Richard Caley
- Year: 1998
- Venue: ESCA Workshop on Speech Synthesis
- DOI/URL: https://www.cs.cmu.edu/~awb/papers/ESCA98_arch.pdf
- Relevance: Seminal paper on Festival TTS architecture, foundational reference for rule-based TTS system design with modular architecture.

37. Statistical Parametric Speech Synthesis (Review)

- Authors: Various
- Year: 2015-2019
- Venue: IEEE
- DOI/URL: https://ieeexplore.ieee.org/document/7282379
- Relevance: Comprehensive review of HMM-based statistical parametric synthesis, bridging rule-based and neural approaches.

38. Deep Learning-Based Expressive Speech Synthesis: A Systematic Review

- Authors: Various
- Year: 2024
- Venue: EURASIP Journal on Audio, Speech, and Music Processing
- DOI/URL: https://asmp-eurasipjournals.springeropen.com/articles/10.1186/s13636-024-00329-7
- Relevance: Recent 2024 systematic review of expressive TTS including prosody modeling, emotion, and speaking style control.

---
ADDITIONAL RESOURCES & TOOLS

39. The Phonemizer: Simple Text to Phones Converter for Multiple Languages

- Authors: bootphon
- Year: Ongoing
- Venue: GitHub
- DOI/URL: https://github.com/bootphon/phonemizer
- Relevance: Open-source G2P tool supporting multiple backends (espeak, festival), useful reference implementation for phoneme conversion.

40. A Mel Spectrogram Enhancement Paradigm Based on CWT in Speech Synthesis

- Authors: Various
- Year: 2024
- Venue: arXiv:2406.12164
- DOI/URL: https://arxiv.org/abs/2406.12164
- Relevance: Recent 2024 work on acoustic feature enhancement improving MOS by 0.14, relevant for acoustic modeling considerations.

---
Sources

- https://www.researchgate.net/figure/Text-To-Speech-system-architecture_fig1_241025907
- https://www.mdpi.com/2079-9292/12/8/1900
- https://github.com/IS2AI/TurkicTTS
- https://www.mdpi.com/2076-3417/14/24/11790
- https://aclanthology.org/2020.sigmorphon-1.7/
- https://www.mdpi.com/1424-8220/24/5/1624
- https://www.isca-archive.org/speechprosody_2020/
- https://arxiv.org/abs/2511.03080
- https://developer.nvidia.com/blog/text-normalization-and-inverse-text-normalization-with-nvidia-nemo/
- https://www.semanticscholar.org/paper/LRSpeech:-Extremely-Low-Resource-Speech-Synthesis-Xu-Tan/fde4e53ba166567f3b9b977a866020f10a996c02
- https://arxiv.org/abs/2306.10097
- https://dl.acm.org/doi/10.1109/TASLP.2024.3364085
- https://arxiv.org/pdf/2106.06103
- https://ieeexplore.ieee.org/document/9915932/
- https://ufdcimages.uflib.ufl.edu/AA/00/05/27/76/00001/generativephonol00sali.pdf
- https://www.cambridge.org/core/journals/journal-of-the-international-phonetic-association/article/azerbaijani/EC9EF0910D4B8B6C24937E5C49F59A82
- https://www.researchgate.net/publication/331168185_MorAz_an_Open-source_Morphological_Analyzer_for_Azerbaijani_Turkish
- https://www.nature.com/articles/s41598-024-64848-1
- https://www.sciencedirect.com/science/article/pii/S1877042813001419
- https://www.cs.cmu.edu/~awb/papers/ESCA98_arch.pdf
- https://arxiv.org/html/2412.06602v1
- https://arxiv.org/abs/2106.15561
- https://asmp-eurasipjournals.springeropen.com/articles/10.1186/s13636-024-00329-7
- https://www.isca-archive.org/interspeech_2024/sadekova24_interspeech.pdf
- https://arxiv.org/html/2407.02337v1
- https://huggingface.co/datasets/azcorpus/azcorpus_v0

