# Final Manuscript Blueprint

This blueprint sets strict constraints for drafting the final paper.

## 1. Abstract
- **Purpose:** Summarize the collapse and recovery of cross-dataset generalization.
- **Allowed Numbers:** 0.964 (Internal), 0.423 (External Absolute), 1.000 (External Relative), $\rho=0.9527$ (SHAP).
- **Forbidden:** Claims of "pure zero-shot" or "universality".

## 2. Introduction
- **Purpose:** Introduce wearable stress detection, frame the domain-shift problem, and explicitly define the evaluation challenge (internal validation overestimates real-world generalization).
- **Claims Allowed:** Absolute representations overfit to cohort-specific distributions.
- **Forbidden:** Claiming the paper proposes a new neural network or causal biological theory.

## 3. Related Work
- **Purpose:** Contextualize against Domain Adaptation (e.g., MMD) and internal uses of baseline normalization.
- **Claims Allowed:** We uniquely evaluate the zero-shot label-transfer capabilities of baseline normalization without unsupervised target feature alignment.

## 4. Materials and Methods
- **Purpose:** Rigorously document the leakage-free pipeline.
- **Required Details:** 
    - WESAD ($N=15$), Dataset B (Original $N=34$, Excluded S02/f14/f07, Evaluated $N=31$).
    - XGBoost classifier, ANOVA SelectKBest ($K=20$) fit on WESAD only, SMOTE on train fold only.
    - Z-score normalization using target-subject unlabeled baseline data.
- **Forbidden:** LightGBM, $K=30$, HR/IBI signals.

## 5. Experimental Design
- **Purpose:** Outline the sequential phases (Exp 1: Internal, Exp 3: External Absolute +ACC, Exp 4: External Absolute -ACC, Exp 5: External Relative -ACC, Exp 6: SHAP).

## 6. Results
- **Purpose:** Report the audited numbers neutrally.
- **Required Evidence:** Table III (0.964), Table IV (0.423 $\rightarrow$ 0.540 $\rightarrow$ 1.000), Cohen's $d \approx -1.47$, Bootstrap CI [1.000, 1.000], Permutation $p < 0.001$, Logistic Regression AUC 0.905, SHAP $\rho=0.9527$.
- **Forbidden:** Speculating *why* ACC failed in the results section (leave for discussion).

## 7. Discussion
- **Purpose:** Interpret the collapse and recovery.
- **Claims Allowed:** ACC encodes physical protocol differences (domain shift). Baseline referencing mitigates inter-subject absolute physiological variance, allowing the model to generalize relative deviation patterns. SHAP proves the model logic is stable.

## 8. Limitations
- **Purpose:** Disarm skeptical reviewers.
- **Required Claims:** The 1.000 AUC is finite-cohort artifact dependent on high laboratory effect sizes. Ambulatory environments will be much harder. Subject-aggregated AUC masks window-level noise. Target baseline data is required.

## 9. Conclusion
- **Purpose:** Concise wrap-up.
- **Claims Allowed:** The transition from internal to external evaluation is severely compromised by ACC domain shift. Subject-specific referencing substantially recovers label-free transferability.
