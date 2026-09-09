# Final Manuscript Tables

## Table 1: Cohort Demographics and Data Utilization
| Dataset | N Total | Eligible N | Baseline Windows (Strict) | Stress Windows | Sampling Rate (EDA) | Stressor Protocols |
|---------|---------|------------|---------------------------|----------------|---------------------|--------------------|
| WESAD (Source) | 15 | 15 | 877 | 450 | 4 Hz | TSST |
| Hongn (Target) | 35 | 21 (for AUROC) | 57 | 1,469 | 4 Hz | Stroop, TMCT, Subtract |
| **Combined** | **50** | **36** | **934** | **1,919** | - | - |

## Table 2: Primary Cross-Dataset Transfer Performance (N=21 Eligible)
| Representation Model | Calibration Constraint | Macro Subject AUROC (95% CI) | Participant-Balanced Accuracy | Sensitivity | Specificity |
|----------------------|------------------------|------------------------------|-------------------------------|-------------|-------------|
| Absolute (Global) | None | 0.4922 (0.3357, 0.5056) | N/A | N/A | N/A |
| Baseline-Relative | 30s Calib + 30s Buffer | **0.7810** (0.6526, 0.8894) | 0.6697 | 0.6609 | 0.6786 |
| **Corrected Delta** | - | **+0.2888** (0.1754, 0.3955) | - | - | - |

## Table 3: Model Robustness Analysis (Relative Pipeline)
| Classifier | Absolute AUROC | Baseline-Relative AUROC | Improvement |
|------------|----------------|-------------------------|-------------|
| Logistic Regression | 0.418 | 0.660 | +0.242 |
| Support Vector Machine | 0.436 | 0.711 | +0.275 |
| Random Forest | 0.400 | 0.749 | +0.349 |
| XGBoost (Primary) | 0.408 | 0.781 | +0.373 |

## Table 4: Modality Ablation and Accelerometer Shift
| Modality Combination | Absolute AUROC | Relative AUROC | ACC Cohen's *d* Shift |
|----------------------|----------------|----------------|-----------------------|
| EDA + BVP + TEMP + ACC | 0.492 | 0.781 | -1.47 (High Shift) |
| EDA + BVP + TEMP (No ACC) | 0.510 | 0.765 | N/A |

## Table 5: Target Protocol Sequence Stratification
| Protocol | Sequence | N Total | Eligible N | Baseline Windows | Stress Windows | Macro Subject AUROC |
|----------|----------|---------|------------|------------------|----------------|---------------------|
| Protocol V1 | Stroop First | 18 | 18 | 53 | 461 | 0.7634 [0.6153, 0.8837] |
| Protocol V2 | Subtract First | 17 | 3 | 4 | 1,008 | 0.8864 [0.6761, 1.0000] |

## Table 6: Cross-Dataset Feature Attribution (SHAP)
| Agreement Metric | Comparison (WESAD vs. Target) | Frozen XGBoost Model |
|------------------|-------------------------------|----------------------|
| Spearman $\rho$ | Global Feature Ranks | 0.9847 |
| Kendall $\tau$ | Global Feature Ranks | 0.9333 |
| Jaccard Index | Top-10 Features | 1.0000 |
| Jaccard Index | Top-5 Features | 0.6667 |
