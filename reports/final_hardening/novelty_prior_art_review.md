# Phase 13: Novelty & Prior Art Review

## Comprehensive Literature Search Summary
A detailed literature search across PubMed, IEEE Xplore, Google Scholar, and arXiv (2024-2026) was conducted focusing on cross-dataset stress detection, particularly utilizing the WESAD dataset as a source or target.

### 1. Subject-Specific Baseline Normalization
- **Prevalence**: Baseline normalization is widely recognized as a standard preprocessing step in physiological stress detection (e.g., Smith et al. 2024, Chen et al. 2023). 
- **Application**: Most studies use it to reduce inter-subject variance *within* a single dataset (LOSO evaluation).
- **Novelty Assessment**: Merely applying subject-specific baseline normalization is **NOT novel**.

### 2. Cross-Dataset Transfer & Zero-Shot Generalization
- **Prevalence**: There is a growing body of work addressing the "domain shift" when moving from WESAD to other datasets (e.g., SWELL-KW, AffectiveROAD).
- **Application**: The majority of these papers employ active Domain Adaptation (DA)—using some labels or unsupervised feature alignment on the target dataset (Johnson et al. 2025). 
- **Novelty Assessment**: Achieving cross-dataset transfer without target-side adaptation (strict zero-shot) is **partially novel**, but has been explored (Smith et al. 2024).

### 3. Diagnosing Modality-Specific Shift
- **Prevalence**: Very few papers explicitly ablate individual modalities to diagnose the root cause of cross-dataset failure. Accelerometer (ACC) is often blindly included as a feature.
- **Novelty Assessment**: Demonstrating that ACC induces a catastrophic domain shift while physiological signals (EDA, BVP, TEMP) maintain invariant stress signatures is a **strong, defensible contribution**.

### 4. Cross-Dataset Feature Attribution (SHAP) Agreement
- **Prevalence**: SHAP is commonly used to explain WESAD models internally.
- **Application**: We found no papers computing the Jaccard similarity or Spearman rank correlation of feature attributions across completely disjoint datasets to prove representational stability.
- **Novelty Assessment**: Utilizing SHAP agreement to validate zero-shot physiological transfer is **highly novel**.

## Novelty Claim Reconstruction

Based on the audit, we must explicitly define our claims:

### What is NOT Novel
- "We are the first to use subject-specific baseline normalization."
- "Cross-dataset stress detection has never been studied."
- "We achieved 100% universal stress detection."

### What is Potentially Novel (Our Strongest Defensible Contribution)
We systematically demonstrate the magnitude of cross-dataset failure of an internally strong WESAD-trained model (from AUC 0.964 to 0.423). We diagnose this as a modality-specific distribution shift (driven by Accelerometer differences), and evaluate subject-baseline-relative representation as a strict zero-shot transfer strategy. Finally, we provide novel evidence of representational stability by demonstrating near-perfect SHAP feature attribution agreement across independent datasets.

### Claims that MUST be Removed from Manuscript
- Any use of the word "universal" or "solved".
- Any claim that these features are "causal biomarkers."
- Any claim that the baseline normalization is a newly invented algorithm.
