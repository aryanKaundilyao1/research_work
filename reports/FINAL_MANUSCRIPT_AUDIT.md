# Final Manuscript Audit (Stage 6)

## PART C — CITATION AUDIT

The following table tracks all instances of `[CITATION NEEDED]` throughout the generated manuscript (Stages 2-6) mapped to the requested categories.

| Section | Claim | Citation needed? | Recommended source type |
|---|---|---|---|
| 1. Intro | Psychological stress affects cognitive performance... | YES | A. Core background citations |
| 1. Intro | Responses commonly include changes in autonomic nervous system activity... | YES | A. Core background citations |
| 1. Intro | Wearable sensing platforms have made it possible to track... | YES | B. Wearable stress detection |
| 1. Intro | ...does not necessarily imply robust external generalization | YES | I. Generalization/leakage |
| 1. Intro | Individuals exhibit different resting skin temperatures... | YES | E. Physiological baseline normalization |
| 1. Intro | ...encode the physical structure of the experimental protocol | YES | D. Domain shift / domain adaptation |
| 1. Intro | ...studies emphasize within-dataset validation... | YES | I. Generalization/leakage |
| 2.1 Related Work | ...signals such as EDA, PPG, and skin temperature... | YES | B. Wearable stress detection |
| 2.1 Related Work | The WESAD dataset established an early benchmark... | YES | B. WESAD original dataset |
| 2.1 Related Work | ...including the Wearable Exam Stress Dataset (Dataset B)... | YES | C. Dataset B original dataset |
| 2.2 Related Work | Covariate shift and domain shift occur when... | YES | D. Domain shift / domain adaptation |
| 2.2 Related Work | ...established Domain Adaptation approaches often utilize techniques such as unsupervised feature alignment, MMD... | YES | D. Domain shift / domain adaptation |
| 2.3 Related Work | Physiological signal normalization is a standard preprocessing step... | YES | E. Physiological baseline normalization |
| 2.3 Related Work | ...computing relative physiological features using Z-score transformations... | YES | E. Physiological baseline normalization |
| 2.4 Related Work | ...interpretability has become critical for ensuring scientific validity... | YES | H. SHAP / explainability |
| 2.4 Related Work | SHAP is a widely adopted framework... | YES | H. SHAP / explainability |
| 5.2 Methods | The Wearable Stress and Affect Detection (WESAD) dataset... | YES | B. WESAD original dataset |
| 5.3 Methods | Dataset B (the Wearable Exam Stress Dataset) serves as... | YES | C. Dataset B original dataset |
| 5.9 Methods | The classification engine is an Extreme Gradient Boosting (XGBClassifier)... | YES | F. XGBoost |
| 5.14 Methods | ...SHapley Additive exPlanations (SHAP) values... | YES | H. SHAP / explainability |
| 5.15 Methods | Data leakage compromises physiological machine learning evaluations... | YES | I. Generalization/leakage |
| 8.8 Discussion | ...demonstrated strong internal stress detection performance using multimodal physiological representations... | YES | B. Wearable stress detection |
| 8.8 Discussion | Established Domain Adaptation (DA) techniques, such as MMD or adversarial alignment... | YES | D. Domain shift / domain adaptation |
| 8.8 Discussion | ...subject-specific baseline normalization, a long-standing preprocessing technique in biomedical signal analysis... | YES | E. Physiological baseline normalization |

---

## PART D — FINAL NUMERICAL AUDIT

- **WESAD N = 15:** PASS
- **Dataset B N = 31:** PASS
- **Internal AUC = 0.964:** PASS
- **External absolute AUC = 0.423:** PASS
- **ACC ablation AUC = 0.540:** PASS
- **Relative AUC = 1.000:** PASS
- **Cohen's d ≈ -1.47:** PASS
- **Bootstrap = 5000 iterations:** PASS
- **Bootstrap CI = [1.000, 1.000]:** PASS
- **Permutation = 1000 iterations:** PASS
- **Permutation exceedances = 0:** PASS
- **SHAP Spearman ρ = 0.9527:** PASS
- **Top-20 Jaccard = 1.000:** PASS

