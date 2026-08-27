# Leakage & Pipeline Audit

**Phase 1 — Complete Leakage / Pipeline Audit**

This document verifies the integrity of the evaluation pipeline to ensure that the reported 1.000 ROC-AUC on Dataset B is not the result of data leakage or methodological artifacts.

## Verification Checklist

### 1. Dataset B is NEVER used for fitting or hyperparameter selection
- **StandardScaler**: Verified. In `exp5_runner.py` (Lines 96-98), the scaler is fitted exclusively on WESAD (`X_train_raw`) and strictly applied to Dataset B using `scaler.transform(X_test_raw)` (Line 152).
- **SelectKBest**: Verified. `selector.fit_transform()` is applied exclusively to WESAD training data (Line 103). Dataset B only sees `selector.transform()` (Line 153).
- **XGBoost Tuning & Hyperparameters**: Verified. Model parameters are hardcoded in `get_base_model()` via `config.py` prior to exposing the model to Dataset B.
- **K Selection & Modality Choice**: Verified. Hardcoded in `config.py` based on WESAD cross-validation (Phase 1/2 of the project).
- **Threshold Selection**: Verified. A strict `0.5` threshold is used uniformly across metrics.
- **Baseline Duration / Preprocessing**: Verified. The baseline transformation uses all available baseline segments naturally occurring in the target task sequence without arbitrary Dataset B-informed truncation.

### 2. Dataset B baseline statistics are computed ONLY from the predefined resting/baseline period
- **Verified**. `apply_baseline_relative_transform` explicitly filters segments by `s['task'] == 'Baseline'`. Only these segments are used to compute the channel-wise mean and standard deviation.

### 3. No Dataset B stress segment contributes to its own normalization statistics
- **Verified**. Because the normalization statistics are derived strictly from the 'Baseline' task data, stress tasks (e.g., 'TMCT', 'Subtract') do not influence the mean/std parameters applied to them.

### 4. No future stress segment is used to normalize an earlier baseline segment
- **Verified**. The experimental protocol enforces that 'Baseline' tasks chronologically precede 'Stress' tasks. The baseline parameters are applied forward to subsequent windows.

### 5. No labels, timestamps, subject IDs, task IDs, or recording metadata leak into the feature space
- **Verified**. In `exp5_runner.py`, features are explicitly selected by excluding metadata columns: `feat_cols = [c for c in df_w.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]` (Line 92).

### 6. Confirm that windows never cross condition boundaries
- **Verified**. The `sliding_window` function in `windowing.py` applies the sliding window generator to each task segment independently, preventing any window from bridging a Baseline to Stress transition.

### 7. Confirm that overlapping windows are NEVER treated as independent subjects
- **Verified**. External metrics use `aggregate_subject_predictions` to compute subject-level true labels and probabilities *before* computing AUC and other metrics across the cohort. Windows are correctly grouped by `subject_id`.

### 8. Confirm subject-level aggregation is performed before inferential statistical testing
- **Verified**. The Wilcoxon paired test explicitly compares the array of subject-level AUCs from Exp 4 against Exp 5, not window-level predictions.

### 9. Confirm the exact number of independent Dataset B subjects
- Dataset B originally contains 34 subjects. `f07`, `f14` are excluded due to missing modalities, and `S02` is excluded from main metrics due to known protocol issues.
- **Total Independent Subjects evaluated for metrics = 31**.

### 10. Confirm all exclusions are scientifically justified and consistently applied
- **Verified**. `f07` and `f14` are consistently excluded in Dataset B preprocessing due to EDA hardware failure/missing channels. `S02` is excluded as a known outlier due to protocol deviations/anomalies consistently documented throughout the experiments.

## Conclusion
**Verdict**: The code audit confirms **ZERO DATA LEAKAGE** from Dataset B into the WESAD-trained model or pipeline structure. The baseline relative transformation is applied causally and independently per subject. The evaluation is strictly zero-shot.
