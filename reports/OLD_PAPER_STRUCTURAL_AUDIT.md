# Previous Paper Structural Audit

## 1. Title Structure
- **Old:** Focused on phase-aware classification.
- **Verdict:** Completely rewrite. The new paper is about cross-dataset generalization, not phase segmentation.

## 2. Abstract Structure
- **Old:** Structured (Background, Methods, Results, Conclusion).
- **Verdict:** Retain the structured format. The content must be completely rewritten.

## 3. Introduction Structure
- **Old:** Good flow from general wearable sensing to a specific dataset limitation (treating the exam as a single block).
- **Verdict:** Retain the paragraph flow (general -> specific -> gap -> contribution) but rewrite the gap to focus on the failure of internal validation and domain shift.

## 4. Related Work Structure
- **Old:** Divided into sub-topics (Wearable Stress, Temporal Analysis, Tree-Based ML, Explainable AI).
- **Verdict:** Retain thematic subsections, but change the themes to Wearable Stress, Cross-Dataset Generalization, Subject-Specific Baseline Normalization, and Interpretability.

## 5. Research Problem / Gap
- **Old:** The gap was the lack of temporal segmentation during exams.
- **Verdict:** Completely rewrite. The new gap is the catastrophic drop in cross-dataset generalization due to absolute physiological limits and modality-specific domain shifts (accelerometry).

## 6. Methodology Organization
- **Old:** Very clear step-by-step subsections (Dataset, Preprocessing, Feature Extraction, Model Development).
- **Verdict:** Retain this explicit, reproducible structure. It is excellent.

## 7. Dataset Description
- **Old:** Described Dataset B (N=10 students, 30 exams).
- **Verdict:** Expand. We must describe *both* WESAD (source, N=15) and Dataset B (target, evaluated N=31). The old paper claims N=10/30 exams, which conflicts with our current evaluated N=31. We must strictly use our audited N=31.

## 8. Feature Extraction Description
- **Old:** Heavily focused on phase-specific statistics.
- **Verdict:** Remove the phase segmentation focus. Replace with a detailed mathematical description of the absolute vs. subject-specific baseline-relative representations.

## 9. Model Description
- **Old:** Explained XGBoost, ANOVA, and SMOTE well.
- **Verdict:** Retain the technical depth here. The explanation of why XGBoost fits tabular physiological data is good and should be kept.

## 10. Experimental Design
- **Old:** Only described a single internal LOSO validation on Dataset B.
- **Verdict:** Completely rewrite. The new paper requires a 6-phase experimental design (Internal -> External Absolute -> ACC Ablation -> External Relative -> Robustness -> SHAP).

## 11. Results Presentation
- **Old:** Clearly separated classification performance, SHAP, phase-wise analysis, permutation test.
- **Verdict:** Retain the clear separation, but the content will follow the new 6-phase experimental narrative.

## 12. Discussion Structure
- **Old:** Reflected directly on the results and their physiological meaning.
- **Verdict:** Retain. The discussion of SHAP features in physiological terms was done well and should be modeled for our cross-dataset SHAP agreement section.

## 13. Limitations
- **Old:** Honest about sample size, single setting, and SMOTE limitations.
- **Verdict:** Retain the honesty and expand it to include the AUC=1.000 artifact, overlapping windows, and the necessity of target baseline calibration.

## 14. Conclusion
- **Old:** Concise summary.
- **Verdict:** Retain the conciseness, but rewrite the claims.

## 15. Tables
- **Old:** Hyperparameter tables, result metrics.
- **Verdict:** Expand to the 6 tables outlined in the `FINAL_TABLE_AUDIT.md`.

## 16. Figures
- **Old:** Workflow diagrams, segmentation strategy, confusion matrix, SHAP plots.
- **Verdict:** Retain the visual style. The new study workflow, ACC shift distribution, and Cross-Dataset SHAP scatter plot will replace the old figures.

## 17. References
- **Old:** 11 references.
- **Verdict:** Expand heavily using the `FINAL_PRIOR_ART_MATRIX.md`.

## 18. Citation Style
- **Old:** IEEE.
- **Verdict:** Retain.

## 19. Writing Style
- **Old:** Accessible but formal biomedical engineering style.
- **Verdict:** Retain. It is not overly hyped.

## 20. Technical Depth
- **Old:** Provided equations for interpolation and Z-score.
- **Verdict:** Retain this practice. We must provide the exact equation for our baseline-relative normalization.
