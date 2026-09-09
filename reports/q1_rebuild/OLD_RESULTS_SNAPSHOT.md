# PHASE 0 — OLD RESULTS SNAPSHOT

## Recorded Results
- **Internal WESAD:** ROC-AUC = 0.964
- **Absolute external:** ROC-AUC = 0.423
- **ACC ablated:** ROC-AUC = 0.540
- **Current baseline-relative:** ROC-AUC = 1.000
- **SHAP rho:** 0.9527
- **Old Top-20 Jaccard:** 1.000

## Experimental Parameters
- **Code file:** `code/experiments.py` (and related runner scripts)
- **Dataset version:** 1.0.1 (Wearable device dataset from induced stress and structured exercise sessions)
- **Exclusions:** `f07` (due to missing valid BVP and TEMP sensors caused by wristband protection dock)
- **Feature set:** K=20 features selected from EDA, TEMP, BVP, ACC using ANOVA F-value
- **Classifier:** XGBoost (Random Seed: 42, max_depth: 3, n_estimators: 50, reg_alpha: 1.0, learning_rate: 0.05, subsample: 0.8)
- **Preprocessing:** StandardScaler, SMOTE
- **Seed:** 42
- **Window count:** 60s windows with 30s stride
- **Subject count:**
  - WESAD: 15 subjects
  - Target Dataset (formerly Dataset B): 35 subjects (36 total minus 1 excluded)
