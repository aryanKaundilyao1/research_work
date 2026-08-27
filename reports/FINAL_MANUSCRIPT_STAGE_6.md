# Abstract

**Background:** Wearable physiological sensing enables continuous automated stress detection, yet models often fail to generalize across independent datasets due to inter-person variability and protocol-specific artifacts. 

**Objective:** This study evaluates whether a source-trained multimodal stress classifier transfers to an independent target dataset, and investigates whether a subject-specific baseline-relative physiological representation improves label-free cross-dataset transfer.

**Methods:** Utilizing a strict source-to-target frozen pipeline, an XGBoost classifier was trained on the WESAD dataset (source domain, $N=15$). The absolute representation pipeline was then evaluated on Dataset B (independent target domain, evaluated $N=31$) using zero-shot stress-label transfer. Modality-specific domain shift was diagnosed via an accelerometer ablation study. Finally, the absolute physiological features were replaced with a subject-specific baseline-relative representation calibrated exclusively using unlabeled target baseline measurements. Feature attribution stability was evaluated using SHAP (SHapley Additive exPlanations).

**Results:** The absolute multimodal representation achieved strong internal performance (LOSO-CV ROC-AUC = 0.964) but suffered substantial external degradation (ROC-AUC = 0.423). Accelerometer features exhibited substantial distribution shift (Cohen's $d \approx -1.47$); their ablation partially improved transfer (ROC-AUC = 0.540). The subject-specific baseline-relative representation substantially improved zero-shot stress-label transfer, yielding an external ROC-AUC of 1.000. Robustness was confirmed via subject-level bootstrap (95% CI [1.000, 1.000]) and task-level permutation (0/1000 permutations achieved or exceeded observed AUC). Cross-dataset SHAP attribution agreement was highly conserved (Spearman $\rho = 0.9527$, Top-20 Jaccard = 1.000).

**Conclusion:** Strong internal validation does not guarantee external generalization. A subject-specific baseline-relative representation successfully mitigated cross-dataset domain shift and enabled robust zero-shot stress-label transfer under the evaluated conditions. Independent replication across diverse cohorts is required to determine the universal viability of this representation-level intervention.

**Keywords:** Affective Computing, Wearable Sensing, Cross-Dataset Generalization, Domain Shift, Physiological Stress Detection, Zero-Shot Transfer, Explainable AI.


# 9. Conclusion

This study addresses the critical challenge of cross-dataset generalization in wearable physiological stress detection. The central finding of this investigation is that absolute multimodal physiological representations are highly vulnerable to domain mismatch, but that subject-specific baseline calibration can substantially recover generalization under the evaluated source-target setting.

The stark performance inversion between the internal WESAD evaluation (ROC-AUC = 0.964) and the absolute external transfer to Dataset B (ROC-AUC = 0.423) demonstrates that strong internal validation is insufficient to guarantee external robustness. The empirical diagnostic revealed that accelerometer distributional differences (Cohen's $d \approx -1.47$) were consistent with protocol-related movement differences, contributing to the observed domain mismatch. However, the partial recovery achieved by accelerometer ablation (ROC-AUC = 0.540) indicated that modality-specific shift was not the sole confound. 

By standardizing physiological features relative to each target subject's resting state, the baseline-relative representation isolated relative physiological changes and achieved an external ROC-AUC of 1.000. This evaluation constitutes zero-shot stress-label transfer, as target stress labels were strictly withheld from model fitting and calibration, relying solely on unlabeled target baseline measurements. The strong cross-dataset SHAP attribution agreement ($\rho = 0.9527$, Top-20 Jaccard = 1.000) provides complementary evidence of stable model decision structure, confirming that the baseline-relative classifier relied on a conserved physiological representational logic across independent domains. 

The primary limitation of this study is its reliance on a single source cohort ($N=15$) and a single evaluated target cohort ($N=31$). While the robustness analyses confirmed statistical stability within this specific target distribution, these findings must be interpreted cautiously. Independent replication across additional, diverse physiological datasets and unconstrained protocols is required to establish the broader viability of subject-specific baseline calibration as a generalized mitigation strategy for domain shift in wearable computing.
