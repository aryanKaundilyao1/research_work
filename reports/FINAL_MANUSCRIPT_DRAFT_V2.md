# FINAL MANUSCRIPT DRAFT V2

## TITLE CANDIDATES

1. **Zero-Shot Stress-Label Transfer in Wearable Physiological Monitoring via Target-Domain Baseline Calibration**
2. **Diagnosing and Mitigating Modality-Specific Domain Shift in Cross-Dataset Wearable Stress Detection**
3. **Subject-Specific Baseline Referencing Improves Cross-Dataset Generalization of Wearable Stress Representations**

**Selected Title:**
Subject-Specific Baseline Referencing Improves Cross-Dataset Generalization of Wearable Stress Representations

---

## ABSTRACT

**Background:** Machine learning models for physiological stress detection often demonstrate strong internal validation performance, but this can substantially overestimate cross-cohort generalizability. Models frequently overfit to dataset-specific absolute physiological limits and laboratory-specific physical protocols, creating severe domain mismatch during independent external evaluation.
**Methods:** To systematically evaluate representation stability, we established a strict source-to-target transfer framework utilizing the WESAD cohort ($N=15$) and an independent target cohort ($N=31$). An XGBoost classifier was trained exclusively on WESAD. We compared the external transfer of an absolute multimodal representation against an ablated physiological pipeline utilizing subject-specific baseline-relative normalization. This calibration used target-subject baseline physiological measurements, ensuring a zero-shot transfer with respect to target stress labels. 
**Results:** Internal WESAD evaluation using the absolute representation yielded strong performance (ROC-AUC = 0.964). However, external zero-shot evaluation failed severely (ROC-AUC = 0.423). Diagnostic analysis identified the accelerometer as a massive domain-shift confound reflecting protocol differences (Cohen's $d \approx -1.47$), and its ablation partially improved transfer (ROC-AUC = 0.540). Transitioning to the subject-specific baseline-relative physiological representation substantially recovered generalization in the evaluated external cohort (ROC-AUC = 1.000). Furthermore, cross-dataset SHapley Additive exPlanations (SHAP) feature attribution was highly conserved (Spearman $\rho = 0.9527$, Top-20 Jaccard = 1.000).
**Conclusion:** Protocol-sensitive modalities (like accelerometry) and absolute physiological variations severely compromise cross-dataset generalization. Under the evaluated laboratory protocols, subject-specific baseline referencing mitigates this domain shift, yielding a stable physiological representation capable of label-free external transfer.

## KEYWORDS
Wearable Sensors, Physiological Stress, Domain Shift, Generalization, Baseline Calibration.

---

*(End of Stage 1)*
