# Manuscript Figures and Tables Plan

## Core Figures to Include
1. **Conceptual Architecture Diagram:** (Needs to be generated for manuscript). A flowchart visually separating the "Absolute Model Pipeline" from the "Baseline-Relative Normalization Pipeline."
2. **Figure 1 (Performance Bar Chart):** Consolidating the external domain shift. A single bar chart showing ROC-AUC for internal WESAD (Exp 1), absolute Dataset B with ACC (Exp 3), absolute Dataset B without ACC (Exp 4), and relative Dataset B (Exp 5).
3. **Figure 2 (Modality Contribution):** Use the existing `reports/experiment_6/outputs/modality_shap_comparison.png` to prove that both datasets leaned identically on EDA and TEMP.
4. **Figure 3 (Feature Agreement):** Use the existing `reports/experiment_6/outputs/feature_level_agreement.png` (Spearman rank scatterplot) showing the 1-to-1 diagonal matching between datasets.
5. **Figure 4 (SHAP Attributions):** Side-by-side beeswarm plots using `reports/experiment_6/outputs/shap_beeswarm_wesad.png` and `reports/experiment_6/outputs/shap_beeswarm_datasetB.png` to illustrate the directional consistency of `TEMP_rms` and `EDA_q1`.
6. **Figure 5 (Task Phase Validation):** Use the existing `reports/experiment_5/outputs/experiment5_task_probabilities.png` to prove that predicted probabilities logically scale across Baseline, Subtraction, and TSST-variants (TMCT).

## Existing Figures to Exclude
- `ablation_subject_comparison.png` (Too detailed for main body).
- `confusion_matrix.png` (ROC-AUC conveys the point better).
- `baseline_relative_signal_comparison.png` (Useful for Supplementary Materials to prove the math, but not the main text).

## Tables
1. **Table 1: Cohort Demographics and Protocols:** (To be constructed from Dataset summaries). Outlining N=15 WESAD and N=34 Dataset B subjects.
2. **Table 2: Pipeline Comparison Results:** Use `reports/final_results_table.csv` to build a clean 4-row table of Exp 1, 3, 4, and 5 performance.
3. **Table 3: Interpretability Feature Rankings:** Use `reports/experiment_6/results/shap_feature_ranking.csv` to list the Top 10 universally conserved features, their mean absolute SHAP, and their biological direction.
