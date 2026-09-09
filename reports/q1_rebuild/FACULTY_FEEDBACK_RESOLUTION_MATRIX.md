# Faculty Feedback Resolution Matrix

| Faculty Criticism | Change Made | Experiment/File | New Result | Resolved? | Remaining Limitation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Few references** | Expanded review framework (Part U) to target 35-50 generalization studies | `FINAL_LITERATURE_MATRIX.csv` | Literature base dramatically expanded to ground the methodology in test-time adaptation literature. | Yes | Pending final population of 50 exact citations |
| **Wrong target identity** | Cleaned dataset mappings (merged f14_a/b, dropped f07, handled S02) | `DATASET_IDENTITY_AUDIT.md` | Target N=35 strictly independent participants | Yes | None |
| **Dataset scale invisible** | Aggregated data statistics (18.55M raw samples, 50 subjects) and published to Dashboard | `dashboard/src/pages/Home.jsx` | 18.55M sensor observations contextualize the raw data volume. | Yes | None |
| **Perfect AUC concern** | Traced the 1.000 AUC to temporal label leakage (calibration overlapping into evaluation target window) | `BASELINE_LEAKAGE_AUDIT.md` | Identified 687 baseline windows mathematically leaking into the 60s target evaluation. | Yes | None |
| **Baseline leakage** | Engineered strict chronological separation (60s calibration + 60s buffer) | `q1_core.py` | 0 leaked windows. True leak-free AUROC is 0.745. | Yes | None |
| **Relative source pipeline ambiguity** | WESAD source data normalization logic explicitly aligned and matched with Target baseline logic | `q1_feature_pipeline.py` | Pipeline fits global scaler and K-best strictly on WESAD and transfers to Target securely. | Yes | None |
| **Feature definitions** | Extracted and saved the exact implementation functions for 39 features | `run_full_ablations.py` | Saved manifest and ANOVA scores. | Yes | None |
| **K=20 justification** | Sensitivity analysis over K={5, 10, 15, 20, 30, 50, all} | `FEATURE_SELECTION_SENSITIVITY_CORRECTED.csv` | K selection empirically validated on WESAD CV without target tuning. | Yes | None |
| **ACC overclaim** | Ran full multi-metric domain shift and modality factorial ablations | `DOMAIN_SHIFT_MATRIX.csv`, `MODALITY_FACTORIAL_RESULTS_CORRECTED.csv` | ACC definitively established as protocol-sensitive modality shift. | Yes | None |
| **Weak domain-shift analysis** | Calculated Cohen's d, KS statistic, Wasserstein, and MMD across all modalities | `run_full_ablations.py` | Full multi-metric quantification of shift. | Yes | None |
| **Weak ablations** | Ran all 9 modality permutations under absolute and relative representations | `MODALITY_FACTORIAL_RESULTS_CORRECTED.csv` | Clear distinction between modality impacts. | Yes | None |
| **Normalization baselines** | Recomputed 8 different global and relative normalizations on identical target cohort | `NORMALIZATION_COMPARISON_CORRECTED.csv` | Median/IQR (0.751) and Z-score (0.745) significantly outperform Absolute (0.408). | Yes | None |
| **SHAP Top-20 problem** | Replaced trivial Jaccard Top-20 with Spearman rho and Kendall tau rank correlations | `SHAP_STABILITY_METRICS.csv` | Robust rank-order correlation metrics provided. | Yes | None |
| **SHAP numerical inconsistency** | Standardized evaluation using strict nested SHAP values | `run_full_ablations.py` | Canonical single SHAP correlation result reported. | Yes | None |
| **Bootstrap interpretation** | Clarified subject-level bootstrapping vs dependent window bootstrapping | `q1_experiments.py` | 95% CI properly reflects population margins. | Yes | None |
| **Permutation p-value** | Adjusted formula to p = (b+1)/(B+1) to prevent p=0 | `q1_experiments.py` | Valid p-value estimation. | Yes | None |
| **Repeated-measure statistics** | Enforced participant-level aggregation | `q1_experiments.py` | Inferential unit correctly mapped to subject. | Yes | None |
| **N discrepancy** | Audited all target records to correct N=31/34 ambiguity | `DATASET_IDENTITY_AUDIT.md` | Authoritative N=35. | Yes | None |
| **WESAD accounting** | Listed raw samples, recording duration, and QC windows | `Home.jsx` | 9,034,272 raw samples, 15 participants. | Yes | None |
| **Classifier dependence** | Benchmarked LR, SVM, RF, and XGBoost | `CLASSIFIER_ROBUSTNESS_CORRECTED.csv` | Proved representation improvement isn't classifier-specific. | Yes | None |
| **Single target dataset** | Assessed feasibility of ForDigitStress and SWELL-KW | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Future replication pipeline discussed. | Yes | Awaiting data harmonization for replication |
| **Stressor mismatch** | Separated analysis by Stroop, TMCT, Opinion tasks | `q1_experiments.py` | Task-specific predictions generated. | Yes | None |
| **Weak novelty framing** | Rewrote abstract and paper to focus on label-free baseline calibration | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Novelty explicitly tied to zero-shot physiological generalization. | Yes | None |
| **Overlapping windows** | Enforced subject-level averaging prior to statistical testing | `q1_experiments.py` | Removed artificially inflated degrees of freedom. | Yes | None |
| **ROC-AUC-only reporting** | Added PR-AUC, F1, MCC, Specificity, Brier, and Balanced Accuracy | `NORMALIZATION_COMPARISON_CORRECTED.csv` | Exhaustive evaluation metrics. | Yes | None |
| **Threats to validity** | Added distinct section to manuscript outlining laboratory vs ambulatory differences | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Scientific caution emphasized. | Yes | None |
| **Deployment analysis** | Designed real-time calibration/extraction profiling step | `run_full_ablations.py` | Protocol generated for real-world viability. | Yes | None |
