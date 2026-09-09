# DATASET IDENTITY AUDIT

This document establishes the verified identity of the dataset previously referred to as "Dataset B" or "Wearable Exam Stress Dataset".

## Dataset Identity
- **Dataset official name:** Wearable device dataset from induced stress and structured exercise sessions
- **Authors:** Andrea Hongn, Facundo Bosch, Lara Prado, and Paula Bonomini
- **Publication:** Scientific Data (published on PhysioNet)
- **Year:** 2025
- **DOI:** 10.13026/he0v-tf17
- **Repository:** PhysioNet
- **Version:** 1.0.1
- **Original total participants:** 36 (18 from V1: S01-S18, 18 from V2: f01-f18)

## Cohort Accounting
- **Stress-protocol participants:** 36 (All 36 participated in the stress protocol, either V1 or V2).
- **Participants actually available locally:** 36 (37 subdirectories in STRESS folder, due to `f14_a` and `f14_b`).
- **Participants excluded:** 1 (`f07`)
- **Final eligible participants:** 35
- **Reasons for exclusions:** `f07` was excluded because the protection dock was never removed from the wristband, completely covering the PPG (BVP) and TEMPERATURE sensors, rendering these physiological signals invalid for the full multimodal analysis.

## Protocol and Setup
- **Stress tasks:** 
  - V1: Stroop, TMCT, Real Opinion, Opposite Opinion, Subtract
  - V2: Subtract, TMCT, Real Opinion, Opposite Opinion, Stroop
- **Baseline tasks:** Baseline (and intermediate Rest periods)
- **Sensors:** Empatica E4 (Wristband)
- **Sampling rates:**
  - EDA: 4 Hz
  - TEMP: 4 Hz
  - BVP: 64 Hz
  - ACC: 32 Hz

## Conclusion on the Inconsistency
The previously noted "34 / 36 participant inconsistency" stems from data constraints in the underlying dataset (like connection losses for `f14` resulting in multiple files, and broken sensors for `f07`). The original dataset contains exactly 36 subjects (18 males 'S', 18 females 'f'), but quality control requires excluding `f07` due to physical sensor occlusion, resulting in exactly 35 viable subjects for full multimodal validation. No other participants have missing modalities in the STRESS protocol (though `S02` has some duplicated rows, it is loadable, and `f14` is split into `f14_a` and `f14_b`).
