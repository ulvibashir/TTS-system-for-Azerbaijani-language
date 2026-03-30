# Gaps to Review

## Testing
- [ ] No automated test suite — `pytest` is in `requirements.txt` but no `tests/` directory exists
- [ ] No unit tests for any individual module (text_normalizer, g2p_converter, stress_assigner, etc.)
- [ ] No integration tests between pipeline stages
- [ ] No edge case coverage (empty strings, malformed input, unicode edge cases)
- [ ] No performance benchmarks

## Error Handling
- [ ] JSON rule file parsing has no validation — could fail silently on malformed rules
- [ ] No consistency checks across rule bases
- [ ] Missing bounds checking for `stressed_syllable` index access
- [ ] Some missing null/None guards in pipeline stages

## Performance
- [ ] Regex patterns in `text_normalizer.py` are not pre-compiled (recompiled on every call)
- [ ] No caching of converter/assigner instances between calls
- [ ] No batch processing mode for large text files

## Features / Functionality
- [ ] Synthesis output limited to WAV only (no MP3, OGG, etc.)
- [ ] No alternative synthesizer backends (Festival, MBROLA)
- [ ] No streaming synthesis capability
- [ ] No callback/progress mechanism for long synthesis tasks
- [ ] No speaker adaptation or voice cloning support
- [ ] No config file support in CLI (only hard-coded defaults)
- [ ] No batch file processing mode in CLI

## Code Quality
- [ ] Duplicate duration prediction logic — could be refactored into lookup tables
- [ ] Similar pitch accent assignment logic repeated — candidate for consolidation
- [ ] Logging uses only INFO level — no DEBUG split for verbose tracing
- [ ] No log file output (console only)

## Evaluation
- [ ] MOS study not yet complete — needs 5 native speakers, 50 phonetically balanced sentences
- [ ] WER intelligibility evaluation pending
- [ ] Acoustic quality ceiling set by espeak-ng (estimated MOS ~3.0–3.8 vs neural ~4.2–4.5)

## Linguistic Rules
- [ ] Formal linguistic validation of G2P, stress, and prosody rules not done
- [ ] No coverage of variant spellings or transliterations
- [ ] Loanword stress exceptions are incomplete (only a few lexical entries)
