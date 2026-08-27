# Final Figure Audit

This document ensures that every requested figure in the final manuscript is scientifically justified and accurately reflects the underlying data.

## Figure 1: Study Workflow
- **Scientific Purpose:** Visually proves that the pipeline strictly separates internal validation (LOSO) from external generalization (Dataset B Zero-Shot). It must show the isolation of the Scaler, SelectKBest, and SMOTE blocks.
- **Claim Supported:** The evaluation prevents data leakage.

## Figure 2: Internal vs External Collapse (Bar Chart)
- **Scientific Purpose:** Visualizes the catastrophic drop from 0.964 to 0.423. 
- **Claim Supported:** Internal LOSO performance vastly overestimates true out-of-distribution generalizability (Tier 1).

## Figure 3: ACC Domain-Shift Diagnostic (Boxplot/Distribution)
- **Scientific Purpose:** Visualizes the `Cohen's d = -1.47` shift in `ACC_Z_mean`.
- **Claim Supported:** Accelerometer captures physical protocol differences, not physiological stress, causing external failure (Tier 2).

## Figure 4: Ablation and Baseline-Relative Recovery (ROC Curve)
- **Scientific Purpose:** Shows the sequential recovery: Exp 3 (0.423) $\rightarrow$ Exp 4 (0.540) $\rightarrow$ Exp 5 (1.000).
- **Claim Supported:** Removing ACC is necessary but insufficient; subject-specific baseline referencing provides the crucial recovery (Tier 1).
- **Data Source:** `reports/final_hardening/relative_modality_ablation.png` (or equivalent ROC generation).

## Figure 5: Subject-Level Probability Margins (Strip plot / Box plot)
- **Scientific Purpose:** Proves that the 1.000 ROC-AUC is real at the subject level and not driven by a few massive outliers or window-level statistical inflation.
- **Claim Supported:** The median predicted stress probability is strictly higher than the median predicted baseline probability for all 31 subjects (Tier 1).
- **Data Source:** `reports/final_hardening/subject_margin_plot.png` or `task_response_plot.png`.

## Figure 6: Cross-Dataset SHAP Attribution (Scatter Plot)
- **Scientific Purpose:** Visualizes the $\rho = 0.9527$ correlation between the WESAD SHAP vector and the Dataset B SHAP vector.
- **Claim Supported:** The model uses the same representational logic across both cohorts, rather than finding spurious new correlations (Tier 1).
