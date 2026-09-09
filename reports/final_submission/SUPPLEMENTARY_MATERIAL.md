# Supplementary Material
**Evaluating Subject-Specific Baseline Calibration for Cross-Dataset Wearable Stress Detection**

## S1. Methodological Justification for 30-Second Calibration Buffer
During the external evaluation on the target cohort (Hongn dataset), the application of standard 5-minute baseline calibration metrics resulted in zero eligible evaluation windows for 14 out of 35 participants. To prevent sample size attrition and maintain statistical power while strictly isolating the evaluation from temporal leakage, a 30-second calibration + 30-second temporal buffer was adopted post-hoc. This ensured that the first evaluation window strictly succeeded a temporally independent calibration segment without future-state leakage.

## S2. Extended Metric Suite (Participant-Balanced)
While Macro Subject AUROC represents the primary classification threshold-independent metric, we report the following threshold-dependent metrics aggregated at the participant-level (N=21 eligible) across the Baseline-Relative pipeline using a default 0.5 decision threshold:

- **Participant-Balanced Accuracy**: 0.6697
- **Sensitivity (Stress Recall)**: 0.6609
- **Specificity (Baseline Recall)**: 0.6786
- **Matthew's Correlation Coefficient (MCC)**: 0.3295
- **Brier Score**: 0.2475

## S3. Detailed Protocol V1 vs V2 Breakdown
The target dataset employs two protocol sequences:
- **Protocol V1**: Rest $\rightarrow$ Stroop $\rightarrow$ TMCT (N=18). Macro AUROC = 0.7634 [95% CI: 0.6153, 0.8837].
- **Protocol V2**: Rest $\rightarrow$ Subtract (N=17, Eligible=3). Macro AUROC = 0.8864 [95% CI: 0.6761, 1.0000].
The higher variance in V2 is attributable to the extreme class imbalance (only 4 valid baseline windows remained across the entire cohort).

## S4. Subject-Level Feature Attribution Jaccard Indices
While global SHAP Spearman $\rho$ achieved 0.9847, the Top-10 global feature rank Jaccard index was exactly 1.000. For the most influential features (Top-5), the Jaccard index was 0.6667. This indicates that while the absolute top-ranked features exhibit some domain sensitivity, the broader Top-10 discriminative physiological representations (primarily EDA statistical moments) are highly stable across the WESAD and Hongn domains.

## S5. Deployment Latency Benchmarks
Simulated on an Intel/AMD CPU architecture, the average latency per 60-second observation window:
- **Feature Extraction (39 features)**: ~4.5 ms
- **XGBoost Inference**: ~0.8 ms
- **Total Pipeline Latency**: ~7.2 ms
The pipeline achieves near real-time feasibility for continuous wearable deployment.
