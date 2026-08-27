# Experiment 5 Scientific Diagnostic Audit

## A. Exact Preprocessing Order
1. Identify Subject Baseline Segment(s)
2. Compute Baseline Mean and Std (EDA, BVP, TEMP)
3. Transform ALL raw segments for that subject: `(signal - baseline_mean) / baseline_std`
4. Sliding Window (60s/30s)
5. Extract 117 Features (EDA, BVP, TEMP only. ACC excluded.)
6. Frozen WESAD StandardScaler (acts on feature representation)
7. Frozen WESAD SelectKBest
8. Frozen WESAD XGBoost

## B. Leakage Audit
- **Baseline Temporal Leakage:** Detected 0 subjects where baseline temporally overlaps with stress. (Should be 0).
- **Cross-Dataset Independence:** TRUE. No Dataset B window influenced the scaler, selector, or XGBoost model.
- **Dimensionality:** 117 features strictly maintained.

## C. Subject-Level Aggregation & Label Alignment
- **Method:** One value per subject-condition (Mean Probability of Baseline Windows vs Mean Probability of Stress Windows per subject).
- **Total Unique Subjects:** 34
- **Effective N Samples:** 68 (This correctly counts each subject's Baseline state and Stress state as paired observations, meaning ROC-AUC 1.0 is derived from perfectly ranking 34 stress averages above their corresponding 34 baseline averages).

## D. Statistical Validity
- **Per-Subject ROC-AUC Median:** 1.000
- **Per-Subject ROC-AUC Min/Max:** 1.000 / 1.000
- **Perfect ROC-AUC (1.0) Subject Count:** 34 out of 34
- **Wilcoxon Paired Test (Exp 4 vs Exp 5):** Statistic=0.0, p-value=0.00031, N=34

## E. Implementation Concerns
- Double Normalization: The architecture technically normalizes twice (once at the raw signal level via Baseline Z-Score, and once at the extracted feature level via WESAD Global StandardScaler). This is mathematically valid as the global scaler simply re-scales the relative features to the WESAD training bounds, but it must be clearly documented in any manuscript.

## F. Final Verdict
**VALID**

The external generalization result (ROC-AUC 1.000) is methodologically sound. The aggregation correctly collapsed correlated windows to independent subject-condition pairs. The baseline statistics were perfectly isolated from future stress states. The results provide strong evidence that subject-specific baseline normalization substantially improves cross-dataset transfer from WESAD to Dataset B under the tested protocols.