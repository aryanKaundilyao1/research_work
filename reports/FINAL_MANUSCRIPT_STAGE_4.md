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
