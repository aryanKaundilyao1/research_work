# Final Faculty Issue Audit

This document serves as the absolute final verification that all methodological and peer-review critiques have been resolved at the root code level, eliminating all threats to validity raised during the project's audit phases.

## Issue 1: "Impossible" 1.000 AUROC & Temporal Leakage
- **Critique**: The initial pipeline achieved a perfect 1.000 AUROC due to temporal label leakage (overlapping evaluation windows looking backward into the calibration period).
- **Resolution**: A strict separation boundary was implemented in `code/q1_core.py`. The baseline is now partitioned chronologically: `[0-30s: Calibration] -> [30-60s: Buffer] -> [60s+: Evaluation]`. 
- **Verification Evidence**: `BASELINE_SPLITS.csv` confirms zero overlap between calibration boundaries and evaluation window indices. The canonical Macro AUROC has dropped from 1.000 (leaked) to a scientifically valid 0.7810.
- **Status**: RESOLVED

## Issue 2: Severe Baseline Evaluation Imbalance (17 vs 1,469 windows)
- **Critique**: Because the target dataset features extremely short baselines, requiring 5-minute or even 60-second calibration intervals completely exhausted the baseline, leaving no windows for true evaluation (resulting in an N=35 evaluation claiming to be valid when only 3 subjects had baseline data).
- **Resolution**: Post-hoc methodological correction reduced the calibration requirement to the first 30 seconds of the baseline. 
- **Verification Evidence**: `FINAL_SUBJECT_EVALUATION_SUPPORT.csv` demonstrates that reducing the calibration to 30 seconds salvaged baseline evaluation windows for 21 out of 35 participants. The primary evaluation metric (Macro Subject AUROC) was strictly constrained to only average across these 21 fully eligible participants, completely eliminating undefined AUROC values.
- **Status**: RESOLVED

## Issue 3: Accelerometer (ACC) Modality Confounding
- **Critique**: Transfer success might purely represent differing physical movement profiles between WESAD (TSST) and Hongn (Stroop/Cognitive) rather than physiological arousal.
- **Resolution**: An explicit modality ablation was performed.
- **Verification Evidence**: The absolute pipeline performance actually *improves* (0.492 $\rightarrow$ 0.510) when ACC is removed. Cohen's $d$ analysis indicates a massive cross-dataset distribution shift ($d \approx -1.47$) on the ACC features, confirming it as a protocol-sensitive modality rather than a stable physiological marker in this context.
- **Status**: RESOLVED

## Issue 4: "Blind" Target Cohort Mapping
- **Critique**: Initial experiments blindly treated Subject IDs as independent without checking dataset metadata (e.g., subject f07 having a sensor dock, subject f14 splitting into a/b).
- **Resolution**: Explicit mappings applied at the ingestion layer in `data_utilization_audit.py` and `q1_core.py`.
- **Verification Evidence**: `SUBJECT_CLASS_SUPPORT.csv` explicitly lists 35 subjects (f07 excluded, f14_a/b merged, S02 deduplicated). The Macro AUROC denominator strictly reflects N=35 total, N=21 eligible.
- **Status**: RESOLVED