*Overall numerical consistency status:* **PASS**.

---

## PART E — SCIENTIFIC LANGUAGE AUDIT

1. **Unsupported causal claims:** PASS. ("contributes to," "suggests," "indicates," rather than "causes.")
2. **Biological causality claims:** PASS. (Explicitly stated that SHAP does not equal biological causality.)
3. **Clinical validity claims:** PASS. (Explicitly rejected.)
4. **Universal generalization claims:** PASS. (Explicitly confined to "the evaluated cohorts and protocols"; calls for replication.)
5. **Overstated novelty claims:** PASS. (Avoided "the first to show" language.)
6. **Incorrect use of "zero-shot":** PASS. (Always qualified as "zero-shot stress-label transfer".)
7. **Confusion between target-label-free and target-data-free:** PASS. (Explicitly clarified in discussion and conclusion that baseline data was used, but labels were withheld.)
8. **Claims that ACC is inherently non-physiological:** PASS. (Framed as recording protocol-related movement differences without claiming movement is non-physiological.)
9. **Claims that baseline normalization universally removes domain shift:** PASS. (Qualified to "substantially improves transfer in the evaluated source-target setting.")
10. **Claims that SHAP proves biological equivalence:** PASS. (Specifically states it provides evidence of "stable model decision structure" but not "biological equivalence.")

*Sentences requiring revision:* None.

---

## PART F — CONSISTENCY AUDIT

- "Dataset B" rather than inventing alternative names: PASS
- N=31 for the evaluated target cohort: PASS
- "baseline-relative representation": PASS
- "absolute representation": PASS
- "zero-shot stress-label transfer": PASS
- "cross-dataset domain shift": PASS
- "protocol-related movement differences": PASS
- "SHAP attribution agreement": PASS

Old paper contamination check:
- Phase segmentation: ABSENT (PASS)
- Beginning/Middle/End phases: ABSENT (PASS)
- 30 recordings: ABSENT (PASS)
- AUC=0.801: ABSENT (PASS)
- Old Dataset B sample counts: ABSENT (PASS)
- Unsupported protocol claims: ABSENT (PASS)

*Overall consistency status:* **PASS**.

---

## PART G — CONTRIBUTION AUDIT

The final manuscript strictly supports the four audited contributions:
1. Strict internal-to-external source-to-target transfer evaluation (Exp 1, Exp 3).
2. Domain-shift diagnosis and accelerometer ablation (Exp 2, Exp 4).
3. Subject-specific baseline-relative calibration for label-free external transfer (Exp 5, Robustness).
4. Cross-dataset SHAP attribution analysis (Exp 6).

No unsupported fifth contribution has been introduced.
*Overall contribution status:* **PASS**.

---

## PART H — FINAL MANUSCRIPT STATUS

- **Conclusion:** COMPLETE
- **Abstract:** COMPLETE
- **Citation audit:** COMPLETE
- **Numerical consistency:** PASS
- **Scientific language:** PASS
- **Terminology consistency:** PASS
- **Old-paper contamination:** PASS
- **Contribution consistency:** PASS

**STAGE 6 COMPLETE**

---

### Remaining work before submission

1. **Resolve Citation Placeholders:** Replace all 24 identified `[CITATION NEEDED]` placeholders with the correct IEEE-formatted references from the finalized Reference Audit.
2. **Compile Final Manuscript Document:** Merge the Abstract, Introduction/Related Work (Stage 2), Methods (Stage 3), Results (Stage 4), Discussion (Stage 5), and Conclusion (Stage 6) into a single master document.
3. **Format Tables and Figures:** Finalize the 6 tables outlined in the Results prompt, construct the 6 specified figures using the underlying experimental data artifacts, and insert them into the master document.
