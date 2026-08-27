# Master Manuscript Consistency Audit

This document traces critical manuscript claims against the actual final Python implementation (`code/`) and verified output reports, resolving all historical inconsistencies.

| Item | Source 1 (Old Claim) | Source 2 (Manuscript) | Actual Evidence (Code/Outputs) | Conflict? | Correct Value | Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A. Dataset Identities** | WESAD, Dataset B | WESAD, Dataset B | `data_loaders.py` loads `datasets/WESAD/` and `datasets/Dataset_B/`. | No | WESAD, Dataset B | Use these exact names. |
| **B. WESAD Participants** | N=15 | N=15 | `load_all_wesad` iterates over 15 `S*.pkl` files. | No | N=15 | Retain N=15. |
| **C. Dataset B Original Size** | N=34 | N=34 | `Stress_Level_v1.csv` / `v2.csv` implies ~34 total subjects. | No | N=34 | State original N=34. |
| **D. Dataset B Evaluated Size** | N=31 | N=31 | `hardening_bootstrap.py` line 90: `mask = ~df_b_filtered['subject_id'].isin(['S02', 'f07', 'f14'])`. | No | N=31 | State evaluated N=31. |
| **E-G. f07, f14, S02** | Excluded | Excluded | Excluded in all phase 3/11 hardening scripts. `f07` BVP/TEMP broken. | No | Excluded from primary. | Clearly list the 3 exclusions. |
| **H. Stress Labels** | TMCT, Opinion... | TMCT, Opinion, Subtract | `data_loaders.py` lines 12-14: WESAD (TSST). Dataset B: TMCT, Real Opinion, Opposite Opinion, Subtract. | No | Verified | Use verified task names. |
| **I. Baseline Labels** | Baseline | Baseline | `task == 'Baseline'` is mapped to label 0 in all scripts. | No | Verified | Use 'Baseline'. |
| **J. Sensor Modalities** | EDA, BVP, TEMP, ACC | EDA, BVP, TEMP, ACC | `config.py`: `MODALITIES = ['EDA', 'TEMP', 'BVP', 'ACC']`. (HR/IBI excluded). | No | EDA, BVP, TEMP, ACC | Ensure HR/IBI are never mentioned. |
| **K. Windowing** | 60s/30s | 60s/30s | `config.py`: `WINDOW_SIZE=60`, `STEP_SIZE=30`. | No | 60s window, 30s stride | Verified. |
| **L. Standard Scaler** | Fitted globally | Fitted on WESAD only | `exp3_runner.py`: `scaler.fit(X_train_raw)`. Frozen for inference. | Yes | Fitted exclusively on WESAD | Correct manuscript to strictly state WESAD-only scaling. |
| **M. Feature Selection** | K=30, K=20 | ANOVA, K=20 | `config.py`: `K_BEST=20`. Fit on WESAD only. | Yes | K=20, WESAD-only | Enforce K=20 ANOVA. |
| **N. SMOTE** | Applied everywhere | Applied to train fold | `pipeline.py`: `SMOTE` applied via `fit_resample` strictly on train data. | No | Train-fold only | State validation/target sets are untouched. |
| **O. Classifier** | LightGBM / LightGBM (XGBoost) | XGBoost | `multimodalai.py` had both. Hardening scripts exclusively import `XGBClassifier`. | Yes | XGBoost | **CRITICAL: Delete all references to LightGBM.** |
| **P. Baseline Normalization** | Baseline subtraction | Z-score (`(x-m)/s`) | `hardening_utils.py`: `new_seg['signals'][ch] = (np.array(data) - m) / s`. | Yes | Z-score referencing | Correct mathematical formula in manuscript. |
| **Q. Target Baseline Leakage** | "Pure zero shot" | "Zero target info" | `hardening_utils.py` computes `m` and `s` using Dataset B baseline task data. | Yes | Target baseline used | **CRITICAL: Remove "pure zero-shot". Replace with "label-free target baseline calibration".** |
| **R. Internal AUC (Exp 1)** | 0.964 | 0.964 | `experiment1_metrics.md` / `final_statistical_table.md` confirms 0.964. | No | 0.964 | Verified. |
| **S. External AUC (Exp 3)** | 0.423 | 0.423 | `final_statistical_table.md` confirms 0.423. | No | 0.423 | Verified. |
| **T. External AUC (Exp 5)** | 1.000 | 1.000 | `final_statistical_table.md` confirms 1.000. Computed on subject-aggregated predictions. | No | 1.000 | Qualify as subject-aggregated. |
| **U. Bootstrap CI** | [1.000, 1.000] | [1.000, 1.000] | `hardening_bootstrap.py`: Resamples subjects `replace=True`. | No | [1.000, 1.000] | State resampling was subject-level, not window-level. |
| **V. Permutation p-value** | p = 0.0000 | p = 0.0000 | `hardening_task_permutation.py` used 1000 permutations. 0 exceeded observed. | Yes | p < 0.001 | Change to scientifically accurate notation p < 0.001. |
| **W. ACC Cohen's d** | -1.47 | -1.47 | `experiment3_diagnostic_audit.md`: `ACC_Z_mean` has Cohen's d of -1.47443. | No | -1.47 | Verified. |
| **X. SHAP Spearman $\rho$** | 0.991 | 0.9527 | `final_shap_audit.md` reports 0.9527. | Yes | 0.9527 | **CRITICAL: Delete 0.991. Use 0.9527.** |
| **Y. SHAP Jaccard** | 1.000 | 1.000 | `final_shap_audit.md` reports Top-20 overlap 20/20. | No | 1.000 | Verified. |
| **Z. Logistic Regression** | Not mentioned | AUC=0.905 | `model_comparison.md`: External Dataset B (LR) ROC-AUC 0.905. | Yes | 0.905 | Add to robustness section. |
