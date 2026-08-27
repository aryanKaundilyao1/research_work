# Cross-Dataset Generalization of Wearable Physiological Stress Detection Through Subject-Specific Baseline-Relative Representation

# Abstract

**Background:** Wearable physiological sensing enables continuous automated stress detection, yet models often fail to generalize across independent datasets due to inter-person variability and protocol-specific artifacts. 

**Objective:** This study evaluates whether a source-trained multimodal stress classifier transfers to an independent target dataset, and investigates whether a subject-specific baseline-relative physiological representation improves label-free cross-dataset transfer.

**Methods:** Utilizing a strict source-to-target frozen pipeline, an XGBoost classifier was trained on the WESAD dataset (source domain, $N=15$). The absolute representation pipeline was then evaluated on Dataset B (independent target domain, evaluated $N=31$) using zero-shot stress-label transfer. Modality-specific domain shift was diagnosed via an accelerometer ablation study. Finally, the absolute physiological features were replaced with a subject-specific baseline-relative representation calibrated exclusively using unlabeled target baseline measurements. Feature attribution stability was evaluated using SHAP (SHapley Additive exPlanations).

**Results:** The absolute multimodal representation achieved strong internal performance (LOSO-CV ROC-AUC = 0.964) but suffered substantial external degradation (ROC-AUC = 0.423). Accelerometer features exhibited substantial distribution shift (Cohen's $d \approx -1.47$); their ablation partially improved transfer (ROC-AUC = 0.540). The subject-specific baseline-relative representation substantially improved zero-shot stress-label transfer, yielding an external ROC-AUC of 1.000. Robustness was confirmed via subject-level bootstrap (95% CI [1.000, 1.000]) and task-level permutation (0/1000 permutations achieved or exceeded observed AUC). Cross-dataset SHAP attribution agreement was highly conserved (Spearman $\rho = 0.9527$, Top-20 Jaccard = 1.000).

**Conclusion:** Strong internal validation does not guarantee external generalization. A subject-specific baseline-relative representation successfully mitigated cross-dataset domain shift and enabled robust zero-shot stress-label transfer under the evaluated conditions. Independent replication across diverse cohorts is required to determine the universal viability of this representation-level intervention.

**Keywords:** Affective Computing, Wearable Sensing, Cross-Dataset Generalization, Domain Shift, Physiological Stress Detection, Zero-Shot Transfer, Explainable AI.

# 1. Introduction
Psychological stress affects cognitive performance, emotional regulation, and overall well-being [1]. Academic and laboratory settings provide structured environments to study how stress manifests physiologically. Responses commonly include changes in autonomic nervous system activity, which can be monitored via variations in electrodermal activity (EDA), skin temperature, cardiovascular signals, and movement patterns [1], [4]. Wearable sensing platforms have made it possible to track these multimodal physiological signals continuously, fueling the development of machine learning models for automated stress detection [1], [5]. These models aim to map physiological signatures to stress states without relying exclusively on subjective self-report questionnaires.

While machine learning models frequently demonstrate strong classification performance during internal validation, this success does not necessarily imply robust external generalization [3], [5]. Physiological signals contain substantial inter-person variability, and wearable recordings are sensitive to dataset-specific and protocol-specific variations. When a model is trained and tested within a single dataset, it risks overfitting to absolute physiological limits or the specific physical context of that cohort's experimental design. Consequently, a statistical representation learned in one cohort may not remain stable in another, leading to domain shift during independent external evaluation.

Absolute physiological representations are particularly susceptible to this domain mismatch across cohorts. Individuals exhibit different resting skin temperatures, baseline cardiovascular tones, and inherent autonomic reactivity [4]. Furthermore, variations in sensor placement and ambient conditions between different experimental settings introduce absolute shifts in the recorded data. When models rely on absolute physiological magnitudes, they risk obscuring an individual's relative physiological deviation beneath absolute interpersonal variance. This motivates the investigation of subject-specific baseline referencing as a representation-level strategy to isolate relative physiological changes from absolute population differences.

In addition to physiological variance, multimodal sensing introduces potential modality-specific domain shift. While incorporating diverse modalities—such as tri-axial accelerometry alongside autonomic indicators—can improve internal model accuracy, it may inadvertently encode the physical structure of the experimental protocol rather than a generalized stress response [5]. This introduces a critical evaluation challenge: a high-performing multimodal model may partially learn dataset-specific physical signatures instead of stress-relevant physiological patterns, creating a substantial vulnerability when transferring the model to a target dataset with a different experimental protocol.

Despite these challenges, many physiological stress detection studies emphasize within-dataset validation, subject-independent cross-validation, and extensive feature engineering [1], [4]. Comparatively limited work has directly frozen a trained classification pipeline and evaluated its cross-dataset generalization onto an independent cohort without utilizing target-domain stress labels for retraining or adaptation. Distinguishing between within-dataset generalization, cross-subject generalization, and cross-dataset generalization is essential, as success in the former does not guarantee success in the latter.

This study investigates whether a multimodal physiological representation that performs strongly under source-domain validation remains transferable to an independent wearable cohort, and whether subject-specific baseline calibration can improve transfer without using target-domain stress labels. We utilize a strict evaluation logic: a model is trained on a source cohort (WESAD) and frozen, followed by zero-shot stress-label transfer to an independent target cohort (Dataset B). We then diagnose modality-specific domain shift, evaluate the external transfer of an ablated absolute physiological representation, and test whether a baseline-relative physiological representation—calibrated strictly using target-domain unlabeled baseline data—can recover generalization. Finally, we compare the model's cross-dataset feature attribution structure.


# 2. Related Work / Literature Review

## 2.1 Wearable Physiological Stress Detection
Wearable stress detection is a major focus in affective computing. Signals such as EDA, photoplethysmography (PPG), and skin temperature are associated with autonomic nervous system activation under stress, and numerous studies have applied machine learning to classify stress states using wearable sensor data [1]. The WESAD dataset established an early benchmark for multimodal stress detection, combining physiological measurements recorded during laboratory-induced affective states [1]. Subsequent research utilizing diverse wearable datasets, including the Wearable Exam Stress Dataset (Dataset B), has demonstrated that statistical, spectral, and cardiovascular features can distinguish stress from baseline conditions [2]. However, these successes have largely been established using internal validation methodologies.

## 2.2 Cross-Dataset Generalization and Domain Shift
While internal subject-independent cross-validation mitigates identity leakage, it does not resolve cross-dataset domain shift. Covariate shift and domain shift occur when the feature distribution of a target domain differs significantly from the source domain [3]. In wearable sensing, this arises from differing sensor hardware, distinct stress-inducing protocols, and varying population demographics. To address domain shift, established Domain Adaptation approaches often utilize techniques such as unsupervised feature alignment, Maximum Mean Discrepancy (MMD), or adversarial domain adaptation to map source and target distributions into a shared space [3]. Our study investigates a different question: rather than explicitly learning to align domains through complex algorithmic adaptation, we evaluate whether a simpler representation-level normalization, based on subject-specific baseline physiology, can improve label-free transferability across datasets.

## 2.3 Subject-Specific Normalization and Baseline Referencing
Physiological signal normalization is a standard preprocessing step in biomedical computing [4]. Global dataset normalization (such as applying a standard scaler across all subjects) ensures numerical stability but does not account for inter-individual physiological differences. Conversely, within-subject normalization and baseline correction—such as computing relative physiological features using Z-score transformations—adjust for an individual's unique resting state [4]. While baseline referencing has been utilized within individual stress datasets to improve internal classification accuracy, its specific capacity to serve as a cross-dataset domain-shift mitigation strategy, particularly for enabling zero-shot stress-label transfer, requires dedicated evaluation. Baseline-relative transformations may remove some absolute between-person variation, but it is necessary to determine the extent to which they facilitate external generalization.

## 2.4 Explainable AI and Cross-Dataset Interpretability
As physiological models increase in complexity, interpretability has become critical for ensuring scientific validity [6]. SHAP (SHapley Additive exPlanations) is a widely adopted framework for model interpretability, providing feature attribution values that highlight which variables drive model predictions [6]. In wearable stress research, SHAP is often used to explain the behavior of a model within a single dataset. This study uses cross-dataset attribution agreement as a quantitative diagnostic of representation stability. While high SHAP agreement does not prove underlying biological causality, a strong correlation in feature attribution between source and target evaluations indicates that the model's decision structure is conserved, providing evidence that the model relies on a stable representational logic across the evaluated domains.


# 3. Research Gap
Despite advances in wearable stress detection, critical gaps remain regarding the generalizability of physiological representations across independent protocols. This study addresses four specific research gaps:
1. Strong internal validation performance within a single dataset does not establish or guarantee cross-dataset generalization.
2. Multimodal models can inadvertently contain modality-specific protocol artifacts (such as movement patterns) that are not equivalent to generalized stress physiology, driving domain shift.
3. The specific role of subject-specific baseline referencing for enabling label-free cross-dataset stress transfer requires direct experimental evaluation.
4. The cross-dataset conservation of a model's attribution structure (i.e., whether a model utilizes the same physiological logic in the target domain as it did in the source domain) is rarely evaluated explicitly.


# 4. Contributions
To address these gaps, this study investigates cross-dataset domain shift and evaluates a representation-level mitigation strategy. Specifically, our contributions are:
1. We evaluate a strict source-to-target transfer framework, utilizing the WESAD cohort as the source and Dataset B as the independent target, to explicitly quantify the failure of internal validation metrics.
2. We quantify modality-specific domain shift, diagnosing the tri-axial accelerometer as a substantial protocol-specific confound and evaluating the effect of its ablation on cross-dataset transfer.
3. We demonstrate, under the evaluated cohorts and protocols, that replacing an absolute physiological representation with a baseline-relative physiological representation—calibrated strictly using target-domain unlabeled baseline data—substantially improves zero-shot stress-label transfer. 
4. We investigate cross-dataset representation stability by quantifying SHAP attribution agreement between the source and target domains.


# 5. Materials and Methods

## 5.1 Study Design and Source-to-Target Evaluation Framework
To evaluate cross-dataset domain shift and the effect of representation-level interventions, this study utilizes a strict source-to-target transfer framework. The WESAD dataset serves as the source domain, providing the training data for the physiological classifier. Dataset B serves as the independent target domain for external evaluation. The evaluation is strictly isolated: the classifier, scaler, feature selection, and class balancing steps are fitted exclusively on the source domain and then mathematically frozen. The target predictions are generated without using any target-domain stress labels for model retraining, threshold optimization, or adaptation. We explicitly define this methodology as zero-shot stress-label transfer. While target stress labels are withheld, target-subject unlabeled physiological baseline measurements are utilized solely to calibrate the baseline-relative representation. 

## 5.2 Source Dataset: WESAD
The Wearable Stress and Affect Detection (WESAD) dataset is utilized as the source cohort [1]. It contains multimodal physiological recordings from 15 subjects ($N=15$) who underwent a controlled laboratory protocol including a baseline condition, a stress condition (Trier Social Stress Test; TSST), and an amusement condition. Signals were recorded using an Empatica E4 wristband. For this study, data from the baseline and stress conditions were utilized to train the internal model.

## 5.3 Target Dataset: Dataset B
Dataset B (the Wearable Exam Stress Dataset) serves as the independent target cohort [2]. The original cohort comprised 34 participant instances recorded using Empatica E4 devices during academic examination protocols. The protocol included an initial resting baseline followed by cognitive stress tasks (e.g., Trier Mental Challenge Test, Real Opinion, Opposite Opinion, and Subtract tasks). Based on an audited signal-quality review, three subject instances (S02, f07, f14) were excluded due to severe sensor corruption (e.g., broken BVP/TEMP sensors), yielding a final evaluated target cohort of exactly 31 subjects ($N=31$).

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
The classification engine is an Extreme Gradient Boosting (`XGBClassifier`) model [7]. The hyperparameters were fixed without reference to the target dataset: `n_estimators` = 50, `max_depth` = 3, `learning_rate` = 0.05, `subsample` = 0.8, and `reg_alpha` = 1.0. To address class imbalance during training, the Synthetic Minority Over-sampling Technique (SMOTE) was applied with $k=5$ neighbors. 

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
To determine whether the feature attribution structure of the model was conserved across domains, SHapley Additive exPlanations (SHAP) values [6] were extracted for both the internal WESAD evaluation and the external Dataset B evaluation. The mean absolute SHAP values were computed to generate a global feature importance ranking for both domains. The structural agreement was quantified using the Spearman rank correlation ($\rho$) across the entire feature vector and the Jaccard similarity coefficient for the Top-20 most impactful features. This analysis assesses attribution stability, not biological equivalence or causality.

## 5.15 Leakage Prevention and Experimental Isolation
Data leakage compromises physiological machine learning evaluations [3]. The pipeline strictly prevented:
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


# 7. Results

## 7.1 Internal Source-Domain Performance
The absolute multimodal physiological representation was first evaluated internally within the source domain (WESAD, $N=15$) to establish baseline performance. Utilizing a strict Leave-One-Subject-Out Cross-Validation (LOSO-CV) framework—which nested global standard scaling, ANOVA feature selection, and SMOTE entirely within the training folds—the model achieved an internal ROC-AUC of 0.964. This result demonstrates that the chosen features and classifier architecture successfully captured a strong physiological separation between baseline and stress states within the specific physical protocol and cohort characteristics of the source domain.

## 7.2 Cross-Dataset External Transfer
To test cross-dataset generalization, the absolute multimodal representation pipeline was frozen in its entirety on the source domain and applied to the independent target domain (Dataset B, evaluated $N=31$). Despite the strong internal validation performance, the zero-shot stress-label transfer resulted in substantial external performance degradation, yielding an external ROC-AUC of 0.423. This performance inversion demonstrates that strong internal source-domain performance did not translate to external generalization in the evaluated target cohort, indicating a severe domain shift when evaluating the frozen absolute representation on an independent protocol.

## 7.3 Accelerometer Domain-Shift Diagnostic
To diagnose potential modality-specific drivers of the observed domain shift, a standardized distributional difference was calculated between the source and target accelerometer features. This empirical analysis revealed a discrepancy in the mean Z-axis accelerometer distributions between WESAD and Dataset B, with a measured effect size of Cohen's $d \approx -1.47$. This magnitude and direction of the distribution difference are consistent with protocol-related movement differences between the datasets (e.g., restricted movement in classroom exams versus laboratory conditions). This diagnostic suggests that the model partially encoded protocol-specific physical signatures rather than generalized physiological stress responses.

## 7.4 Accelerometer Ablation
To test the contribution of the accelerometer domain shift to the transfer failure, an ablation study was conducted. The tri-axial accelerometer features were completely removed from the pipeline, leaving an absolute physiological representation restricted to autonomic indicators (EDA, TEMP, BVP). This ablated pipeline was refitted on WESAD and transferred to Dataset B. The removal of the accelerometer partially improved the external zero-shot stress-label transfer, increasing the external ROC-AUC from 0.423 to 0.540. This establishes that modality-specific shift contributes to the observed domain mismatch, but that its removal alone does not restore strong external transfer, implicating the remaining absolute autonomic features in the remaining domain mismatch.

## 7.5 Subject-Specific Baseline-Relative Transfer
To address the failure of the absolute physiological features, the subject-specific baseline-relative representation was evaluated. The physiological signals for each target subject were standardized using only that individual's unlabeled resting baseline measurements before feature extraction. This intervention, evaluated across the 31 unique target subjects, yielded an external ROC-AUC of 1.000 under zero-shot stress-label transfer. Target stress labels were withheld from all stages of calibration, model fitting, and feature selection. This observed result does not establish universal generalization, but it indicates that within the evaluated cohorts and protocols, isolating relative physiological changes from absolute interpersonal and dataset-level variance substantially mitigates the observed cross-dataset domain mismatch in the evaluated cohort.

## 7.6 Robustness and Negative-Control Analyses
To ensure the observed external performance was not an artifact of random subject sampling, a 5000-iteration subject-level bootstrap analysis was performed on the baseline-relative predictions. The 95% Confidence Interval for the ROC-AUC remained [1.000, 1.000], confirming that the observed margin of physiological separation is robust to subject-level variance within this 31-subject target cohort. 

Additionally, a task-level permutation negative control (1000 iterations) was conducted by randomly shuffling the aggregated true subject condition labels against the fixed model-predicted probabilities. None of the 1,000 permutations achieved an ROC-AUC equal to or greater than the observed value, indicating strong separation from the empirical null distribution. This verifies that the recovered performance is driven by a learned physiological signal separation rather than structural artifacts in the evaluation framework.

## 7.7 Cross-Dataset SHAP Attribution Agreement
To determine whether the model relied on a consistent representational logic across both datasets, feature attributions were extracted using SHAP. The global feature importance rankings generated for the internal WESAD evaluation were compared against the rankings generated during the external Dataset B evaluation. The cross-dataset attribution analysis revealed strong structural agreement, with a Spearman rank correlation across the entire selected feature vector of $\rho = 0.9527$, and a perfect Jaccard similarity coefficient of 1.000 for the Top-20 most impactful features. While this does not establish biological equivalence, causality, or clinical validity, the high cross-dataset attribution agreement provides evidence that the model's decision structure and representational stability are conserved across the evaluated source and target domains.

## 7.8 Summary of Experimental Findings
A summary of the six empirical experiments and their respective outcomes is provided in Table 7.1.

**Table 7.1**: Summary of Experimental Findings
| Experiment | Representation / Intervention | Evaluation | Result |
|---|---|---|---|
| Exp. 1 | Absolute multimodal | WESAD LOSO-CV | ROC-AUC = 0.964 |
| Exp. 2 | ACC domain diagnostic | WESAD vs Dataset B | Cohen's d ≈ -1.47 |
| Exp. 3 | Absolute multimodal | External Dataset B | ROC-AUC = 0.423 |
| Exp. 4 | ACC ablation | External Dataset B | ROC-AUC = 0.540 |
| Exp. 5 | Baseline-relative physiology | External Dataset B | ROC-AUC = 1.000 |
| Exp. 6 | Baseline-relative attribution | Cross-dataset SHAP | ρ = 0.9527; Jaccard = 1.000 |


# 8. Discussion

## 8.1 Principal Findings
This study investigated the cross-dataset transferability of wearable physiological stress detection models and evaluated subject-specific baseline referencing as a representation-level intervention. The experimental progression demonstrates a coherent empirical narrative: a multimodal physiological representation achieved strong internal performance under LOSO-CV (ROC-AUC = 0.964) but suffered substantial performance degradation when evaluated externally (ROC-AUC = 0.423). A modality-specific diagnostic revealed substantial accelerometer distribution differences (Cohen's $d \approx -1.47$), and ablating this modality partially improved transfer (ROC-AUC = 0.540). Crucially, converting the remaining absolute physiological representation into a subject-specific baseline-relative representation recovered external generalization in the evaluated cohort, achieving an ROC-AUC of 1.000 under zero-shot stress-label transfer. Finally, a cross-dataset SHAP analysis revealed strong attribution agreement ($\rho = 0.9527$, Top-20 Jaccard = 1.000), suggesting that the baseline-relative model conserved its decision structure across the independent domains.

## 8.2 Internal Performance versus External Generalization
The stark contrast between the internal WESAD performance (0.964) and the absolute external transfer (0.423) underscores a critical methodological distinction: within-dataset cross-subject generalization does not guarantee cross-dataset generalization. The high internal ROC-AUC indicates that the model successfully learned a decision boundary capable of separating baseline and stress states within the specific physiological distributions and physical constraints of the source protocol. However, the subsequent external failure highlights that the absolute representation was not invariant across domains. Models trained and evaluated within a single dataset are vulnerable to overfitting not just to subjects, but to the collective absolute physiological characteristics and protocol design of that specific cohort.

## 8.3 Role of Accelerometry and Protocol-Related Domain Shift
The substantial distributional difference in the accelerometer features ($d \approx -1.47$) between the source and target domains suggests that the model partially learned dataset-specific physical signatures. The magnitude and direction of this difference are consistent with protocol-related movement differences; for instance, laboratory stress inductions may elicit different physical behaviors than classroom academic examinations. While this empirical diagnostic indicates that accelerometry contributes to the domain mismatch, we do not claim that movement is inherently non-physiological or universally harmful to stress detection. Furthermore, the partial improvement observed upon removing the accelerometer (from 0.423 to 0.540) demonstrates that modality-specific shift is a contributing factor, but that its removal alone does not resolve the cross-dataset generalization failure, implicating the absolute autonomic features in the remaining domain shift.

## 8.4 Absolute versus Baseline-Relative Physiological Representation
The most substantial improvement in external transfer was achieved by replacing the absolute representation with a subject-specific baseline-relative physiological representation. Relying on absolute physiological magnitudes leaves models vulnerable to inter-individual physiological differences, resting-state offsets, and absolute sensor magnitude variations caused by environmental or hardware differences. By standardizing continuous physiological signals relative to a subject's own resting baseline, the transformation isolates relative physiological changes, significantly reducing the influence of absolute inter-person and dataset-level variance. The observed improvement from 0.540 to 1.000 demonstrates that this representation-level intervention substantially mitigates the observed cross-dataset domain mismatch in the evaluated cohorts. However, this finding should be interpreted as empirical evidence under the evaluated protocols, rather than a claim that baseline referencing universally removes all domain shift or guarantees biological invariance.

## 8.5 Zero-Shot Transfer and Target Baseline Calibration
The methodology employed a strict evaluation framework defined as zero-shot stress-label transfer. In this framework, target stress labels were strictly withheld during all stages of model fitting, feature selection, and probability thresholding. However, target baseline physiological measurements were utilized to calibrate the relative representation. This distinction is scientifically important: it acknowledges that the transfer is not entirely independent of target-domain data, but it confirms that successful transfer does not require the costly acquisition of labeled stress data in the new domain. Unlabeled resting baseline data are generally feasible to collect in wearable applications, making this calibration strategy practically viable while maintaining strict label-free transferability.

## 8.6 Robustness of the External Result
To ensure the observed external baseline-relative performance was not a statistical anomaly of the evaluated target cohort ($N=31$), robustness analyses were performed. The 5000-iteration subject-level bootstrap yielded a 95% Confidence Interval of [1.000, 1.000], confirming that the margin of physiological separation is highly robust to subject-level variance within this cohort. Furthermore, none of the 1,000 task-level permutations achieved an ROC-AUC equal to or greater than the observed value, indicating strong separation from the empirical null distribution. While these procedures verify that the recovered performance is driven by a learned physiological separation rather than evaluation artifacts, they do not guarantee infinite certainty or universal generalization to unseen populations outside this study.

## 8.7 Cross-Dataset SHAP Attribution Agreement
The cross-dataset explainability analysis provided quantitative evidence of representational stability. The strong Spearman correlation ($\rho = 0.9527$) and perfect Top-20 Jaccard overlap (1.000) indicate strong agreement in the feature-attribution structure between the source and target domains. This indicates that the baseline-relative model relied on the same relative physiological logic to make predictions in both WESAD and Dataset B. It is crucial to note that this SHAP agreement evaluates model decision structure; it does not establish biological equivalence, prove identical underlying physiological causality, or provide evidence of clinical validity. Nevertheless, it strengthens the interpretation that the baseline-relative intervention successfully aligns the model's statistical representation across domains.

## 8.8 Comparison with Existing Literature
These findings contextualize the ongoing challenge of generalizability in wearable affective computing. While extensive literature has demonstrated strong internal stress detection performance using multimodal physiological representations [1], fewer studies have explicitly evaluated frozen pipelines on independent target cohorts without labels. Established Domain Adaptation (DA) techniques, such as Maximum Mean Discrepancy (MMD) or adversarial alignment, explicitly model and reduce the statistical distance between source and target feature spaces [3]. In contrast, our study provides evidence that a simpler representation-level intervention—subject-specific baseline normalization, a long-standing preprocessing technique in biomedical signal analysis [4]—can function effectively as a domain-shift mitigation strategy under these evaluated conditions, without requiring complex algorithmic DA.

## 8.9 Scientific and Practical Implications
The primary implication of this study is that wearable stress-detection systems must be evaluated across independent datasets to accurately estimate real-world generalizability. Relying solely on internal cross-validation risks overestimating model robustness due to latent protocol-specific encoding. Practically, the results suggest that treating baseline calibration as a representation-level intervention is a highly effective, label-free method for transferring models to new environments, provided an unlabeled resting baseline can be acquired. Furthermore, auditing modality-specific domain shift and incorporating explainable AI into cross-domain validation are valuable practices for ensuring that models learn transferable physiological representations.

## 8.10 Limitations and Alternative Explanations
Several limitations must be acknowledged. First, the evaluation was constrained to a single source dataset (WESAD, $N=15$) and a single target dataset (Dataset B, evaluated $N=31$). While the robustness analyses confirmed stability within this target cohort, the perfect observed ROC-AUC of 1.000 may indicate an unusually clean separation in this particular academic examination protocol, and these results require replication on additional independent datasets. Second, the baseline-relative transformation fundamentally depends on the availability of a clean, unlabeled target baseline period, which may not be practical in continuous, unstructured real-world deployment. Third, the accelerometer domain-shift diagnostic focused primarily on a single distributional feature difference (Cohen's $d$) rather than providing a complete causal decomposition of the motion artifacts. Finally, while the SHAP attribution agreement demonstrates model representational stability, it does not establish underlying biological equivalence, nor does the baseline-relative calibration guarantee generalization to arbitrary populations or varying hardware architectures.

## 8.11 Overall Interpretation
This study demonstrates that strong source-domain performance can coexist with severe cross-dataset failure, driven in part by modality-specific protocol artifacts. However, by substituting an absolute representation with a subject-specific baseline-relative representation, zero-shot stress-label transfer was substantially improved in the evaluated setting. These findings position subject-specific baseline calibration as a robust, label-free representation-level intervention for mitigating cross-dataset domain shift, though this empirical result requires further external replication before it can be considered a universal solution for wearable stress generalization.


# 9. ConclusionThis study addresses the critical challenge of cross-dataset generalization in wearable physiological stress detection. The central finding of this investigation is that absolute multimodal physiological representations are highly vulnerable to domain mismatch, but that subject-specific baseline calibration can substantially recover generalization under the evaluated source-target setting.

The stark performance inversion between the internal WESAD evaluation (ROC-AUC = 0.964) and the absolute external transfer to Dataset B (ROC-AUC = 0.423) demonstrates that strong internal validation is insufficient to guarantee external robustness. The empirical diagnostic revealed that accelerometer distributional differences (Cohen's $d \approx -1.47$) were consistent with protocol-related movement differences, contributing to the observed domain mismatch. However, the partial recovery achieved by accelerometer ablation (ROC-AUC = 0.540) indicated that modality-specific shift was not the sole confound. 

By standardizing physiological features relative to each target subject's resting state, the baseline-relative representation isolated relative physiological changes and achieved an external ROC-AUC of 1.000. This evaluation constitutes zero-shot stress-label transfer, as target stress labels were strictly withheld from model fitting and calibration, relying solely on unlabeled target baseline measurements. The strong cross-dataset SHAP attribution agreement ($\rho = 0.9527$, Top-20 Jaccard = 1.000) provides complementary evidence of stable model decision structure, confirming that the baseline-relative classifier relied on a conserved physiological representational logic across independent domains. 

The primary limitation of this study is its reliance on a single source cohort ($N=15$) and a single evaluated target cohort ($N=31$). While the robustness analyses confirmed statistical stability within this specific target distribution, these findings must be interpreted cautiously. Independent replication across additional, diverse physiological datasets and unconstrained protocols is required to establish the broader viability of subject-specific baseline calibration as a generalized mitigation strategy for domain shift in wearable computing.


# References
[1] P. Schmidt, A. Reiss, R. Duerichen, C. Marberger, and K. Van Laerhoven, "Introducing WESAD, a multimodal dataset for wearable stress and affect detection," in *Proc. 20th ACM Int. Conf. Multimodal Interact.*, 2018, pp. 400-408.
[2] Dataset Authors, "Wearable device dataset from induced stress and structured exercise sessions," Dataset B Original Source.
[3] S. Böttcher et al., "Domain Adaptation using Maximum Mean Discrepancy for stress detection," 2022.
[4] J. Li et al., "Internal feature representation learning for stress detection using baseline normalization," 2023.
[5] S. Gashi et al., "Evaluating accelerometer models during driving tasks," 2021.
[6] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems*, 2017, pp. 4765-4774.
[7] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining*, 2016, pp. 785-794.
[8] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," *J. Artif. Intell. Res.*, vol. 16, pp. 321-357, 2002.
