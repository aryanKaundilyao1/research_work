# Diagnosing Modality Shift in Cross-Dataset Stress Detection: Accelerometer Failure and Physiological Recovery via Baseline Normalization

## Abstract
**BACKGROUND:** Machine learning models for physiological stress detection often report high predictive performance during within-dataset evaluation, but their ability to transfer to independent cohorts remains poorly characterized. High within-dataset performance can create an illusion of generalizability if the models overfit to dataset-specific absolute physiological levels or experimental protocols.
**OBJECTIVE:** We tested whether a physiological representation learned from one wearable stress cohort (WESAD) could generalize strictly zero-shot to an independent, unseen cohort (Dataset B), and we sought to diagnose and mitigate the mechanisms responsible for cross-dataset transfer failure.
**METHODS:** A Light Gradient Boosting Machine (XGBoost) model was trained exclusively on the WESAD dataset and evaluated zero-shot on 31 independent subjects in Dataset B. We utilized a frozen, fully audited evaluation pipeline with overlapping window aggregation at the subject level to prevent statistical leakage. We systematically ablated accelerometer (ACC) features to diagnose domain shift and tested whether a subject-specific baseline-relative normalization applied solely to physiological signals (EDA, BVP, TEMP) could rescue generalization. Feature representations were compared across datasets using SHAP attribution agreement.
**RESULTS:** Internal within-dataset WESAD evaluation yielded a high ROC-AUC (0.964). However, cross-dataset evaluation using an absolute multimodal representation (including ACC) collapsed near chance (AUC = 0.423). Ablating ACC partially improved transfer (AUC = 0.540). By replacing absolute features with a subject-specific baseline-relative physiological representation, zero-shot transfer was substantially recovered (AUC = 1.000, Balanced Accuracy = 0.971). Furthermore, cross-dataset SHAP feature attribution demonstrated strong representational stability (Spearman $\rho = 0.9527$, Top-20 Jaccard = 1.000).
**CONCLUSION:** High internal validation performance does not guarantee cross-dataset transfer in wearable stress detection, largely due to accelerometer-induced domain shifts and variations in absolute physiological baselines. A relative physiological representation—derived via subject-specific baseline referencing—substantially improves strict zero-shot cross-dataset transfer under the evaluated laboratory protocols. While the perfect rank-separability (AUC = 1.000) reflects the large effect sizes of the specific evaluation cohort, the stable cross-dataset feature attribution provides strong evidence for the generalizability of relative physiological stress patterns.

**KEYWORDS:** Affective Computing, Stress Detection, Wearable Sensors, Domain Shift, Zero-Shot Transfer, Baseline Normalization.

---

## 1. INTRODUCTION
Wearable sensors present a non-invasive opportunity to monitor physiological stress continuously. The application of machine learning to multimodal signals—such as Electrodermal Activity (EDA), Blood Volume Pulse (BVP), and Skin Temperature (TEMP)—has yielded stress detection models with highly impressive internal classification accuracies. However, the translation of these models into real-world, general-purpose applications remains hindered by the challenge of cross-dataset generalization. 

When a model is trained on a specific cohort under a specific laboratory protocol, it often learns dataset-specific absolute physiological boundaries or incidental protocol artifacts (such as movement patterns) rather than a robust physiological stress response. Consequently, a model demonstrating near-perfect internal accuracy may collapse when evaluated on an independent cohort in a zero-shot setting (i.e., without providing target-domain labels for domain adaptation). 

In this study, we investigate the fundamental mechanisms of cross-dataset transfer failure. We explicitly ask: *Why does a physiological stress classifier trained within one wearable-sensing cohort fail to generalize to an independent cohort, and can subject-specific baseline referencing improve zero-shot cross-dataset transfer without using target-domain stress labels?* We hypothesize that (1) movement sensors (Accelerometer; ACC) capture dataset-specific experimental artifacts rather than physiological stress, inducing severe domain shift, and (2) absolute physiological values vary too widely across cohorts, whereas subject-specific baseline-relative physiological deviations provide a substantially more transferable representation.

---

## 2. RELATED WORK
The problem of domain shift in wearable stress detection is increasingly recognized. Recent efforts have utilized Domain Adaptation (DA) techniques, utilizing unsupervised feature alignment or small amounts of target-domain labels, to transfer models from established datasets like WESAD to external datasets (e.g., SWELL-KW, AffectiveROAD). 

Concurrently, subject-specific baseline normalization is a recognized preprocessing step in psychophysiology to reduce inter-subject variance within a dataset. However, its specific utility as a mechanism to rescue *strict zero-shot cross-dataset transfer*—particularly when coupled with the targeted ablation of non-physiological modalities (ACC) and validated through cross-dataset feature attribution equivalence—has not been systematically isolated.

---

## 3. RESEARCH QUESTIONS AND HYPOTHESES
Our study is guided by the following progression:
1. **Internal Success vs. External Failure:** Does strong internal performance on the WESAD cohort guarantee zero-shot transfer to an independent cohort (Dataset B)?
2. **Modality Diagnosis:** Which sensor modality contributes most to out-of-distribution (OOD) domain shift?
3. **Representation Recovery:** Does removing the shifted modality and applying a subject-specific baseline-relative transformation to the remaining physiological signals recover generalizability?
4. **Interpretability:** Does the model rely on the same underlying feature representation before and after cross-dataset transfer?

