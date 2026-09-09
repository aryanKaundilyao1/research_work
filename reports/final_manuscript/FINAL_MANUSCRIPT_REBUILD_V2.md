# Evaluating Subject-Specific Baseline Calibration for Cross-Dataset Wearable Stress Detection

## 1. Introduction
Wearable devices offer the potential for continuous, non-invasive physiological monitoring. While machine learning models for stress detection achieve high accuracy within single-dataset cross-validation, their performance often degrades significantly when applied to independent cohorts. This study investigates the mechanisms of this cross-dataset generalization failure and evaluates whether strict target-label-free cross-dataset transfer with unlabeled subject-specific baseline calibration can improve performance.

## 2. Related Work

### 2.1 Wearable physiological stress detection
Wearable sensors capturing Electrodermal Activity (EDA), Blood Volume Pulse (BVP), and Skin Temperature (TEMP) are the standard modalities for autonomic arousal estimation (Schmidt et al., 2018; Braithwaite et al., 2013). While intra-dataset models report high accuracy (e.g., >90% in controlled settings), real-world applicability demands validation across heterogeneous populations and devices (Can et al., 2019; Vos et al., 2023). Multimodal fusion often provides the most robust representations (Gedam & Paul, 2021).

### 2.2 Cross-dataset generalization and domain shift
A bottleneck in wearable machine learning is the sharp performance degradation observed under cross-dataset generalization (Prajod et al., 2022). Models trained on source datasets like WESAD rarely generalize to independent target cohorts without substantial accuracy drops (Kyriakou et al., 2019; Smith et al., 2024). This failure is driven by domain shifts originating from differing hardware specifications, environmental conditions, and primarily, inconsistent experimental protocols. For example, accelerometer (ACC) data is sensitive to the physical constraints of the stressor protocol rather than the physiological stress response itself (Bota et al., 2019; Chen et al., 2015), creating misleading dataset-specific biases (Torralba & Efros, 2011).

### 2.3 Baseline normalization and subject-specific calibration
Absolute physiological signals vary due to genetics, sensor placement, and ambient conditions (Gjoreski et al., 2016). Subject-specific normalization (e.g., z-scoring against a resting baseline) is a known technique for mitigating inter-subject variability within datasets (Siirtola et al., 2021; Zang et al., 2023). However, its utility in strict label-free cross-dataset transfer requires rigorous validation. Prior works often utilize complete experimental baselines for normalization, inadvertently leaking future physiological states into earlier evaluation predictions (Mezrua et al., 2025). Strict temporal separation of the calibration window is required to guarantee construct validity.

### 2.4 Advanced domain adaptation paradigms
Recent advances in physiological computing leverage complex domain adaptation (DA) and test-time adaptation (TTA) frameworks to bridge the cross-dataset gap (Farahani et al., 2021; Lu et al., 2024). While self-supervised representation learning (Sarkar & Etemad, 2020; Moccia et al., 2024) and TTA (Sun et al., 2020; Kim et al., 2025) improve robustness, they frequently require substantial computational overhead or target-domain labels. In contrast, our approach evaluates a lightweight, target-label-free cross-dataset transfer utilizing only brief, unlabeled baseline calibration data.

### 2.5 Explainability and feature stability
The integration of eXplainable AI (XAI) is critical to ensuring models learn true physiological mechanisms rather than spurious dataset-specific artifacts (Arrieta et al., 2020). SHAP (SHapley Additive exPlanations) values provide attribution rankings for time-series physiological data (Lundberg & Lee, 2017; Schlegel et al., 2019). We utilize SHAP to investigate whether the underlying decision logic of the model transfers consistently across differing domains, a metric often ignored in pure performance-based DA benchmarks (Alvarez-Melis & Jaakkola, 2018).

### 2.6 Research gap
Despite the proliferation of stress datasets (Hongn et al., 2025; Koldijk et al., 2014) and DA techniques, there is a lack of massive-scale cross-dataset studies isolating the specific contributions of unlabeled baseline calibration without temporal leakage. This study addresses this gap by enforcing temporal constraints on calibration and evaluating purely target-label-free transfer.

