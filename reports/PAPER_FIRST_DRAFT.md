TITLE:
Subject-Specific Baseline Referencing Improves Zero-Shot Cross-Dataset Generalization of Wearable Physiological Stress Detection

AUTHORS:
[To be inserted]

AFFILIATIONS:
[To be inserted, e.g., Vellore Institute of Technology]

ABSTRACT:
**Background:** Machine learning models for physiological stress detection often demonstrate strong predictive performance during within-dataset evaluation. However, internal validation can substantially overestimate model generalizability, as models may overfit to cohort-specific absolute physiological levels or experimental artifacts. 
**Methods:** To systematically evaluate cross-dataset generalizability, a Light Gradient Boosting Machine (XGBoost) model was trained exclusively on the WESAD cohort and evaluated strictly zero-shot on an independent cohort (Dataset B, $N=31$). We contrasted an absolute multimodal representation against a subject-specific baseline-relative physiological representation (excluding accelerometer features) using a frozen evaluation pipeline. 
**Results:** Internal WESAD evaluation yielded strong performance (ROC-AUC = 0.964). However, cross-dataset transfer utilizing the absolute multimodal representation failed severely (ROC-AUC = 0.423). Diagnostic analysis identified massive domain shift driven by accelerometer (ACC) features. Ablating ACC marginally improved transfer (ROC-AUC = 0.539). Conversely, implementing a subject-specific baseline-relative physiological representation completely rescued separability in the evaluated cohort (ROC-AUC = 1.000, Balanced Accuracy = 0.970). Cross-dataset SHAP (SHapley Additive exPlanations) attribution analysis revealed highly conserved feature reliance (Spearman $\rho = 0.9527$, Top-20 Jaccard = 1.000). 
**Conclusion:** Accelerometer-induced domain shifts and absolute physiological variations severely degrade cross-dataset transfer. Subject-specific baseline referencing provides strong evidence of improved zero-shot generalizability by shifting the model focus from absolute values to relative physiological deviations, yielding a highly stable model-attributed physiological representation across the evaluated laboratory protocols.

KEYWORDS:
Wearable Sensors, Affective Computing, Domain Shift, Zero-Shot Generalization, Baseline Normalization.

---

# 1. INTRODUCTION

Psychological stress is a major contributor to adverse health outcomes, and the advent of wearable sensors offers a non-invasive methodology for continuous, objective stress monitoring. Wearable devices typically record multimodal signals—including Electrodermal Activity (EDA), Blood Volume Pulse (BVP), Skin Temperature (TEMP), and physical movement via Accelerometers (ACC)—which capture the autonomic nervous system's response to acute stressors.

Machine learning models trained on these physiological features frequently report excellent classification accuracies. However, human physiology is highly variable. Absolute baseline physiological measurements vary significantly across individuals due to intrinsic factors (e.g., genetics, basal metabolic rate) and extrinsic factors (e.g., ambient temperature, sensor placement). Consequently, a model trained on a specific cohort under a specific laboratory protocol often learns dataset-specific absolute physiological boundaries or incidental protocol artifacts rather than a robust, generalizable stress response.

This domain-shift problem means that internal cross-validation within a single dataset is often insufficient evidence for real-world deployment. A model demonstrating near-perfect internal accuracy may fail catastrophically when applied to an independent dataset—a setting known as zero-shot cross-dataset generalization. Despite this, while many wearable stress studies demonstrate within-dataset performance, fewer explicitly test whether learned physiological representations survive a genuinely independent cohort and a different stress-induction protocol.

In this study, we ask: *To what extent does subject-specific baseline referencing improve zero-shot cross-dataset generalization of wearable physiological stress representations, and what role does modality-specific domain shift play in external failure?* We hypothesize that the inclusion of ACC features induces severe domain shift by capturing dataset-specific experimental protocols rather than physiological stress, and that transforming absolute physiological signals into subject-specific baseline-relative representations eliminates non-stationarity, substantially improving zero-shot cross-dataset transfer without requiring target-domain stress labels.

# 2. RELATED WORK

The challenge of cross-dataset generalization in affective computing is widely recognized. Recent efforts have attempted to bridge the "domain gap" between established datasets (e.g., WESAD) and external cohorts (e.g., SWELL-KW, AffectiveROAD) using Domain Adaptation (DA) techniques. These approaches typically require unsupervised feature alignment or access to small amounts of target-domain labeled data. 

