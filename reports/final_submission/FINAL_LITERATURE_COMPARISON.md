# Final Literature Comparison

The following table contextualizes the proposed strictly temporal, baseline-anchored pipeline against existing approaches in wearable stress detection.

| Study | Modalities | Evaluation Paradigm | Target Cohort Size | Domain Transfer Strategy | Result |
|-------|------------|---------------------|--------------------|--------------------------|--------|
| Schmidt et al. (2018) | EDA, ECG, RESP, etc | Intra-dataset CV | 15 (WESAD) | None (Source-only) | 93% accuracy |
| Koldijk et al. (2014) | ECG, Posture, Facial | Intra-dataset CV | 25 (SWELL-KW) | None | Baseline performance |
| Prajod et al. (2022) | EDA, ECG | Cross-dataset (Zero-shot) | 15/25 | Zero-shot standard | Severe performance drop |
| Nkurikiyeyezu et al (2019) | HRV | Intra-dataset | 18 | Personalization | Personalized > Global |
| Siirtola et al. (2021) | EDA | Cross-device | 20 | Subject-specific centering | Robust to device shift |
| Kyriakou et al. (2019) | EDA, BVP | Cross-corpus | 20 | Target zero-mean | Fails to generalize |
| Hossain et al. (2022) | EDA, TEMP | Lab-to-field | 30 | Active Domain Adaptation | Requires target labels |
| **This Study** | **EDA, BVP, TEMP, ACC** | **Cross-dataset (Strict)** | **35 (Hongn)** | **30s Calibration Anchoring** | **0.7810 AUROC (Zero Target Stress Labels)** |

## Summary of Contributions
1. **Strict Temporal Separation:** Unlike studies that use entire baselines for normalization (implicitly leaking future temporal states into early evaluation windows), this study strictly bounds calibration to an initial 30s period, preserving a separate 30s buffer before evaluation begins.
2. **True Zero-Shot Label Transfer:** The method requires exactly zero labels from the target distribution for stress induction; it relies purely on a brief, neutral calibration period from the target subject.
3. **Reproducible Bounds:** Confidence intervals are explicitly mapped to participant subsets (N=21 eligible), whereas most cross-dataset literature reports window-wise metrics that violate independent and identically distributed (IID) assumptions.
