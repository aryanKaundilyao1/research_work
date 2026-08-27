# Manuscript Figure Plan

## Figure 1: Overall Study Workflow and Evaluation Framework
- **Source File:** (To be generated via block diagram / TikZ in LaTeX)
- **Caption:** *Figure 1. Experimental workflow. The model is trained exclusively on the WESAD source cohort using an absolute representation. The frozen pipeline is then evaluated zero-shot on the independent Dataset B target cohort. Modality ablation and subject-specific baseline-relative normalization are sequentially applied to diagnose and mitigate cross-dataset domain shift.*
- **What it demonstrates:** The strict separation of internal validation from zero-shot external generalization, enforcing leakage control.
- **Why it matters:** Proves to the reviewer visually that no target-domain information was used for adaptation.

## Figure 2: Internal versus External Performance Collapse
- **Source File:** (Bar chart generated from `final_statistical_table.md`)
- **Caption:** *Figure 2. Comparison of internal validation (WESAD LOSO-CV) against external zero-shot generalization (Dataset B) using the absolute multimodal representation (Exp 1 vs. Exp 3).*
- **What it demonstrates:** The catastrophic drop in ROC-AUC from 0.964 to 0.423.
- **Why it matters:** Establishes the core problem—internal metrics do not guarantee generalizability due to shortcut learning on cohort-specific absolutes.

## Figure 3: Feature Distribution and ACC Domain-Shift Diagnosis
- **Source File:** (Boxplots from Phase 6 diagnostic scripts, e.g., ACC Z mean vs. EDA tonic mean)
- **Caption:** *Figure 3. Modality-specific distribution shifts across datasets. Accelerometer features (e.g., ACC Z mean) exhibit severe distributional divergence (Cohen’s $d \approx -1.47$) due to differing experimental physical protocols, acting as a domain-shift confound.*
- **What it demonstrates:** That the failure in Fig 2 is largely driven by the model attempting to use physical posture/movement to predict stress in a dataset with a different posture protocol.
- **Why it matters:** Justifies the removal of ACC features for cross-dataset transfer.

## Figure 4: Ablation and Baseline-Relative Recovery
- **Source File:** `reports/final_hardening/relative_modality_ablation.png`
- **Caption:** *Figure 4. ROC curve comparison of external transfer performance. Ablating the accelerometer from the absolute representation (Exp 4) provides marginal improvement. Transitioning to a subject-specific baseline-relative physiological representation (Exp 5) substantially recovers zero-shot transferability.*
- **What it demonstrates:** The sequential recovery of the model by addressing both modality shift (ACC) and absolute physiological variation.
- **Why it matters:** This is the primary methodological result of the paper.

## Figure 5: External Subject-Level Stress Probability Separation
- **Source File:** `reports/final_hardening/subject_margin_plot.png`
- **Caption:** *Figure 5. Subject-level predicted probability margins for Dataset B using the relative physiological representation. For all 31 evaluated subjects, the median predicted stress probability remains strictly higher than the median predicted baseline probability.*
- **What it demonstrates:** That the AUC of 1.000 is not driven by a few outlier subjects, but is a consistent, strictly positive margin across the entire finite cohort.
- **Why it matters:** Defends against the reviewer critique that the high AUC is a window-level evaluation artifact.

## Figure 6: Cross-Dataset SHAP Feature Agreement
- **Source File:** (Scatter plot of WESAD SHAP vs. Dataset B SHAP, data from `final_shap_audit.md`)
- **Caption:** *Figure 6. SHAP feature attribution agreement between internal (WESAD) and external (Dataset B) evaluation of the baseline-relative model. The highly conserved feature ranking (Spearman $\rho = 0.9527$, Top-20 Jaccard = 1.000) indicates stable representation transfer.*
- **What it demonstrates:** The model relies on the exact same physiological features to make predictions in both cohorts.
- **Why it matters:** Proves the zero-shot recovery in Fig 4/5 is due to true physiological representation stability, not the model latching onto spurious new correlations in the target dataset.

---
*(Note: Secondary figures such as permutation null distributions and baseline duration robustness plots are reserved for the Supplementary Material.)*