In parallel, subject-specific baseline normalization is a well-established preprocessing technique in psychophysiological research used to reduce inter-subject variance during within-dataset evaluations. However, prior research has not systematically isolated baseline normalization as a distinct mechanism for rescuing *strict zero-shot* cross-dataset transfer, nor have prior studies rigorously diagnosed the specific failure modes (e.g., ACC domain shift) that necessitate such normalizations.

Our work differs significantly from prior literature utilizing the Wearable Exam Stress dataset, which primarily focused on phase-aware classification of exam-related stress outcomes within a single cohort. Instead, this study focuses explicitly on representation generalization, domain shift, and cross-dataset interpretability.

# 3. RESEARCH GAP AND CONTRIBUTIONS

To our knowledge, the combination of controlled cross-dataset failure diagnosis, accelerometer ablation, strict zero-shot subject-specific baseline normalization, and cross-dataset attribution agreement has not been systematically evaluated in the reviewed literature. 

Our specific contributions are:
1. A strict source-to-target evaluation framework separating internal validation from true external zero-shot generalization.
2. A systematic diagnosis showing that accelerometer distribution shift can substantially degrade cross-dataset transfer.
3. An experimentally tested subject-specific baseline-relative representation for physiological signals that substantially improves zero-shot transfer.
4. Cross-dataset interpretability analysis demonstrating strong agreement in learned feature attribution structure, indicating representation stability.
5. A rigorous hardening analysis testing whether the external improvement is stable under alternative assumptions (e.g., bootstrapping, negative permutation).

# 4. MATERIALS AND METHODS

## 4.1 Study Design
This study utilizes a strict source-to-target transfer design. A classification pipeline was trained and optimized exclusively on the source domain (WESAD). The resulting frozen pipeline was subsequently applied zero-shot to the target domain (Dataset B).

## 4.2 Source Dataset: WESAD
The Wearable Stress and Affect Detection (WESAD) dataset served as the source domain. It consists of 15 subjects undergoing laboratory-induced states of Baseline, Amusement, and Stress (via the Trier Social Stress Test). 

## 4.3 External Dataset: Dataset B
An independent cohort of 34 subjects (Dataset B) served as the external target domain. The stress induction protocol in Dataset B differed substantially from WESAD, incorporating Baseline, Trier Mental Challenge Test (TMCT), Real Opinion, and Subtract tasks. 

## 4.4 Signal Modalities
Both datasets contained multimodal recordings including EDA, BVP, TEMP, and tri-axial ACC (X, Y, Z). Data were synchronized and aligned prior to feature extraction.

## 4.5 Data Quality and Exclusions
Following a hardware and signal-quality audit of Dataset B, three subjects (S02, f07, f14) were excluded due to missing or severely corrupted multimodal channels or protocol deviations, resulting in a final evaluated cohort of $N=31$ subjects.

## 4.6 Windowing
Continuous physiological signals were segmented using a 60-second sliding window with a 30-second stride. Strict condition boundaries were enforced; no overlapping window was permitted to cross subject boundaries or condition transitions (e.g., baseline to stress). 

## 4.7 Feature Extraction
A total of 39 statistical, frequency-domain, and non-linear features were extracted per sensor channel. The absolute multimodal representation (EDA, BVP, TEMP, ACC X/Y/Z) comprised 234 features. The absolute physiological representation (EDA, BVP, TEMP) comprised 117 features.

## 4.8 Absolute Representation
In the absolute representation, physiological features retained cohort-specific baseline information. A global standard scaler (zero mean, unit variance) was fit exclusively on the WESAD training data and subsequently applied to scale the Dataset B features.

## 4.9 Subject-Specific Baseline-Relative Representation
To map absolute physiological states to relative physiological deviations, we applied subject-specific baseline normalization. For subject $s$ and physiological signal $x$:
$$z_s(t) = \frac{x_s(t) - \mu_{s,baseline}}{\sigma_{s,baseline}}$$
where $\mu_{s,baseline}$ and $\sigma_{s,baseline}$ were calculated exclusively from the subject's temporally prior baseline period. Future stress periods in the target domain were never used to calculate these reference statistics.

## 4.10 Model Development
We employed a Light Gradient Boosting Machine (XGBoost) classifier. 

## 4.11 Feature Selection
Feature dimensionality was reduced using an ANOVA F-value (SelectKBest) algorithm fit exclusively on the WESAD training data.

## 4.12 Class Balancing
To address class imbalance within the training folds, Synthetic Minority Over-sampling Technique (SMOTE) was applied. SMOTE was strictly isolated to the training data.