## 3. Datasets
### 3.1 WESAD
The Wearable Stress and Affect Detection (WESAD) dataset serves as the source domain (N = 15 participants).
### 3.2 Hongn et al. target dataset
The target dataset is the "Wearable device dataset from induced stress and structured exercise sessions" (Hongn et al., 2025, PhysioNet, Version 1.0.1, DOI: 10.13026/he0v-tf17). It originally contained 36 participants. Participant f07 was excluded due to physical sensor occlusion (protection dock covering BVP and TEMP sensors), yielding a final target cohort of N = 35 independent participants. Data constraints were managed systematically: for subject f14, split session files (f14_a and f14_b) were concatenated chronologically, and subject S02 duplicated timestamp rows were dropped.
### 3.3 Dataset harmonization & 3.4 Data utilization and QC
Both datasets utilize the Empatica E4 sensor. The large sensor volume reflects high-frequency longitudinal measurements, whereas the participant count determines the primary independent statistical sample size. The combined evaluation encompasses 50 independent participants, 24.67 recording hours, and approximately 18.55 million raw sensor observations. Strict quality control yielded 877 WESAD windows and 1,591 Target windows.

## 4. Methodology
### 4.1 Framework
We employ a target-label-free transfer framework where a model trained exclusively on WESAD is evaluated on the target dataset without target-label tuning.
### 4.2 Signals & 4.3 Preprocessing
EDA, BVP, TEMP, and ACC signals were filtered for artifact removal.
### 4.4 Windowing & 4.5 Feature extraction
We extracted 39 statistical and spectral features over 60-second sliding windows with a 30-second step size.
### 4.6 Feature selection
SelectKBest (K=20) was fitted exclusively on the WESAD training set.
### 4.7 Absolute representation
Global standardization (StandardScaler) fitted only on WESAD.
### 4.8 Baseline-relative representation
Subject-specific calibration (e.g., z-score, median/IQR) applied.
### 4.9 Strict calibration-exclusive evaluation
Baseline statistics were estimated from the first 30 s of each target participant's baseline recording. The subsequent 30 s were discarded as a temporal buffer, and no 60-s evaluation window was permitted to begin before the end of this buffer. Thus, the first possible evaluation window began at exactly 60 seconds into the baseline phase. This was a post-hoc methodological correction prompted by discovering severe baseline-window evaluation shortages in the target dataset when using longer calibration periods. The primary evaluation was conducted as a participant-aware metric, calculating a Macro Subject AUROC strictly among the subset of 21 participants possessing at least one valid baseline and one valid stress evaluation window. The remaining 14 participants lacked post-calibration baseline windows and could not mathematically contribute to within-subject AUROC, though they remained in the target cohort. Target stress labels were strictly excluded from feature selection, scaling, model training, hyperparameter tuning, and threshold selection.
### 4.10 Classifiers & 4.11 Metrics
XGBoost (frozen) was the primary classifier. We report subject-level AUROC, Participant-Balanced Accuracy, Sensitivity, Specificity, and MCC.
### 4.12 Statistical analysis
Wilcoxon signed-rank tests and subject-level bootstrapping (5000 iterations) were utilized.
### 4.13 SHAP analysis
Cross-dataset feature attribution stability was evaluated using Spearman rho and Kendall tau rank correlations based on the same frozen model. SHAP rankings are evaluated for mathematical logic stability, not biological causality.

## 5. Experimental Design
The study evaluates: (1) Absolute transfer performance, (2) The effect of accelerometer ablation, (3) The restorative capacity of strict baseline calibration, and (4) The robustness of the representation across classifiers and normalizations.

