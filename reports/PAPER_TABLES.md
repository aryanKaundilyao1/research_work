# Manuscript Tables

**TABLE I: Dataset and Participant Characteristics**
| Characteristic | Source Domain (WESAD) | Target Domain (Dataset B) |
| :--- | :--- | :--- |
| **Participants** | $N=15$ | $N=31$ (Valid subset) |
| **Stress Induction** | Trier Social Stress Test (TSST) | TMCT, Opinion, Subtract |
| **Control Tasks** | Amusement | None (Baseline only) |
| **Physiological Modalities** | EDA, BVP, TEMP | EDA, BVP, TEMP |
| **Motion Modalities** | ACC (X, Y, Z) | ACC (X, Y, Z) |

**TABLE II: Experimental Pipeline Definitions**
| Component | Implementation Details / Leakage Control |
| :--- | :--- |
| **Windowing** | 60s window, 30s stride. Strict subject and condition boundaries. |
| **Feature Space** | 39 features/channel (time, frequency, non-linear). |
| **Scaling** | Fit on WESAD training data *only*; applied to validation/target. |
| **Feature Selection** | ANOVA F-value (SelectKBest) fit on WESAD training data *only*. |
| **Class Balancing** | SMOTE applied to WESAD training data *only*. |
| **Classifier** | XGBoost (hyperparameters tuned on WESAD *only*). |
| **Subject Aggregation**| Predictions aggregated to subject level for inferential statistics. |
| **Zero-Shot Eval** | Dataset B target labels strictly isolated from training/tuning. |

**TABLE III: Internal and External Performance Comparison**
| Experiment | Representation | Modalities | Evaluation | ROC-AUC | Balanced Accuracy | F1 Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Exp 1** | Absolute | EDA, BVP, TEMP, ACC | Internal (WESAD LOSO) | 0.964 | 0.933 | 0.933 |
| **Exp 3** | Absolute | EDA, BVP, TEMP, ACC | External (Dataset B Zero-Shot) | 0.423 | 0.441 | NR |

**TABLE IV: Domain-Shift and Ablation Analysis (External Dataset B Evaluation)**
| Experiment | Representation | ACC Included | ROC-AUC | Balanced Acc. | Sensitivity | Specificity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Exp 3** | Absolute | Yes | 0.423 | 0.441 | NR | NR |
| **Exp 4** | Absolute | No | 0.539 | 0.514 | NR | NR |
| **Exp 5** | Relative (Baseline) | No | 1.000 | 0.970 | 0.941 | 1.000 |

**TABLE V: Cross-Dataset SHAP Attribution Agreement**
| Metric | Result | Interpretation |
| :--- | :--- | :--- |
| **Spearman Rank Correlation ($\rho$)** | 0.9527 | Highly conserved feature priority across datasets. |
| **Top-20 Jaccard Overlap** | 1.000 | Perfect overlap in the 20 most important features. |
| **Modality Proportion (WESAD)** | EDA: 55.8%, TEMP: 38.3%, BVP: 5.9% | Internal reliance on EDA and TEMP. |
| **Modality Proportion (Dataset B)**| TEMP: 54.0%, EDA: 39.3%, BVP: 6.7% | Target relies on the same core physiological modalities. |

**TABLE VI: Robustness and Hardening Analyses (Dataset B, Relative Representation)**
| Analysis | Methodology | Metric / Result | Conclusion |
| :--- | :--- | :--- | :--- |
| **Subject-Level Bootstrapping** | 5,000 resamples at the subject level. | 95% CI: [1.000, 1.000] | Probability margin is strictly positive for all valid subjects. |
| **Permutation Control** | Subject-level label shuffle. | Empirical $p = 0.0000$ | Results are not a structural artifact of the evaluation pipeline. |
| **Baseline Duration Sensitivity** | Reduced relative reference window. | Stable transfer at 30s. | Substantial clinical baselines are not required for transfer. |
| **Modality Ablation (Relative)** | Isolation of EDA vs. BVP vs. TEMP. | Both TEMP and EDA retain high independent AUCs. | Physiological features are independently predictive. |

*(Note: "NR" = Not Reported in final auditing for this specific intermediate phase).*
