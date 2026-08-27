# Experiment 3: Cross-Dataset External Generalization

## 1. Methodology
- **Training Dataset:** WESAD
- **Test Dataset:** Dataset B
- **Constraints:** The complete pipeline (StandardScaler, SelectKBest, SMOTE, XGBoost) was mathematically frozen after fitting on WESAD. Dataset B was only used for pure inference. The fixed decision threshold of `0.5` was strictly maintained.

## 2. Leakage Audit
- Was Dataset B used for Scaler fitting? **NO**
- Was Dataset B used for Feature Selection? **NO**
- Was Dataset B used for Model Training? **NO**

## 3. Results (Main Cohort)
| Cohort                      |   Subjects |   Windows |   ROC-AUC |   PR-AUC |   Balanced Accuracy |       F1 |   Sensitivity |   Specificity |   TP |   FP |   TN |   FN |
|:----------------------------|-----------:|----------:|----------:|---------:|--------------------:|---------:|--------------:|--------------:|-----:|-----:|-----:|-----:|
| Main Cohort (Excluding S02) |         34 |       958 |  0.42301  | 0.445346 |            0.441176 | 0.136364 |     0.0882353 |      0.794118 |    3 |    7 |   27 |   31 |
| Main Cohort + S02           |         35 |       980 |  0.430204 | 0.447803 |            0.442857 | 0.133333 |     0.0857143 |      0.8      |    3 |    7 |   28 |   32 |

## 4. Subject Exclusions
- **f07:** Excluded due to invalid BVP/TEMP modalities.
- **f14:** Excluded due to severely fragmented windows (failed the 60s contiguous threshold).
- **S02:** A known signal quality issue was evaluated in the sensitivity analysis (see table above).

## 5. Task-Specific Exploration
See `outputs/external_task_specific_distribution.png` for a breakdown of how the frozen WESAD model responds to various Dataset B stressors (e.g. TMCT, Real Opinion, Subtract).