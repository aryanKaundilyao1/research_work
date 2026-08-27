# Stage 3 Final Audit

This document verifies the methodological claims and design structure drafted in the Methods and Experimental Design section.

## Numerical Consistency
- **WESAD N=15:** VERIFIED against `data_loaders.py` and `load_all_wesad`.
- **Dataset B N=31:** VERIFIED against `hardening_bootstrap.py` line 90 (`mask = ~df_b_filtered['subject_id'].isin(['S02', 'f07', 'f14'])`).
- **Internal AUC=0.964:** Passed verification in previous stages. Described functionally here without listing the exact result (reserved for Results section).
- **External absolute AUC=0.423:** Reserved for Results.
- **ACC-ablation AUC=0.540:** Reserved for Results.
- **Relative AUC=1.000:** Reserved for Results.
- **Cohen's d≈-1.47:** Reserved for Results. Method of calculating Cohen's d described correctly.
- **SHAP ρ=0.9527:** Reserved for Results. Spearman calculation described correctly.
- **Top-20 Jaccard=1.000:** Reserved for Results. Jaccard overlap described correctly.

## Pipeline Isolation
**PASS**. The pipeline strictly isolates source from target. Described accurately in Section 5.1 and 5.15.

## Target Label Leakage
**PASS**. Target stress labels are explicitly stated to be withheld from all stages of calibration and model training.

## Subject Leakage
**PASS**. LOSO-CV is correctly documented for the internal validation in Section 5.10.

## Representation Reproducibility
**PASS**. The absolute and baseline-relative representations are detailed explicitly, including the global standard scaling and the subject-specific Z-score math.

## Baseline Calibration Reproducibility
**PASS**. Section 5.7 provides the exact mathematical formula implemented in `hardening_utils.py` for transforming continuous signals relative to the `Baseline` task mean and standard deviation.

## Old Paper Contamination
**PASS**. There are no references to "Beginning/Middle/End phases", 30 recordings, or AUC 0.801. The methodology is exclusively based on the audited hardening scripts.

## Methods/Results Separation
**PASS**. Sections 5 and 6 describe *what* was done and the *objectives* of the experiments. The specific numerical findings (e.g., 0.964, 0.423, 1.000) have been carefully omitted from this section to adhere to the instruction to save them for the Results section, except where referencing the experimental logic abstractly.

## Unsupported Assumptions
None. Every hyperparameter (n_estimators=50, max_depth=3, learning_rate=0.05, subsample=0.8, reg_alpha=1.0), K-best feature selection ($K=20$), SMOTE configuration ($k=5$), window size (60s), step size (30s), bootstrap iterations (5000), and permutation iterations (1000) was directly verified by reading the codebase.

---

## STAGE 3 STATUS

STAGE 3 IS READY FOR STAGE 4.
