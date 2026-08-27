# 5. Materials and Methods

## 5.1 Study Design and Source-to-Target Evaluation Framework
To evaluate cross-dataset domain shift and the effect of representation-level interventions, this study utilizes a strict source-to-target transfer framework. The WESAD dataset serves as the source domain, providing the training data for the physiological classifier. Dataset B serves as the independent target domain for external evaluation. The evaluation is strictly isolated: the classifier, scaler, feature selection, and class balancing steps are fitted exclusively on the source domain and then mathematically frozen. The target predictions are generated without using any target-domain stress labels for model retraining, threshold optimization, or adaptation. We explicitly define this methodology as zero-shot stress-label transfer. While target stress labels are withheld, target-subject unlabeled physiological baseline measurements are utilized solely to calibrate the baseline-relative representation. 

## 5.2 Source Dataset: WESAD
The Wearable Stress and Affect Detection (WESAD) dataset is utilized as the source cohort [CITATION NEEDED]. It contains multimodal physiological recordings from 15 subjects ($N=15$) who underwent a controlled laboratory protocol including a baseline condition, a stress condition (Trier Social Stress Test; TSST), and an amusement condition. Signals were recorded using an Empatica E4 wristband. For this study, data from the baseline and stress conditions were utilized to train the internal model.

## 5.3 Target Dataset: Dataset B
Dataset B (the Wearable Exam Stress Dataset) serves as the independent target cohort [CITATION NEEDED]. The original cohort comprised 34 participant instances recorded using Empatica E4 devices during academic examination protocols. The protocol included an initial resting baseline followed by cognitive stress tasks (e.g., Trier Mental Challenge Test, Real Opinion, Opposite Opinion, and Subtract tasks). Based on an audited signal-quality review, three subject instances (S02, f07, f14) were excluded due to severe sensor corruption (e.g., broken BVP/TEMP sensors), yielding a final evaluated target cohort of exactly 31 subjects ($N=31$).

## 5.4 Signal Modalities and Preprocessing
The physiological modalities utilized across both datasets were Electrodermal Activity (EDA), Skin Temperature (TEMP), and Blood Volume Pulse (BVP), recorded via wrist-worn sensors. Tri-axial Accelerometry (ACC) was initially included to diagnose motion-related domain shift. Signals were processed using identical temporal segmentation: continuous recordings were segmented into overlapping windows of 60 seconds duration with a 30-second step size. 

## 5.5 Feature Extraction
For each 60-second window, statistical and temporal features were extracted across the available modalities. Rather than passing all features directly to the classifier, the feature space was strictly constrained to prevent high-dimensional overfitting. ANOVA F-value feature selection (`SelectKBest`) was utilized to select the top 20 features ($K=20$). Crucially, this feature selection was fitted exclusively on the WESAD training data, ensuring the selected feature subset was optimized solely for the source domain before external transfer.

## 5.6 Absolute Physiological Representation
The absolute physiological representation models the raw magnitude of the recorded signals. To standardize this representation prior to classification, a global standard scaler (Z-score normalization) was applied. This scaler was fitted globally across the WESAD training folds to compute the source-domain mean and variance, and it was applied identically to the test data. When evaluating the absolute representation externally, the frozen WESAD-fitted scaler was applied directly to Dataset B, treating target measurements based on the source domain's absolute statistical distribution.

## 5.7 Subject-Specific Baseline-Relative Representation
To mitigate the absolute interpersonal variance and domain shift observed in the absolute representation, a subject-specific baseline-relative physiological representation was implemented. For each subject $i$ and physiological channel $c$ in the target domain, the transformation utilizes the continuous unlabeled data recorded exclusively during that subject's experimental `Baseline` task. 
The subject-specific baseline mean $\mu_{i,c}^{base}$ and standard deviation $\sigma_{i,c}^{base}$ are calculated over the baseline measurements. Subsequently, all continuous physiological signals $x_{i,c}(t)$ for that subject are transformed prior to windowing and feature extraction using:
$$ z_{i,c}(t) = \frac{x_{i,c}(t) - \mu_{i,c}^{base}}{\sigma_{i,c}^{base}} $$
If the baseline standard deviation is exactly zero (e.g., a flat sensor reading), the denominator defaults to 1.0 to prevent mathematical undefined behavior. Target stress labels do not enter any stage of this calibration; it relies entirely on the target subject's unlabeled resting physiology.

## 5.8 Accelerometer Ablation
To experimentally test whether accelerometry contributed disproportionately to cross-domain mismatch, an ACC ablation intervention was designed. The tri-axial accelerometer channels were completely removed from the feature matrix, restricting the representation exclusively to autonomic physiological indicators (EDA, BVP, TEMP). The rest of the machine learning pipeline (scaling, selection, class balancing, and classifier architecture) remained mathematically constant.

## 5.9 XGBoost Classification Pipeline
The classification engine is an Extreme Gradient Boosting (`XGBClassifier`) model [CITATION NEEDED]. The hyperparameters were fixed without reference to the target dataset: `n_estimators` = 50, `max_depth` = 3, `learning_rate` = 0.05, `subsample` = 0.8, and `reg_alpha` = 1.0. To address class imbalance during training, the Synthetic Minority Over-sampling Technique (SMOTE) was applied with $k=5$ neighbors. 

