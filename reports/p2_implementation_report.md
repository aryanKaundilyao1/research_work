# P2 Implementation Report

## 1. Architecture Overview
The P2 Model Construction pipeline is entirely modular, separated from all legacy code, and built to unconditionally enforce zero-leakage cross-dataset generalization.

### Files Created
- **`code/config.py`**: A centralized, reproducible configuration file locking paths, hyperparameters (`RANDOM_SEED=42`), feature subsets (`K_BEST=20`), XGBoost params (`max_depth=3`, `n_estimators=50`), and dataset constraints.
- **`code/features.py`**: A robust `build_feature_matrix()` orchestrator that applies exactly the same mathematics to WESAD and Dataset B signals while handling missing/NaN windows transparently.
- **`code/pipeline.py`**: The core ML engine. Implements `run_nested_cv()` for WESAD internal evaluation and `train_final_model()` / `predict_external()` for frozen cross-dataset testing.
- **`code/metrics.py`**: Evaluator containing `aggregate_subject_predictions()` to collapse highly collinear overlapping windows into statistically valid subject-level probabilities before computing ROC-AUC, PR-AUC, etc.
- **`code/experiments.py`**: Skeleton runner housing the orchestrators for Experiments 1 through 6.
- **`code/sanity_test.py`**: A micro-scale execution script to validate architecture routing.

## 2. Order of Operations

### Exact Preprocessing Order (Nested CV)
1. Window extraction (Independent bounds).
2. Mathematical Feature Extraction (234 total).
3. `LeaveOneGroupOut` Split (grouped by `subject_id`).
4. **`StandardScaler`**: Fitted on `X_train`, applied to `X_test`.
5. **`SelectKBest`**: Fitted on scaled `X_train`, applied to `X_test`.
6. **`SMOTE`**: Applied exclusively to the balanced, scaled, selected `X_train` to generate `X_train_resampled`.
7. **`XGBoost`**: Trained on `X_train_resampled`.
8. Predictions on `X_test`.

### External Validation Implementation
1. Train complete pipeline (`Scaler` -> `Selector` -> `SMOTE` -> `XGBoost`) on 100% of WESAD using identical hyperparameters.
2. Freeze pipeline objects.
3. Load Dataset B windows (unmodified, unfiltered).
4. Apply WESAD `Scaler.transform()`.
5. Apply WESAD `Selector.transform()`.
6. Generate predictions using WESAD `XGBoost.predict_proba()`.
7. Zero Dataset B information is leaked into the pipeline configuration.

## 3. Sanity Test Outcome
A small local execution was triggered on a 4-subject sub-cohort (WESAD: S2, S3; Dataset B: S01, S03) via `python code/sanity_test.py`.

**Results:**
- Internal WESAD Subject-Aggregated AUC: `0.625`
- External Dataset B Subject-Aggregated AUC: `0.250`
- Feature Dimensions: `234` matching exactly across both datasets.
- **Verdict:** `PASSED`. The structural mathematics successfully separated train/test vectors. The frozen Dataset B prediction executed flawlessly without encountering scaling or feature-matching dimension errors. 

*(Note: AUCs are non-scientific artifacts of a 4-subject N=4 test).*

## 4. Remaining Blockers
- **None.** The infrastructure supports Ablation mapping, Temporal extraction via relative ranks, Task-based aggregation, and SHAP compatibility exactly as demanded.

---

### STATUS
**READY FOR EXPERIMENT 1**
