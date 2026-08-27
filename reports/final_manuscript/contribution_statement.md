# Contribution Statement

The central scientific contribution of this study is the systematic isolation and diagnosis of modality-specific distribution shifts in cross-dataset wearable stress detection, combined with the demonstration that a subject-specific, baseline-relative physiological representation enables robust, strict zero-shot transfer across independent cohorts. 

Specifically, we contribute:

1. **Diagnosis of Accelerometer-Induced Domain Shift:** We explicitly decouple the predictive utility of physiological sensors (EDA, BVP, TEMP) from movement sensors (ACC). We demonstrate that while ACC features are highly predictive within a single dataset, they induce severe cross-dataset generalization failure by capturing dataset-specific experimental artifacts rather than universal physiological stress responses.
2. **Validation of Zero-Shot Physiological Transfer:** We evaluate the efficacy of subject-specific baseline normalization without relying on any active domain adaptation or target-domain stress labels. We prove that relative physiological deviations are substantially more robust to environmental and population shifts than absolute physiological measurements.
3. **Cross-Dataset Representational Stability via SHAP:** Rather than merely relying on target accuracy metrics, we introduce the use of cross-dataset SHAP feature attribution agreement (Spearman $\rho = 0.9527$, Top-20 Jaccard = $1.000$) to prove that the rescued zero-shot performance is driven by a stable, functionally equivalent physiological representation rather than spurious target-side correlations.
4. **Rigorous Subject-Level Evaluation Protocol:** We provide a transparent evaluation methodology that prevents statistical leakage by enforcing subject-level aggregation of correlated overlapping windows, thereby preventing degenerate and overly optimistic confidence intervals that plague physiological ML literature.