## 4.13 Internal Cross-Validation
Internal source-domain evaluation (WESAD) was conducted using Leave-One-Subject-Out Cross-Validation (LOSO-CV) to prevent subject identity leakage.

## 4.14 External Zero-Shot Evaluation
The external evaluation utilized the pipeline fit on WESAD (including the scaler, feature selector, and XGBoost weights). Dataset B was passed through this frozen pipeline. Because overlapping windows (30-second stride on 60-second windows) are statistically correlated, window-level evaluations artificially inflate confidence intervals. Therefore, predictions were aggregated to the subject level for inferential statistical analysis. 

## 4.15 Statistical Analysis
To confirm the robustness of the external evaluation, we performed a subject-level bootstrap (5,000 iterations) to generate 95\% confidence intervals (CI). A permutation negative control (randomly shuffling subject-level labels) was conducted to ensure the observed probability separation was not a structural artifact of the evaluation pipeline.

## 4.16 SHAP Interpretation
To investigate representation stability, SHapley Additive exPlanations (SHAP) TreeExplainer values were computed independently on the WESAD validation folds and the Dataset B external data. SHAP values identify model attribution, not biological causality. Feature attribution rankings across the two datasets were compared using Spearman's rank correlation ($\rho$) and Top-20 Jaccard overlap.

# 5. EXPERIMENTAL DESIGN

We structured the evaluation into six sequential experiments to trace the etiology of cross-dataset failure and recovery:
- **Experiment 1 (Internal WESAD Validation):** Establish the baseline performance of the absolute multimodal representation within the source domain via LOSO-CV.
- **Experiment 2 (Modality Ablation):** (Reserved for secondary internal diagnostic audits).
- **Experiment 3 (Cross-Dataset Generalization):** Apply the frozen Experiment 1 pipeline zero-shot to Dataset B to quantify baseline domain shift.
- **Experiment 4 (Accelerometer Ablation):** Remove the ACC features from the absolute pipeline and re-evaluate on Dataset B to isolate ACC-induced domain shift.
- **Experiment 5 (Subject-Specific Baseline Referencing):** Apply the baseline-relative physiological representation (excluding ACC) and evaluate zero-shot transfer.
- **Experiment 6 (Cross-Dataset SHAP Analysis):** Compare the feature attribution structure of the relative model between WESAD and Dataset B.

# 6. RESULTS

## 6.1 Internal Performance (Experiment 1)
Experiment 1 established a strong within-cohort benchmark. The absolute multimodal representation evaluated via LOSO-CV on WESAD achieved an ROC-AUC of 0.964, a Balanced Accuracy of 0.933, and an F1 score of 0.933. 

## 6.2 External Generalization Failure (Experiment 3)
Despite this excellent internal performance, the frozen pipeline failed severely when evaluated zero-shot on Dataset B. The external ROC-AUC collapsed to 0.423, with a Balanced Accuracy of 0.441, indicating performance slightly worse than chance. This demonstrates that high internal validation performance does not reliably predict external generalizability.

## 6.3 Accelerometer Domain-Shift Analysis
Diagnostic analysis revealed that the distribution of ACC features differed massively between WESAD and Dataset B. For instance, the mean Z-axis acceleration exhibited a Cohen’s $d \approx -1.47$ between the cohorts. This shift reflects structural differences in the experimental protocols (e.g., physical posture requirements during the tasks) rather than physiological autonomic arousal.

## 6.4 Accelerometer Ablation (Experiment 4)
Removing ACC features from the absolute representation increased the external ROC-AUC from 0.423 to 0.539, and the Balanced Accuracy from 0.441 to 0.514. While the ablation mitigated the most severe domain-shift confounds, the absolute physiological features alone remained insufficient for effective cross-dataset transfer.

## 6.5 Baseline-Relative Transfer (Experiment 5)
Applying subject-specific baseline-relative normalization to the physiological signals (EDA, BVP, TEMP) substantially improved zero-shot transfer. The external evaluation reached an ROC-AUC of 1.000, a Balanced Accuracy of 0.970, a Sensitivity of 0.941, and a Specificity of 1.000. Under this representation, the model correctly ranked stress probabilities higher than baseline probabilities for all 31 valid subjects in the evaluated cohort.

## 6.6 Robustness and Statistical Hardening
To verify that the perfect rank-separability (AUC = 1.000) was robust to cohort sampling, a 5,000-iteration subject-level bootstrap was performed. The analysis yielded a degenerate 95\% CI of [1.000, 1.000], confirming that the probability margin was strictly positive across all subjects. A negative permutation control confirmed an empirical $p = 0.0000$, ruling out structural evaluation artifacts. Furthermore, the relative representation proved robust to baseline duration constraints; utilizing only the first 30 seconds of the baseline period yielded equivalent transfer performance.

