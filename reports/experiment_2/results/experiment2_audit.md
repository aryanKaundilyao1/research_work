# Experiment 2 Methodology Audit

## 1. Experimental Constancy
- **WESAD Subjects:** **[PASS]** Code verified; identical 15 subjects utilized.
- **Windows / Step:** **[PASS]** 60s/30s used via centralized `config.py`.
- **LOSO Folds:** **[PASS]** 15 folds exactly matched.
- **Nested Preprocessing (Scaler, KBest, SMOTE):** **[PASS]** Identical fold-level fitting constraints applied via `run_ablation_condition`.
- **XGBoost Parameters & Random Seeds:** **[PASS]** Centralized `get_base_model()` ensured exactly identical configuration (`RANDOM_SEED=42`).
- **Subject-level Aggregation:** **[PASS]** `aggregate_subject_predictions` was used identically for all modalities.

## 2. Per-Subject Result Table
The deterministic extraction of subject-level ROC-AUCs has been saved to `reports/experiment2_subject_results.csv`.

**OBSERVED RESULT (CRITICAL CORRECTION):**
The subject-level ROC-AUC (which evaluates whether a specific individual's predicted stress probability is strictly greater than their predicted baseline probability) is **exactly 1.000 for EVERY subject across ALL 5 modality conditions.** 

## 3. Calculated Paired Performance Differences
Using the Wilcoxon signed-rank test on the subject-level ROC-AUCs across the 15 subjects:
- **Full vs BVP:** Mean Diff = +0.000 | p-value = 1.0000
- **Full vs EDA:** Mean Diff = +0.000 | p-value = 1.0000
- **Full vs EDA+BVP:** Mean Diff = +0.000 | p-value = 1.0000
- **Full vs EDA+BVP+TEMP:** Mean Diff = +0.000 | p-value = 1.0000

## 4. Investigation of Balanced Accuracy Variance
Since the internal ranking metric (Subject ROC-AUC) is a perfect 1.0 for all subjects across all conditions, the previous assumption that certain subjects "failed classification under EDA but succeeded under BVP" is **mathematically false**.

**Interpretation of the Variance:**
The variations in global ROC-AUC (0.907 to 0.964) and Balanced Accuracy (0.833 to 0.933) are entirely artifacts of **global thresholding calibration, not internal discriminative failure.**
Because Balanced Accuracy applies a hard threshold of `0.5` across all subjects globally:
- If a subject's EDA-based baseline probability is `0.6` and stress is `0.9` (AUC = 1.0), the hard `0.5` threshold misclassifies the baseline as Stress.
- The addition of modalities (like BVP and TEMP) does not improve internal ranking (it is already perfect), but it **calibrates the absolute probabilities** closer to the 0.5 global threshold across diverse individuals. 
Therefore, the improvement in Balanced Accuracy (0.867 to 0.933) is driven by shifting the absolute probabilities of outlier subjects across the 0.5 threshold, rather than fixing a failure to rank stress higher than baseline.

## 5. Statistical Significance Claims
No statistical significance can be claimed for the performance differences between the modalities. The appropriate paired non-parametric test (Wilcoxon signed-rank) yields a p-value of 1.0000 for all comparisons because the within-subject discrimination is identical (perfect) for all subsets.

## 6. Audit Conclusion
**Methodological Integrity:** The code execution was structurally flawless and perfectly aligned with the Experiment 1 constraints. 
**Interpretive Correction:** The previous interpretation hallucinated subject-specific failures that did not exist. The model perfectly discriminates stress from baseline within *every* individual using *any* modality subset; the only challenge remaining is calibrating the global threshold across individuals.

We are ready to proceed to Experiment 3, noting that cross-dataset external validation (which relies on absolute probability calibration transferred from WESAD) may suffer if the target dataset has a different baseline threshold.
