# Supplementary Material Plan

In order to keep the main manuscript focused on the central scientific chain of evidence (Internal Success $\rightarrow$ External Failure $\rightarrow$ Modality Diagnosis $\rightarrow$ Relative Recovery), several critical but secondary hardening analyses will be provided in the Supplementary Material.

## Section S1: Robustness Audits
1. **Baseline Duration Sensitivity:** Table demonstrating the stability of the AUC (1.000) when the subject-specific baseline reference period is reduced from "Full" to 30, 60, 120, 180, and 300 seconds. (Source: `baseline_duration_sensitivity.csv`)
2. **Model Simplicity Comparison:** Table comparing the XGBoost pipeline to a standard Logistic Regression pipeline. This proves that under relative normalization, the physiological representation becomes linearly separable, suggesting the representation is robust independent of the model architecture. (Source: `model_comparison.csv`)
3. **Modality Ablation under Relative Normalization:** Expanded table isolating EDA, BVP, TEMP, and their combinations to show how TEMP and BVP provide independent signal while EDA acts synergistically. (Source: `relative_modality_ablation.csv`)

## Section S2: Statistical and Evaluation Controls
1. **Subject-Level Bootstrapping:** A detailed discussion of the 5,000-iteration subject-level bootstrap. This section will explicitly discuss the degenerate confidence intervals (e.g., `[1.0, 1.0]`) and interpret them not as universal perfection, but as proof that the large probability margin within the finite Dataset B cohort is robust to subject-level resampling. (Source: `bootstrap_audit.md`)
2. **Permutation Negative Control:** The null distribution resulting from subject-level label shuffling, establishing the empirical $p=0.0000$ and confirming the evaluation pipeline is free of structural artifacts. (Source: `permutation_negative_control.md`)
3. **Task-Specific Response Analysis:** Evaluation breaking down the target-domain classification probability by individual tasks (TMCT vs Opinion vs Subtract) to demonstrate that the model generalized to the physiological state rather than a specific physical protocol. (Source: `task_response_analysis.md`)

## Section S3: Dataset and Feature Details
1. **Complete 234-Feature Set:** A table listing the exhaustive set of all time-domain, frequency-domain, and non-linear features computed per sensor channel.
2. **Exclusion Criteria Sensitivity:** Proof that excluding vs. including specific hardware-failed subjects (e.g., f07, f14) changes absolute numbers but does not alter the fundamental scientific conclusions regarding the ACC-domain shift or the relative-recovery. (Source: `exclusion_sensitivity.md`)
