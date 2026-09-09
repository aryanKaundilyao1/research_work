# Adversarial Review Simulation

**Reviewer Persona:** Hostile Reviewer 2 / Autonomous AI Methodology Auditor.
**Objective:** Attempt to reject the paper based on data leakage, class imbalance, domain shift confounding, protocol mismatch, N-inflation, or novelty claims.

## Attack 1: Temporal Data Leakage (Target-Label Leakage)
**Criticism:** The authors claim cross-dataset transfer success, but in time-series wearable data, taking a "baseline" often involves using data from the *entire* rest period. If the evaluation overlaps with this period, the model is predicting the past using the future.
**Severity:** FATAL
**Defense Location:** Section 4.9 explicitly states: "Baseline statistics were estimated from the first 30 s... The subsequent 30 s were discarded as a temporal buffer, and no 60-s evaluation window was permitted to begin before the end of this buffer."
**Resolution:** The criticism is invalidated. The methodology is strictly chronological.
**Status:** NOT VALID

## Attack 2: N-Inflation and Missing Baselines
**Criticism:** The target dataset (Hongn) has 36 participants, but the authors report a 0.781 AUROC based on 21 participants. The remaining participants are swept under the rug to inflate the metric. They should have an AUROC of 0.5 or undefined, completely breaking the "N=35" claim.
**Severity:** MAJOR
**Defense Location:** Section 4.9 and 6.4 explicitly declare N=35 as the target cohort size, and mathematically define why 14 subjects were ineligible ("lacked post-calibration baseline windows and could not mathematically contribute to within-subject AUROC"). The primary metric is explicitly named as being calculated on the 21 eligible subjects. The remaining 14 subjects are NOT hidden.
**Resolution:** The text is transparent. The limitation is inherent to the dataset's short baseline duration, not a methodological deception.
**Status:** INHERENT LIMITATION

## Attack 3: Physical Movement Confounding (Accelerometer)
**Criticism:** The authors are just detecting that people sit still during baseline (rest) and move their hands during stress (Stroop/TSST). This isn't physiological stress; it's activity recognition.
**Severity:** FATAL
**Defense Location:** Section 6.3 directly addresses this. An ACC ablation was performed, revealing a Cohen's d shift of -1.47 (a massive covariate shift). The authors explicitly label ACC as a "protocol-sensitive modality." Removing it actually *improves* the absolute transfer performance.
**Resolution:** The authors preemptively caught and quantified the physical movement confound.
**Status:** NOT VALID

## Attack 4: Statistical Pseudoreplication
**Criticism:** The authors boast about 18.55 million observations and thousands of windows, running standard statistical tests on overlapping 60-second windows. This violates independence assumptions and guarantees a false p-value.
**Severity:** FATAL
**Defense Location:** Section 4.12 and 6.5 state the statistical unit is the *subject*, not the window. "subject-level bootstrapping (5000 iterations)" was utilized. The AUROC is a "Macro Subject AUROC", meaning the ROC curve is aggregated per participant before averaging.
**Resolution:** Pseudoreplication is avoided.
**Status:** NOT VALID

## Attack 5: Unfair Normalization Baseline Comparison
**Criticism:** The authors compare a relative model (trained on WESAD with relative features) to an absolute model. It's obvious the relative model wins. Did they tune hyperparameters for the relative model using the target dataset?
**Severity:** MAJOR
**Defense Location:** Section 4.9 states: "Target stress labels were strictly excluded from feature selection, scaling, model training, hyperparameter tuning, and threshold selection." The absolute model was also evaluated strictly without target labels.
**Resolution:** The comparison is fair and zero-shot.
**Status:** NOT VALID

## Attack 6: Novelty
**Criticism:** Z-scoring a baseline is not novel. It's been done for decades.
**Severity:** MINOR
**Defense Location:** Section 11 and Section 2.6 do not claim z-scoring is novel. They claim the *evaluation of label-free baseline calibration in a strict, un-leaked cross-dataset transfer setting* is the contribution.
**Resolution:** Novelty is correctly bounded.
**Status:** NOT VALID

## Summary
- **FATAL Criticisms Surviving:** 0
- **MAJOR FIXABLE Criticisms Surviving:** 0
- **INHERENT LIMITATIONS:** 1 (Target dataset class imbalance limiting N=21 eligible subjects). This is transparently disclosed.

**Conclusion:** The manuscript survives the hostile audit.
