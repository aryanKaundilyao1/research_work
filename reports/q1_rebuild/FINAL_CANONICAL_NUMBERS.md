# Final Canonical Numbers

| Metric | Exact Value | Representation | Classifier | Modalities |
| :--- | :--- | :--- | :--- | :--- |
| **Absolute AUROC** | 0.408 | Absolute (StandardScaler) | XGBoost | EDA+BVP+TEMP+ACC |
| **Baseline-Relative AUROC** | 0.739 | Z-Score (60s Calibration) | XGBoost | EDA+BVP+TEMP+ACC |
| **Median/IQR AUROC** | 0.751 | Median/IQR (60s Calibration) | XGBoost | EDA+BVP+TEMP+ACC |
| **Cohen's d (ACC Shift)** | ≈ -1.47 | Absolute | N/A | ACC-Z |
| **SHAP Spearman $\rho$** | 0.9527 | Z-Score | XGBoost | EDA+BVP+TEMP+ACC |
| **Permutation p-value** | $p \approx 0.001$ | Z-Score | XGBoost | EDA+BVP+TEMP+ACC |

**Target Cohort Details**:
- N subjects = 35 independent participants
- Calibration duration = 60s
- Evaluation unit = Subject-level aggregation

**Classifier Robustness (Absolute $\rightarrow$ Relative AUROC)**:
- Logistic Regression: 0.418 $\rightarrow$ 0.660
- SVM: 0.436 $\rightarrow$ 0.711
- Random Forest: 0.400 $\rightarrow$ 0.749
- XGBoost: 0.408 $\rightarrow$ 0.739

*Note: All four evaluated classifiers demonstrated substantial improvement under the baseline-relative representation.*
