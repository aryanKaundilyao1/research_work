# Phase 18: Final Paper Positioning

Based on the completed scientific hardening and literature audit, this document outlines the exact framing for the manuscript to ensure scientific rigor and novelty without overclaiming.

## A. Proposed Title (5 Options)
1. *Diagnosing Modality Shift in Cross-Dataset Stress Detection: Accelerometer Failure and Physiological Recovery via Baseline Normalization*
2. *Zero-Shot Cross-Dataset Transfer of Wearable Stress Models using Baseline-Relative Physiological Representations*
3. *Robustness of Wearable Stress Detection: Eliminating Modality Shift and Validating Representational Transfer across Datasets*
4. *Subject-Specific Baseline Normalization Rescues Cross-Dataset Transfer in Physiological Stress Detection*
5. *Why Generalization Fails in Wearable Stress Detection: Identifying Accelerometer Domain Shift and Restoring Transferability*

## B. One-Sentence Contribution
We demonstrate that the catastrophic failure of wearable stress models during cross-dataset transfer is largely driven by accelerometer-induced domain shift, and we prove that a baseline-relative transformation of purely physiological signals (EDA, BVP, TEMP) restores zero-shot generalizability while preserving stable feature attributions.

## C. Primary Research Question
Why do machine learning models for stress detection, which achieve near-perfect internal validation performance, fail catastrophically when evaluated on unseen external datasets, and how can this failure be mitigated in a zero-shot setting?

## D. Secondary Research Questions
- Which sensor modality contributes most to the out-of-distribution (OOD) shift?
- Does subject-specific baseline normalization of physiological signals rescue external transferability?
- Does the model rely on the same underlying feature representation before and after transfer?

## E. Hypotheses
- **H1**: The inclusion of accelerometer features, which capture dataset-specific experimental protocols rather than physiological stress, causes severe domain shift.
- **H2**: Transforming absolute physiological signals into subject-specific baseline-relative representations eliminates non-stationarity and allows models to generalize zero-shot.

## F. Main Novelty Claim
We systematically isolate modality-specific distribution shifts (ACC vs. Physio) in cross-dataset transfer and introduce cross-dataset SHAP feature attribution agreement to validate that the recovered zero-shot performance relies on a stable, transferable representation rather than spurious correlations.

## G. Claims We Must NOT Make
- We have "solved" universal stress detection.
- We have identified "causal biomarkers" for stress.
- Subject-specific baseline normalization is a newly invented algorithm (it is a standard technique that we are validating for *cross-dataset zero-shot transfer*).
- The 1.000 AUC guarantees perfect performance in the real world (the bootstrap audit shows it is an artifact of the clean separability within the evaluated cohort).

## H. Strongest Result
The complete recovery of Dataset B performance (ROC-AUC from 0.539 to 1.000) using a frozen WESAD-trained model, coupled with a highly significant SHAP Spearman rank correlation ($\rho > 0.99$) between the internal and external datasets.

## I. Biggest Limitation
The perfect 1.000 external AUC, while robust to bootstrapping and permutation, is likely an artifact of Dataset B's specific composition (e.g., highly controlled laboratory stressors with large physiological effect sizes). Real-world ambulatory data will exhibit much smaller margins of separation.

## J. Closest Prior Work
Smith et al. (2024): *Cross-domain generalisation of physiological stress detection* (WESAD to SWELL-KW transfer using baseline normalization).

## K. Exact Differentiation from Closest Prior Work
Unlike prior work that relies on active Domain Adaptation (updating model parameters based on target distributions), our approach demonstrates *strict zero-shot transfer*. Furthermore, we are the first to explicitly ablate the accelerometer to diagnose the root cause of the initial failure and utilize SHAP attribution agreement to prove representational stability across datasets.

## L. Recommended Target Journal/Conference Categories
- *IEEE Journal of Biomedical and Health Informatics (JBHI)*
- *ACM Transactions on Computing for Healthcare*
- *IMWUT / UbiComp*
- *CHIL (Conference on Health, Inference, and Learning)*

## M. Publication Readiness Assessment
**READY FOR DRAFTING**. All rigorous audits (leakage, degeneracy, bootstrapping, permutations) have passed, and the narrative has been accurately constrained to avoid overclaiming.

## N. Recommended Final Manuscript Structure
1. **Introduction**: The promise of wearable stress detection and the reality of cross-dataset failure.
2. **Related Work**: Domain shift, baseline normalization, feature attribution.
3. **Methods**: Datasets (WESAD, Dataset B), Feature Extraction, The Baseline-Relative Transformation, XGBoost Pipeline.
4. **Experiments**: 
   - Exp 1: The Illusion of Internal Success (WESAD LOSO)
   - Exp 2/3: The Cross-Dataset Failure (Absolute + ACC)
   - Exp 4: Modality Diagnosis (Absolute - ACC)
   - Exp 5: The Recovery (Relative - ACC)
5. **Robustness Audits**: Baseline Duration Sensitivity, Model Comparison (LR vs XGB), Subject Bootstrapping, Negative Permutation Control.
6. **Interpretability**: Cross-Dataset SHAP Agreement.
7. **Discussion & Limitations**: Interpreting the 1.000 AUC, real-world applicability.
8. **Conclusion**.
