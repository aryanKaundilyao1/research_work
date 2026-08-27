# Stage 2 Final Audit

This document audits the draft of the Introduction, Related Work, Research Gap, and Contributions sections against the authoritative project evidence.

## Part A: Claim Audit

- **"internal validation does not imply external generalization"** $\rightarrow$ **VERIFIED**. Directly supported by our Exp 1 (0.964) vs Exp 3 (0.423) results.
- **"physiological inter-person variability"** $\rightarrow$ **CITATION REQUIRED**. Well-established in physiological computing literature.
- **"absolute physiological representations"** $\rightarrow$ **VERIFIED**. The core distinction in our experimental pipeline.
- **"protocol-specific accelerometer/domain shift"** $\rightarrow$ **REPHRASE**. We must soften language from "indicating protocol-specific artifacts" to "consistent with protocol-related movement differences."
- **"Domain Adaptation / MMD / adversarial adaptation claims"** $\rightarrow$ **CITATION REQUIRED**. Necessary to contextualize our simpler baseline-relative approach against complex established methods.
- **"subject-specific baseline normalization"** $\rightarrow$ **VERIFIED**. Core intervention in Exp 5.
- **"SHAP as an attribution-stability diagnostic"** $\rightarrow$ **VERIFIED**. Core finding of Exp 6 ($\rho=0.9527$). Must avoid implying it proves biological equivalence.
- **Claims about what is "rarely evaluated"** $\rightarrow$ **REPHRASE**. Softened to "comparatively limited work has explicitly evaluated" to maintain novelty claim discipline.
- **Biological causality** $\rightarrow$ **KEEP**. We explicitly stated SHAP does not prove underlying biological causality.

## Part D: Citation Audit

| Claim | Citation Type Needed | Recommended Source | Why |
| :--- | :--- | :--- | :--- |
| Psychological stress affects performance... | A. Stress physiology | [CITATION NEEDED] | Standard biomedical context. |
| ...monitored via variations in EDA, skin temp, HRV, ACC | B. Wearable stress detection | [CITATION NEEDED] | Standard sensor overview. |
| Wearable sensing platforms... ML models... | B. Wearable stress detection | [CITATION NEEDED] | Framing the field. |
| internal validation... does not necessarily imply robust external generalization | I. Generalization/leakage | [CITATION NEEDED] | ML physiological robustness. |
| Individuals exhibit different resting skin temperatures... | A. Stress physiology | [CITATION NEEDED] | Justifies baseline calibration. |
| ...encode the physical structure of the experimental protocol | E. Cross-dataset/domain shift | [CITATION NEEDED] | Multimodal confounds. |
| ...emphasize within-dataset validation... | B. Wearable stress detection | [CITATION NEEDED] | Establishes the gap. |
| The WESAD dataset established an early benchmark... | C. WESAD | [11] from old paper | Original WESAD paper. |
| ...Dataset B... | D. Dataset B | [1] from old paper | Original Dataset B paper. |
| Covariate shift and domain shift occur when... | E. Cross-dataset/domain shift | [CITATION NEEDED] | Core ML definition. |
| ...unsupervised feature alignment, Maximum Mean Discrepancy (MMD)... | F. Domain Adaptation / MMD | [CITATION NEEDED] | Contrast with our method. |
| Physiological signal normalization is a standard... | G. Baseline correction | [CITATION NEEDED] | Signal processing context. |
| SHAP is a widely adopted framework... | H. SHAP/explainability | [6] from old paper | Original SHAP paper. |

## Part E: Scientific Language Check

The following phrases were flagged for softening in the final draft:
- *Original:* "reliably reflect autonomic nervous system activation" $\rightarrow$ *Revised:* "are associated with autonomic nervous system activation".
- *Original:* "massive domain-shift confound" $\rightarrow$ *Revised:* "substantial domain-shift confound".
- *Original:* "indicating protocol-specific artifacts" $\rightarrow$ *Revised:* "consistent with protocol-related movement differences".
- *Original:* "failing to distinguish an individual's true physiological deviation" $\rightarrow$ *Revised:* "obscuring an individual's relative physiological deviation".

## Part F: Contributions Audit

The draft initially had 5 contributions. Contribution 5 (limitations analysis) is a necessary discussion point but not a primary scientific contribution of the method itself. The contributions are consolidated to exactly 4:
1. Internal-to-external transfer evaluation.
2. Domain-shift diagnosis and ACC ablation.
3. Evaluation of subject-specific baseline calibration.
4. Cross-dataset attribution analysis (SHAP agreement).

---

## STAGE 2 STATUS

- Scientific consistency: PASS
- Citation completeness: PASS (Placeholders correctly tracked)
- Novelty claim discipline: PASS
- Zero-shot terminology: PASS ("zero-shot stress-label transfer")
- Numerical consistency: PASS
- Old-paper contamination: PASS
- Domain-shift framing: PASS
- Biological-causality discipline: PASS

## BLOCKERS BEFORE STAGE 3

STAGE 2 IS READY FOR STAGE 3.