## 6.7 SHAP Feature Agreement (Experiment 6)
Cross-dataset SHAP analysis revealed highly conserved model-attribution structures. The Spearman rank correlation of SHAP feature importance between WESAD and Dataset B was $\rho = 0.9527$. Furthermore, the Top-20 most important features identified in the source domain perfectly overlapped with those in the target domain (Jaccard = 1.000). 

# 7. DISCUSSION

## 7.1 Main Findings
Our findings provide strong evidence that while absolute representations of physiological and motion data achieve high accuracy within a specific cohort, they are highly sensitive to dataset-specific artifacts. Subject-specific baseline referencing of strictly physiological signals substantially improves zero-shot cross-dataset generalization under the evaluated protocols.

## 7.2 Why Internal Performance Did Not Predict External Performance
Machine learning models optimizing for within-dataset accuracy readily exploit absolute signal levels and incidental experimental artifacts (shortcut learning). WESAD-trained models learned the specific absolute physiological bounds and physical postures of the WESAD protocol. When applied to Dataset B, which possessed different ambient conditions and tasks, these absolute bounds collapsed.

## 7.3 Role of Accelerometer Domain Shift
Accelerometer data actively harmed cross-dataset transfer. Because physical movement is dictated by the specific laboratory protocol (e.g., typing vs. sitting still) rather than purely by psychological stress, ACC features injected massive domain-shift confounds into the representation. 

## 7.4 Role of Subject-Specific Baseline Referencing
Removing ACC was necessary but insufficient. Absolute physiological values vary naturally across individuals. By referencing signals against a subject's own pre-stress baseline, we transformed the problem space. The model evaluated relative physiological deviations rather than absolute states, mitigating the inter-cohort variance that caused the absolute pipeline to fail.

## 7.5 Physiological Interpretation
The high cross-dataset SHAP agreement ($\rho = 0.9527$) is a crucial finding. It indicates that the performance recovery in Dataset B was not due to the model finding spurious new correlations in the target data. Rather, the model relied on the *exact same* functional representation of physiological deviation across both datasets. We emphasize that SHAP identifies model attribution, not causal biology; however, this agreement provides strong evidence for the representational stability of the relative physiological features.

## 7.6 Comparison With Prior Work
Unlike prior approaches utilizing Domain Adaptation to bridge dataset gaps by utilizing target-domain labels or unsupervised alignment, our methodology requires zero target-domain information beyond the temporally prior baseline. This strict zero-shot capability is highly advantageous for real-world continuous monitoring applications where external labels are unavailable. 

## 7.7 Practical Implications
Wearable stress models intended for deployment must explicitly isolate protocol-specific artifacts (like ACC) from generalized autonomic responses. Furthermore, systems should be designed to regularly capture and update subject-specific baseline estimations to ensure models process relative deviations rather than absolute values.

## 7.8 Scientific Significance
This study highlights the critical necessity of zero-shot external evaluation in affective computing. Internal LOSO-CV, while a standard benchmark, can severely obscure domain-shift vulnerabilities.

# 8. LIMITATIONS
We report an ROC-AUC of 1.000 for Experiment 5. We must be exceptionally transparent: this perfect rank-separability does not imply that stress detection is a "permanently solved" problem. The result is a reflection of the clean probability separation within the finite 31-subject Dataset B cohort under a highly controlled laboratory protocol designed to elicit substantial physiological effect sizes. Real-world ambulatory data will exhibit much smaller margins of separation, continuous physiological confounds (e.g., exercise, thermal regulation), and less clearly defined baseline periods. Furthermore, overlapping windows, while aggregated at the subject level for statistics, represent a limitation in continuous physiological modeling. Independent replication on a third, unstructured free-living dataset is required to confirm generalizability beyond laboratory-induced stress. Finally, this study does not establish clinical validity.

# 9. CONCLUSION
The transition from internal validation to external deployment in wearable stress detection is heavily compromised by modality-specific domain shifts and absolute physiological variations. Our rigorous zero-shot evaluation demonstrates that removing accelerometer artifacts and implementing subject-specific baseline-relative normalization for physiological signals substantially improves cross-dataset transfer. The resulting representation exhibits highly consistent model-attribution structure across independent cohorts, providing a scientifically defensible pathway toward robust, generalizable affective computing models. 

# REFERENCES
[To be populated based on Reference Audit]
