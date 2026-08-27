# Final Claim Hierarchy

To ensure scientific discipline in the manuscript, all claims are strictly categorized. The manuscript must **never** present a Tier 4 claim as a Tier 1 result.

## TIER 1: DIRECTLY DEMONSTRATED (Empirical Facts)
*These statements can be made unequivocally.*
- Internal LOSO-CV on WESAD achieved an ROC-AUC of 0.964.
- Zero-shot evaluation of the frozen absolute multimodal pipeline on Dataset B resulted in an ROC-AUC of 0.423.
- The mean Z-axis accelerometer feature exhibited a massive distribution shift between datasets (Cohen's $d \approx -1.47$).
- Removing ACC features increased the absolute pipeline's external ROC-AUC from 0.423 to 0.540.
- Subject-specific baseline Z-score normalization of EDA, BVP, and TEMP features (excluding ACC) yielded an external ROC-AUC of 1.000 in the finite ($N=31$) Dataset B cohort.
- The SHAP feature attribution ranking between the internal WESAD evaluation and the external Dataset B evaluation exhibited a Spearman correlation of $\rho = 0.9527$ and a Top-20 Jaccard overlap of 1.000.
- 5000 subject-level bootstrap resamples of the baseline-relative representation maintained a strictly positive probability margin (CI: [1.000, 1.000]).
- A task-level permutation negative control yielded 0 null exceedances out of 1000 permutations ($p < 0.001$).

## TIER 2: STRONGLY SUPPORTED BUT QUALIFIED (Interpretations of Facts)
*These statements must include qualifiers like "in the evaluated cohort" or "substantially improves."*
- Accelerometer features capture dataset-specific physical experimental protocols, contributing significantly to cross-dataset domain mismatch.
- Transforming absolute physiological values into relative deviations mitigates the inter-cohort physiological variance that causes absolute representations to fail.
- Subject-specific baseline referencing provides a highly stable representational transfer between these two laboratory protocols.

## TIER 3: HYPOTHESES / DISCUSSION POINTS
*These are reserved exclusively for the Discussion and Limitations sections.*
- A shorter baseline duration (e.g., 30s) appears sufficient for calibration, which may improve real-world ambulatory feasibility.
- The results suggest Domain Adaptation (which often requires unsupervised feature alignment on target data) may be unnecessary if the fundamental physiological representation is correctly normalized.
- The 1.000 ROC-AUC is highly dependent on the controlled laboratory conditions (e.g., lack of thermal or physical exercise confounds during the target stress task).

## TIER 4: SPECULATION / EXPLICITLY FORBIDDEN
*These phrases and claims must NOT appear anywhere in the final manuscript.*
- ❌ "We have solved cross-dataset stress detection."
- ❌ "The model discovered the true causal biological biomarkers of stress."
- ❌ "This pipeline will achieve 1.000 ROC-AUC in free-living environments."
- ❌ "Light Gradient Boosting Machine (XGBoost)" (Technically false).
- ❌ "Pure zero-shot" (Because target baseline info is used).
- ❌ "Dataset B contains exactly 34 subjects in the final analysis."
