# Stage 1.5 Manuscript Strategy

This document synthesizes the structural benefits of the old paper with the rigorous scientific authority of the new audited evidence, forming the master plan for writing Stages 2 through 7.

## 1. Final Recommended Paper Title
*Subject-Specific Baseline Referencing Improves Cross-Dataset Generalization of Wearable Stress Representations*

## 2. Central Research Question
To what extent do absolute physiological levels and modality-specific artifacts cause cross-dataset generalization failure in wearable stress detection, and can subject-specific baseline referencing recover label-free transferability?

## 3. Main Hypothesis
Absolute multimodal representations overfit to cohort-specific distributions and physical protocols. Transforming physiological features into relative deviations calibrated on a target subject's unlabeled baseline will substantially improve zero-shot stress-label transfer.

## 4. Secondary Hypotheses
- The accelerometer captures dataset-specific physical experimental protocols, creating severe domain mismatch.
- A model trained on a relative physiological representation in the source domain will utilize the same attribution logic (SHAP) in the target domain.

## 5. Core Novelty Claim
We provide the first explicit quantification of how subject-specific baseline referencing rescues zero-shot stress-label transfer across independent wearable protocols without requiring unsupervised Domain Adaptation feature alignment.

## 6. Conservative Novelty Claim
We are the first to demonstrate cross-dataset representational stability for wearable stress using SHAP attribution agreement.

## 7. Exact Narrative
INTERNAL SUCCESS (0.964) $\rightarrow$ EXTERNAL FAILURE (0.423) $\rightarrow$ DOMAIN-SHIFT DIAGNOSIS (ACC $d \approx -1.47$) $\rightarrow$ ACC ABLATION (0.540) $\rightarrow$ ABSOLUTE PHYSIOLOGY STILL FAILS $\rightarrow$ SUBJECT-SPECIFIC BASELINE REFERENCING $\rightarrow$ EXTERNAL RECOVERY (1.000) $\rightarrow$ ROBUSTNESS / NEGATIVE CONTROL (Bootstrap/Permutation) $\rightarrow$ CROSS-DATASET SHAP AGREEMENT ($\rho=0.9527$) $\rightarrow$ CAREFUL LIMITATIONS $\rightarrow$ GENERALIZABILITY IMPLICATION.

## 8. Section-by-Section Purpose
- **Introduction:** Establish the generalization gap.
- **Related Work:** Differentiate from Domain Adaptation and internal normalizations.
- **Research Gap & Contributions:** Formalize the 4 gaps and precise contributions.
- **Methods:** Rigorously document the dual-dataset design, the exact relative transformation, and the strict leakage prevention.
- **Experimental Design:** Define the 6 canonical experiments.
- **Results:** Neutrally report the audited metrics.
- **Discussion:** Interpret *why* absolute representations fail and *why* baseline referencing succeeds.
- **Limitations:** Disarm reviewers regarding the AUC 1.000 artifact and target baseline requirements.

## 9. What the Old Paper Contributes Structurally
- Formal, academic biomedical engineering tone.
- Thematic organization of Related Work.
- Detailed step-by-step Methodology subsections.
- Clear separation of physiological SHAP interpretation.

## 10. What the New Paper Adds Scientifically
- A completely different hypothesis (cross-dataset generalization).
- Dual-dataset evaluation (WESAD $\rightarrow$ Dataset B).
- Explicit domain shift quantification.
- A mathematically audited, frozen pipeline.
- Cross-dataset interpretability agreement.

## 11. Claims That Require Citations
- Wearable sensing is widely used for stress detection.
- Internal validation overestimates real-world generalization.
- Domain Adaptation (like MMD) is the typical, but complex, approach to domain shift.
- WESAD and Dataset B original dataset papers.

## 12. Claims That Require Direct Experimental Evidence
- Internal WESAD performance (Exp 1).
- ACC distribution shift (Exp 2/3).
- Absolute physiological failure (Exp 4).
- Baseline-relative recovery (Exp 5).
- SHAP agreement (Exp 6).

## 13. Claims That Must Be Avoided
- "Universal stress detection."
- "Pure zero-shot" (target baseline is used).
- "Biological causality" or "biomarkers" in a clinical sense.
- "Solving the problem."

## 14. Reviewer Objections We Should Proactively Answer
- *Objection:* You used target data, so it's not zero-shot.
  - *Answer:* We explicitly define it as "zero-shot with respect to target stress labels," noting the calibration requires unlabeled baseline data.
- *Objection:* 1.000 AUC is impossible in the real world.
  - *Answer:* We explicitly state it is a finite-cohort laboratory artifact driven by large effect sizes under controlled conditions.

## 15. Recommended Figure Sequence
1. Study Workflow (Source to Target isolation).
2. Internal vs External Collapse (Bar Chart).
3. ACC Domain-Shift Diagnostic (Distribution).
4. Ablation and Baseline-Relative Recovery (ROC Curves).
5. Subject-Level Probability Margins (Strip plot).
6. Cross-Dataset SHAP Attribution (Scatter Plot).

## 16. Recommended Table Sequence
1. Dataset and Participant Characteristics.
2. Signal Processing and Pipeline Rules.
3. Internal WESAD Performance.
4. External Zero-Shot Transfer and Ablation.
5. Cross-Dataset Attribution Agreement.
6. Robustness Analyses.

## 17. Exact Terminology to Use Consistently
- "Zero-shot stress-label transfer"
- "Subject-specific baseline calibration"
- "Absolute multimodal representation"
- "Baseline-relative physiological representation"
- "Modality-specific domain shift"