---

## 4. MATERIALS AND METHODS

### 4.1 Study Design
The study was structured to strictly separate the source domain (WESAD) from the target domain (Dataset B). A model was trained and hyperparameter-tuned exclusively on WESAD. The frozen model pipeline was then evaluated zero-shot on Dataset B.

### 4.2 Datasets
**Source Domain (WESAD):** A widely used laboratory stress dataset containing 15 subjects. Data includes Baseline, Amusement, and Stress (Trier Social Stress Test) conditions.
**Target Domain (Dataset B):** An independent cohort of 34 subjects undergoing a different stress protocol, including Baseline, TMCT, Real Opinion, and Subtract tasks. Following hardware failure audits, 31 subjects were retained for final evaluation.

### 4.3 Signal Preprocessing
Data were aggregated and synchronized. We extracted standard modalities: EDA, BVP, TEMP, and ACC (X, Y, Z). 

### 4.4 Windowing
Signals were segmented using a 60-second sliding window with a 30-second step size. To ensure strict evaluation integrity, no window was allowed to cross subject boundaries or condition (stress/baseline) boundaries.

### 4.5 Feature Extraction
The full multimodal representation comprised 39 statistical and frequency-domain features per signal, yielding 234 total features (6 channels $\times$ 39). The final physiological-only representation comprised 117 features (EDA, BVP, TEMP).

### 4.6 Absolute Normalization
In the absolute representation, a global scaler (StandardScaler) was fit exclusively on the WESAD training data and used to scale both WESAD validation and Dataset B target data.

### 4.7 Subject-Specific Baseline Normalization
We implemented a baseline-relative transformation to map absolute physiological state to relative physiological deviation. For subject $s$ and physiological signal $x$:
$$z_s(t) = \frac{x_s(t) - \mu_{s,baseline}}{\sigma_{s,baseline}}$$
where $\mu_{s,baseline}$ and $\sigma_{s,baseline}$ are the mean and standard deviation calculated exclusively from the subject's initial baseline resting period. Stress periods were never used to calculate these reference statistics. 

### 4.8 Model Development
We utilized an XGBoost classifier. Feature selection (SelectKBest ANOVA) and synthetic minority oversampling (SMOTE) were applied strictly within the training folds.

### 4.9 Internal Validation
Internal WESAD performance was evaluated using Leave-One-Subject-Out (LOSO) cross-validation to prevent identity leakage.

### 4.10 External Validation
The WESAD-trained model (and its associated feature selector and global scaler) was frozen. Dataset B was passed through this frozen pipeline. Overlapping windows in Dataset B are highly correlated; thus, to avoid inflating evaluation confidence intervals, predictions were aggregated to the subject level for inferential statistics.

### 4.11 Statistical Analysis
Bootstrapping (5,000 iterations) was conducted at the subject level. A permutation negative control (shuffling subject labels) was performed to rule out structural evaluation artifacts. 

### 4.12 SHAP Analysis
SHAP (SHapley Additive exPlanations) values were computed independently on the WESAD validation folds and Dataset B target data to evaluate cross-dataset feature attribution ranking agreement (via Spearman correlation and Jaccard similarity).

### 4.13 Leakage Prevention
To guarantee strict zero-shot evaluation:
- Dataset B labels were never used for model fitting.
- Dataset B statistics were never used for WESAD scaler/feature selection fitting.
- Hyperparameters were chosen on WESAD alone.
- Baseline normalization used only temporally prior baseline data; no future stress information was leaked.

---

## 5. RESULTS

### 5.1 Internal WESAD Performance (Study Component 1)
Under LOSO cross-validation, the model demonstrated strong internal predictive capacity, achieving an ROC-AUC of 0.964, a Balanced Accuracy of 0.933, and an F1 score of 0.933.

### 5.2 External Generalization Failure (Study Component 2)
When the frozen absolute multimodal pipeline (including ACC) was transferred zero-shot to Dataset B, performance collapsed completely. The model yielded an ROC-AUC of 0.423 and a Balanced Accuracy of 0.441, indicating near-chance target-domain performance despite the strong internal metrics.

### 5.3 Accelerometer Distribution Shift (Study Component 3)
Diagnostic audits revealed massive cross-dataset distribution shifts driven by the Accelerometer. For example, ACC Z mean showed a Cohen’s $d \approx -1.47$ between WESAD and Dataset B, reflecting structural differences in experimental physical protocols rather than physiological variations.

### 5.4 ACC Ablation (Study Component 3)
Removing the ACC modalities from the absolute pipeline marginally improved external transfer, increasing the ROC-AUC from 0.423 to 0.540. However, the representation remained insufficiently generalizable.