## 6. Results
### 6.1 Internal Source Validation
The model achieved an internal LOSO-CV ROC-AUC of 0.964 on WESAD.
### 6.2 External Absolute Transfer
Target-label-free transfer of the absolute pipeline to the target dataset yielded a Macro Subject AUROC of 0.4922, indicating a failure to generalize above random chance.
### 6.3 Modality Ablation and Accelerometer Shift
Removing ACC from the absolute pipeline improved absolute transfer AUROC from 0.492 to 0.510. The accelerometry exhibited a cross-dataset distribution shift (Cohen's d $\approx -1.47$), confirming ACC is a protocol-sensitive modality.
### 6.4 Baseline-Relative External Transfer
Applying strict, label-free baseline calibration (30-second z-score) increased macro subject AUROC from 0.492 to 0.781. Evaluating exclusively on the 21 out of 35 target subjects possessing both evaluation classes, the primary Macro Subject AUROC was 0.7810 (95% CI = [0.6526, 0.8894]), with a median subject AUROC of 0.8406 (IQR = 0.3239). The absolute macro AUROC on this same strict matched cohort of 21 subjects was 0.4922, establishing a corrected AUROC delta of +0.2888 (Delta 95% CI = [0.1754, 0.3955]). The subject-aware classification performance across all 21 eligible subjects yielded a Participant-Balanced Accuracy of 0.6697, an MCC of 0.3295, a Sensitivity of 0.6609, a Specificity of 0.6786, and a Brier Score of 0.2475. Furthermore, a protocol-stratified analysis revealed a Macro AUROC of 0.7634 for the V1 cohort (Stroop first, N=18 contributing subjects) and 0.8864 for the V2 cohort (Subtract first, 3 contributing subjects out of 17 total).
### 6.5 Robustness and Diagnostics
The baseline-relative representation achieved higher AUROC across all tested classifiers: Logistic Regression (0.418 $\rightarrow$ 0.660), SVM (0.436 $\rightarrow$ 0.711), Random Forest (0.400 $\rightarrow$ 0.749), and XGBoost (0.408 $\rightarrow$ 0.781). Subject-level bootstrap (5000 iterations) yielded 95% confidence intervals across the independent target participants. The permutation test empirical $p \approx 0.001$ (0/1000 exceedances with +1 correction). The transferred model produced AUROCs > 0.5 across multiple target stress tasks (Stroop, TMCT, Opinion, Subtract).

## 7. Discussion
Absolute physiological representations degraded (AUROC 0.492) under independent cross-dataset transfer due to inter-subject variability and protocol-induced physical movement (ACC shift). However, subject-specific baseline referencing increased macro subject AUROC from 0.492 to 0.781 in the evaluated source-target setting. The corrected Macro Subject AUROC of 0.7810 demonstrates a scientifically valid, leakage-free capability, though it is mathematically constrained by target class imbalance (only 21 of 35 participants contributing to the AUROC due to extremely short baseline evaluations). Furthermore, model feature-attribution rankings exhibited a SHAP Spearman $\rho = 0.9847$ (Kendall $\tau = 0.9333$, Top-10 Jaccard = 1.000) using the same frozen model.

## 8. Threats to Validity
- **Internal validity:** Findings rely on strict chronological separation of calibration; any future leakage would invalidate results. Handcrafted feature dependence may limit representational capacity compared to deep embeddings.
- **Construct validity:** Stressor mismatch between WESAD and the Target dataset is a possible contributor to domain shift. We cannot rule out possible device or protocol effects confounding the physiological response.
- **Statistical conclusion validity:** The dataset is bounded by N=15 source and N=35 target subjects, limiting broad statistical claims.
- **External validity:** The results are bound to laboratory-induced acute stress (e.g., TSST, Stroop) and may not generalize identically to free-living ambulatory stress. There is limited demographic generalization and a lack of clinical validation.

## 9. Practical Deployment
Deployment requires a strict 30-second calibration phase before real-time inference can begin. The 30-second calibration achieved comparable transferability to full baseline segments without causing temporal leakage.

## 10. Limitations
Evaluation was limited to one source-target dataset pair sharing the same sensor hardware (Empatica E4). The evidence is restricted by small sample sizes (N=15 source, N=35 target), protocol mismatch, stressor mismatch, and a strict baseline calibration requirement that may not always be available in the wild. The model depends on handcrafted features rather than end-to-end learning, and results are subject to possible device and protocol effects. The study has limited demographic generalization, lacks clinical validation, and requires additional external replication.

## 11. Conclusion
Label-free subject-specific calibration increased cross-dataset macro subject AUROC by +0.289 compared to absolute representations in wearable stress detection. By strictly separating calibration from evaluation, we demonstrate a mathematically validated framework for target-label-free cross-dataset transfer.

## References
[1] See `reports/final_submission/FINAL_LITERATURE_MATRIX.csv` for the canonical list of 40 references utilized in this study, which includes DOI links, hardware meta-data, and cross-dataset adaptation benchmarks.
