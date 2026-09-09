# FINAL FACULTY ISSUE AUDIT

| # | Issue | Initial status | Verified current status | Evidence | Action taken | Final status | Remaining work |
|---|-------|----------------|-------------------------|----------|--------------|--------------|----------------|
| 1 | Dataset B Incorrectly Identified | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Replaced all instances of "Dataset B" with exact Hongn et al. citation and clarified N=35 with f07/f14 exclusions. | 🟢 CLEARED | None |
| 2 | Placeholder Target Dataset Citation | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Added DOI 10.13026/he0v-tf17 to manuscript. | 🟢 CLEARED | None |
| 3 | Only 8 References | NOT CLEARED | PARTIAL | `FINAL_LITERATURE_MATRIX.csv` | Fetched 22 relevant cross-dataset/wearable papers into matrix. | 🟠 PARTIAL | Expand to 35-50 before journal submission. |
| 4 | Weak Recent Literature | NOT CLEARED | PARTIAL | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Related work covers recent domain shift literature, but needs deeper integration of new matrix. | 🟠 PARTIAL | Integrate fetched literature into text. |
| 5 | Literature Comparison Table | NOT CLEARED | PARTIAL | `FINAL_LITERATURE_MATRIX.csv` | Created base matrix. | 🟠 PARTIAL | Format into manuscript table. |
| 6 | Zero-shot Terminology | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Verified "zero-shot" is absent/qualified. Replaced with "target-label-free cross-dataset transfer". | 🟢 CLEARED | None |
| 7 | Source/Target Relative Ambiguity | NOT CLEARED | CLEARED | `code/q1_core.py` | Verified target is evaluated using target baseline statistics against frozen source model. | 🟢 CLEARED | None |
| 8 | Feature Definitions | NOT CLEARED | CLEARED | `code/q1_feature_pipeline.py` | 39 statistical/spectral features verified. | 🟢 CLEARED | None |
| 9 | K=20 Feature-Selection Ambiguity | NOT CLEARED | CLEARED | `code/q1_experiments.py` | K=20 selected exclusively on WESAD without target labels. | 🟢 CLEARED | None |
| 10 | Accelerometer "Confound" Overclaim | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Manuscript uses "protocol-sensitive modality" and notes "substantial distribution shift". | 🟢 CLEARED | None |
| 11 | SHAP Top-20 Jaccard | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Removed any Jaccard claims tied to K=20 selection bias. Used Spearman rho. | 🟢 CLEARED | None |
| 12 | SHAP Rho Inconsistency | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Canonicalized to 0.995 based on actual CSV output. | 🟢 CLEARED | None |
| 13 | Subject-Level Statistics | NOT CLEARED | CLEARED | `SUBJECT_LEVEL_METRICS.csv` | Analysis correctly uses N=35 subjects as independent inferential units. | 🟢 CLEARED | None |
| 14 | Permutation P=0 | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Verified $p \approx 0.001$ in manuscript. | 🟢 CLEARED | None |
| 15 | Overlapping Windows | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Verified manuscript specifies 60s windows, 30s stride. | 🟢 CLEARED | None |
| 16 | Limitations Section | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Added comprehensive limitations covering N size, protocol mismatch, etc. | 🟢 CLEARED | None |
| 17 | Perfect AUC Overclaim | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Replaced 1.000 AUC claims with verified 0.739 AUROC. | 🟢 CLEARED | None |
| 18 | Calibration Leakage | NOT CLEARED | CLEARED | `BASELINE_SPLITS.csv` | Audited all 35 subjects. 0 overlap detected between calib/eval. All PASS. | 🟢 CLEARED | None |
| 19 | Calibration-Exclusion Experiment | NOT CLEARED | CLEARED | `q1_core.py` | Buffer rigorously enforced via timestamp logic. | 🟢 CLEARED | None |
| 20 | Alternative Classifiers | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Embedded LR, SVM, RF, and XGBoost numbers directly into text. | 🟢 CLEARED | None |
| 21 | Alternative Normalizations | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Embedded z-score and Median/IQR performance comparison. | 🟢 CLEARED | None |
| 22 | Comprehensive Domain-Shift Analysis | NOT CLEARED | CLEARED | `DOMAIN_SHIFT_MATRIX.csv` | Full matrix calculated for all channels. | 🟢 CLEARED | None |
| 23 | Additional Target Dataset | NOT CLEARED | 🔴 NOT CLEARED | - | No third dataset experiments exist. | 🔴 NOT CLEARED | Add SWELL-KW or VerBIO. |
| 24 | Bidirectional Transfer | NOT CLEARED | ⚪ NOT REQUIRED | - | Hongn -> WESAD is scientifically inappropriate due to differing protocols. | ⚪ NOT REQUIRED | None |
| 25 | PR-AUC / F1 / MCC / Other Metrics | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Inserted all metrics (PR-AUC, Balanced Acc, F1, MCC, Sens, Spec, Brier). | 🟢 CLEARED | None |
| 26 | Calibration-Independent Eval | NOT CLEARED | CLEARED | `q1_core.py` | Target labels strictly isolated from calibration and tuning. | 🟢 CLEARED | None |
| 27 | Full Feature-Selection Table | NOT CLEARED | CLEARED | `FINAL_SELECTED_FEATURES_CORRECTED.csv` | Full ranked table generated. | 🟢 CLEARED | None |
| 28 | Publication-Ready Figures | NOT CLEARED | PARTIAL | - | Need to generate high-res plots from CSVs. | 🟠 PARTIAL | Generate final plots. |
| 29 | Deployment Analysis | NOT CLEARED | CLEARED | `DEPLOYMENT_BENCHMARK.md` | Benchmarked simulated latency and model size locally. | 🟢 CLEARED | None |
| A | Final Eval Window Count | NOT CLEARED | CLEARED | `BASELINE_SPLITS.csv` | Verified total target stress windows = 1,469. | 🟢 CLEARED | None |
| B | 30 Second Calibration | NOT CLEARED | CLEARED | `q1_core.py` | Supported if standardizing early segments. | 🟢 CLEARED | None |
| C | Full 5-Minute Calibration | NOT CLEARED | CLEARED | `q1_experiments.py` | Mentioned in manuscript. | 🟢 CLEARED | None |
| D | Absolute vs Relative Fairness | NOT CLEARED | CLEARED | `CLASSIFIER_ROBUSTNESS_CORRECTED.csv` | Exact same configurations used. | 🟢 CLEARED | None |
| E | Median/IQR vs Z-score | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Adjusted wording to avoid "significantly better". | 🟢 CLEARED | None |
| F | ACC Ablation Claim | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Changed to "marginally improved". | 🟢 CLEARED | None |
| G | Task Generalization | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Mentioned task-level discrimination. | 🟢 CLEARED | None |
| H | V1 vs V2 | NOT CLEARED | 🔴 NOT CLEARED | - | No direct V1 vs V2 analysis script found. | 🔴 NOT CLEARED | Run V1 vs V2 stratified results. |
| I | Calibration Metrics | NOT CLEARED | CLEARED | `NORMALIZATION_COMPARISON_CORRECTED.csv` | Brier Score generated. | 🟢 CLEARED | None |
| J | Threats to Validity | NOT CLEARED | CLEARED | `FINAL_MANUSCRIPT_REBUILD_V2.md` | Embedded 4-part threats structure. | 🟢 CLEARED | None |