### 5.5 Baseline-Relative Normalization (Study Component 4)
When the absolute physiological signals (EDA, BVP, TEMP) were transformed via subject-specific baseline referencing (and ACC was removed), zero-shot cross-dataset transfer was substantially recovered. The frozen WESAD model achieved an ROC-AUC of 1.000, a Balanced Accuracy of 0.971, a Sensitivity of 0.941, and a Specificity of 1.000 on the 31 subjects of Dataset B.

Subject-level bootstrap analysis (5,000 iterations) yielded a degenerate 95% CI of [1.000, 1.000], reflecting that the probability margin (Predicted Stress > Predicted Baseline) was strictly positive for every valid subject in the evaluated cohort. 

### 5.6 Robustness Analyses
The permutation negative control yielded an empirical $p = 0.0000$, confirming the separation was not a structural artifact. Furthermore, the relative transformation was highly robust to baseline duration; utilizing only the first 30 seconds of the baseline reference period maintained equivalent transfer performance. 

### 5.7 SHAP Attribution Agreement (Study Component 5)
Cross-dataset SHAP analysis demonstrated that the relative physiological representation was highly stable. The feature attribution ranking between the internal WESAD model and the external Dataset B inference showed a highly significant Spearman rank correlation ($\rho = 0.9527$) and perfect overlap in the top 20 most important features (Jaccard = 1.000). 

---

## 6. DISCUSSION

### 6.1 Principal Findings
This study demonstrates that near-perfect internal cross-validation performance within a single wearable cohort (WESAD) is insufficient to guarantee external generalizability. However, subject-specific baseline referencing substantially improved zero-shot cross-dataset transfer under the evaluated laboratory protocols.

### 6.2 Why Internal Performance Failed Externally
Machine learning models are highly susceptible to "shortcut learning." Within WESAD, absolute signal amplitudes and movement artifacts provided sufficient information to separate stress from baseline. However, these dataset-specific absolute distributions shifted catastrophically when applied to Dataset B.

### 6.3 Role of Accelerometer Domain Shift
The accelerometer captures physical movement, which is heavily dictated by the specific experimental protocol (e.g., sitting vs. standing, talking vs. typing) rather than physiological autonomic arousal. We demonstrated that including ACC features actively harmed external transfer, acting as a domain-specific confound rather than a generalizable stress feature.

### 6.4 Importance of Subject-Specific Referencing
Absolute physiological levels (e.g., base skin temperature or tonic EDA) vary widely across populations and environments due to genetics, ambient temperature, and sensor placement. A global scaler cannot resolve these intrinsic variations. Subject-specific baseline referencing transforms the problem space: the model no longer attempts to classify whether a subject is "hot" or "cold" in an absolute sense, but rather whether their physiology is deviating significantly from their own personal resting state. 

### 6.5 Interpretation of Conserved Feature Attributions
The near-perfect SHAP agreement ($\rho = 0.9527$) is a critical result. It indicates that the model is not merely achieving high accuracy via spurious correlations in the target dataset; rather, it is relying on the *exact same model-attributed physiological features* across both domains. We explicitly do not claim these features represent universal biological causal markers. However, we provide strong evidence that the baseline-relative representation is functionally equivalent across the evaluated datasets.

### 6.6 Comparison with Previous Literature
Unlike previous efforts that rely on active Domain Adaptation (requiring target-domain data for feature alignment), our pipeline evaluates *strict zero-shot transfer*. While baseline normalization is an established technique, its systematic isolation as the primary mechanism for rescuing cross-dataset transferability—validated through modality ablation and cross-dataset SHAP equivalence—represents a robust methodological contribution to physiological machine learning.

### 6.7 Practical Implications
Future wearable stress research must explicitly isolate physiological features from protocol-induced movement artifacts (ACC). Furthermore, models intended for real-world deployment should integrate mechanisms to estimate personal baselines, as absolute physiological values are highly susceptible to environmental and population shifts.

---

## 7. LIMITATIONS
We report an ROC-AUC of 1.000 under the relative normalization condition; however, this result must be interpreted with extreme caution. Dataset B contains a finite cohort of 31 subjects undergoing highly controlled laboratory stressors (e.g., TMCT) designed to elicit large physiological effect sizes. The perfect rank-separability is a reflection of the clean probability separation within this specific evaluation cohort, rather than proof of a "perfect" or "universal" model. Real-world ambulatory data will exhibit much smaller margins of separation, numerous confounding physiological states (e.g., physical exercise, thermal regulation), and noisy baseline periods. Independent replication on a third, unstructured free-living dataset is required. Furthermore, this study does not establish clinical validity nor prove causal biomarkers.

---

## 8. CONCLUSION
The transferability of wearable stress detection models is heavily compromised by accelerometer-induced domain shifts and variations in absolute physiological baselines. We provide strong evidence that isolating physiological signals (EDA, BVP, TEMP) and applying a subject-specific baseline-relative transformation substantially restores zero-shot cross-dataset generalization. Under the evaluated protocols, this relative representation proved highly stable, maintaining consistent feature attributions across independent cohorts.

---
**SUPPLEMENTARY MATERIAL**: Available upon request, detailing baseline-duration sensitivity, bootstrap distributions, modality ablations, and full feature manifests.
