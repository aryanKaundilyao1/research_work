# Final Table Audit

Before the manuscript is generated, the tables must reflect ONLY the audited, mathematically verified numbers from the codebase.

## TABLE I: Dataset and Participant Characteristics
- **Rule:** Do NOT write N=31 for Dataset B without qualification. 
- **Required:** WESAD N=15. Dataset B Original N=34. Excluded N=3 (S02, f07, f14). Evaluated N=31.

## TABLE II: Signal Processing and Pipeline Rules
- **Rule:** Explicitly state the leakage controls verified in code.
- **Required:**
    - Standard Scaler: Fit on WESAD only.
    - Feature Selection: ANOVA F-value (K=20), fit on WESAD only.
    - SMOTE: Applied exclusively to the training fold (k=5).
    - Classifier: XGBoost.

## TABLE III: Internal WESAD Performance
- **Rule:** This establishes the internal benchmark (Exp 1).
- **Required:** 
    - ROC-AUC: 0.964
    - Must specify this is LOSO-CV.

## TABLE IV: External Zero-Shot Transfer and Ablation
- **Rule:** This table tells the collapse and recovery story. It must map exactly to Exp 3, Exp 4, and Exp 5.
- **Required:**
    - Absolute + ACC (Exp 3): ROC-AUC 0.423
    - Absolute - ACC (Exp 4): ROC-AUC 0.540 (Rounded from 0.539/0.54 in reports)
    - Relative - ACC (Exp 5): ROC-AUC 1.000, Balanced Acc 0.971 (Based on actual hardening report rounding).
    - Note: Because F1/Sens/Spec were not systematically re-exported for Exp 3/4 in the final script, leave those as N/A or compute them in text. Do not invent them.

## TABLE V: Cross-Dataset Attribution Agreement
- **Rule:** Use the audited SHAP script outputs.
- **Required:**
    - Spearman $\rho$: 0.9527
    - Top-20 Jaccard: 1.000
    - Modality Proportions (WESAD): EDA 55.8%, TEMP 38.3%, BVP 5.9%
    - Modality Proportions (Dataset B): TEMP 54.0%, EDA 39.3%, BVP 6.7%

## TABLE VI: Robustness Analyses
- **Rule:** Include the bootstrap, permutation, baseline duration, and logistic regression results.
- **Required:**
    - Bootstrap: CI [1.000, 1.000]
    - Permutation: Empirical p < 0.001 (0/1000)
    - Logistic Regression: External AUC 0.905
