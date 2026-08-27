# Figure and Table Mapping Plan

## Figures

- **Figure 1: Overall Study Design and Experimental Framework.** 
  - *Description:* Flowchart demonstrating the training on WESAD, the absolute representation failure on Dataset B, the ACC diagnosis, and the baseline-relative recovery.
  - *Source:* To be generated as a block diagram.
- **Figure 2: Cross-Dataset Generalization Collapse and Recovery.** 
  - *Description:* Bar chart contrasting internal WESAD performance (AUC=0.964) with Absolute+ACC transfer (AUC=0.423) and Relative-ACC transfer (AUC=1.000).
  - *Source:* Built from `final_statistical_table.md`.
- **Figure 3: Modality-Specific Domain Shift (ACC Diagnostic).** 
  - *Description:* Boxplots showing the catastrophic dataset shift in Accelerometer features (e.g., ACC Z mean) compared to physiological features. 
  - *Source:* Based on data from Phase 6 (`normalization_acc_factorial.csv`).
- **Figure 4: Ablation and Normalization Performance Comparison.** 
  - *Description:* ROC curves showing the impact of removing ACC and shifting to relative normalization.
  - *Source:* `relative_modality_ablation.png`.
- **Figure 5: Subject-Level Stress vs. Baseline Probability Distributions.** 
  - *Description:* Scatter/Violin plot showing strict probability margin separation (Predicted Stress > Predicted Baseline) for all 31 valid subjects in Dataset B under the relative representation.
  - *Source:* `subject_margin_plot.png`.
- **Figure 6: SHAP Feature Attribution Agreement.** 
  - *Description:* Scatter plot comparing internal WESAD SHAP values versus external Dataset B SHAP values, demonstrating the high Spearman correlation ($\rho=0.9527$).
  - *Source:* Data from `final_shap_audit.md`.

## Tables

- **Table 1: Dataset Characteristics and Signal Modalities.**
  - *Description:* Demographic and protocol comparison of WESAD (source) and Dataset B (target).
- **Table 2: Experimental Pipeline and Leakage-Control Strategy.**
  - *Description:* Checkmarks detailing how information leakage was prevented at each modeling stage.
- **Table 3: Internal and External Performance Comparison.**
  - *Description:* Core AUC, Balanced Accuracy, and F1 comparisons for internal vs. external baselines.
- **Table 4: Ablation and Normalization Comparison.**
  - *Description:* The 4 conditions (Absolute+ACC, Absolute-ACC, Relative+ACC, Relative-ACC) summarizing the interaction of ACC and referencing.
- **Table 5: Top SHAP Features and Cross-Dataset Attribution Agreement.**
  - *Description:* Lists the top selected features, their modality, and the Spearman/Jaccard metrics proving cross-dataset stability.