## 5.10 Internal Source-Domain Validation
To establish the internal efficacy of the representation, validation on WESAD was performed using Leave-One-Subject-Out Cross-Validation (LOSO-CV). The scaler, ANOVA feature selector, and SMOTE transformations were strictly nested inside the training fold for every iteration. Out-of-fold predictions were aggregated, yielding the internal source-domain performance.

## 5.11 External Zero-Shot Stress-Label Transfer
Following internal validation, the complete pipeline (scaler, feature selector, and trained XGBoost model) was fitted globally on 100% of the WESAD data. This final pipeline was mathematically frozen. External evaluation was then executed by passing the Dataset B representations through the frozen source pipeline. 

## 5.12 Domain-Shift Diagnostic Analysis
To quantify the modality-specific domain shift between WESAD and Dataset B, a standardized distributional difference was calculated for the accelerometer features. Specifically, Cohen's $d$ was calculated to measure the effect size of the shift in the mean Z-axis accelerometer feature between the source and target distributions. 

## 5.13 Robustness and Statistical Validation
To verify the stability of the external performance, two statistical robustness procedures were conducted based on the subject-aggregated prediction probabilities:
1. **Subject-Level Bootstrap:** A 5000-iteration bootstrap analysis was performed, resampling the 31 unique target subjects with replacement. This generated a 95% Confidence Interval (calculated via 2.5th and 97.5th percentiles) for the aggregated ROC-AUC, ensuring the result was not driven by a small subset of outlier subjects.
2. **Task-Level Permutation Negative Control:** A permutation test with 1000 iterations was executed. The aggregated true subject-level condition labels were randomly shuffled against the fixed model-predicted probabilities. The empirical p-value was calculated as the proportion of null ROC-AUCs greater than or equal to the observed ROC-AUC, verifying the model's performance against random chance.

## 5.14 Cross-Dataset SHAP Attribution Analysis
To determine whether the feature attribution structure of the model was conserved across domains, SHapley Additive exPlanations (SHAP) values [CITATION NEEDED] were extracted for both the internal WESAD evaluation and the external Dataset B evaluation. The mean absolute SHAP values were computed to generate a global feature importance ranking for both domains. The structural agreement was quantified using the Spearman rank correlation ($\rho$) across the entire feature vector and the Jaccard similarity coefficient for the Top-20 most impactful features. This analysis assesses attribution stability, not biological equivalence or causality.

## 5.15 Leakage Prevention and Experimental Isolation
Data leakage compromises physiological machine learning evaluations [CITATION NEEDED]. The pipeline strictly prevented:
- **Subject Leakage:** Internal WESAD evaluation utilized strict LOSO-CV.
- **Target-Label Leakage:** Target stress labels were categorically withheld from all stages of external transfer, including calibration.
- **Methodological Leakage:** ANOVA feature selection, global standard scaling, and SMOTE balancing were fitted exclusively on WESAD training data. Target data were never used to tune hyperparameters or optimize probability thresholds. 


# 6. Experimental Design
The study executed a sequence of 6 canonical experiments to isolate the source of domain shift and evaluate the representation-level intervention.

## 6.1 Experiment 1 — Internal Source Validation
**Objective:** Establish the baseline internal accuracy of the absolute multimodal representation.
**Input:** WESAD multimodal data (EDA, BVP, TEMP, ACC).
**Evaluation:** LOSO-CV on WESAD.

## 6.2 Experiment 2 — Domain-Shift Diagnostic
**Objective:** Quantify the distributional shift in physical protocol characteristics.
**Input:** Accelerometer features from WESAD and Dataset B.
**Evaluation:** Calculation of Cohen's $d$ between source and target cohorts.

## 6.3 Experiment 3 — External Absolute Transfer
**Objective:** Evaluate the cross-dataset generalization of the frozen internal model.
**Input:** Dataset B multimodal data evaluated via the frozen WESAD absolute pipeline.
**Evaluation:** Zero-shot stress-label transfer ROC-AUC on Dataset B.

## 6.4 Experiment 4 — Accelerometer Ablation
**Objective:** Test whether removing the protocol-sensitive motion modality improves transfer.
**Input:** Absolute physiological data (EDA, BVP, TEMP), with ACC ablated.
**Evaluation:** Zero-shot stress-label transfer ROC-AUC on Dataset B.

## 6.5 Experiment 5 — Baseline-Relative External Transfer
**Objective:** Evaluate whether a representation mitigating absolute physiological variance recovers generalization.
**Input:** Subject-specific baseline-relative physiological data (EDA, BVP, TEMP).
**Evaluation:** Zero-shot stress-label transfer ROC-AUC on Dataset B.

## 6.6 Experiment 6 — Cross-Dataset Attribution Agreement
**Objective:** Determine whether the physiological logic learned in the source domain persists in the target domain.
**Input:** The baseline-relative model predictions on WESAD and Dataset B.
**Evaluation:** SHAP Spearman correlation ($\rho$) and Top-20 Jaccard overlap.
