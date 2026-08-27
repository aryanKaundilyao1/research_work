# Final Experiment Plan

## EXPERIMENT 1: Internal WESAD Validation (LOSO-CV)
**Objective:** Establish whether wrist-based multimodal physiological features can classify Baseline vs Stress internally within a single cohort.
- **Inputs:** WESAD 60-second sliding windows (EDA, TEMP, BVP, ACC).
- **Labels:** 0 (Baseline), 1 (Stress).
- **CV:** Leave-One-Subject-Out (15 folds).
- **Pipeline (per fold):**
  1. `StandardScaler` (fit on Train, transform Test).
  2. `SelectKBest(f_classif, k=20)` (fit on Train, transform Test).
  3. `SMOTE` (apply to Train only).
  4. `XGBoost(max_depth=3, n_estimators=50, reg_alpha=1.0)`
- **Metrics:** Subject-aggregated ROC-AUC, PR-AUC, F1, Balanced Accuracy.
- **Statistical Tests:** Wilcoxon signed-rank test comparing subject-average predicted probability of Stress during true Baseline windows vs true Stress windows.
- **Expected Outputs:** Internal validation performance table.
- **Plots:** ROC Curve (with shaded CV variance), Confusion Matrix.

## EXPERIMENT 2: Ablation Study
**Objective:** Determine the minimal sensor combination required for robust stress detection.
- **Design:** Repeat Experiment 1 using strictly constrained feature subsets:
  - EDA only
  - BVP only
  - TEMP only
  - ACC only
  - EDA + BVP
- **Expected Outputs:** Table comparing ROC-AUC across modalities.
- **Statistical Tests:** Linear Mixed-Effects Model (LMM) testing whether adding modalities significantly improves subject-level AUC over EDA alone.

## EXPERIMENT 3: Cross-Dataset External Generalization
**Objective:** Test whether the WESAD-trained biomarkers generalize to a distinct cohort undergoing different stress tasks (Dataset B).
- **Inputs:** 
  - WESAD: All subjects (Training).
  - Dataset B: All usable subjects (Testing). Exclude `f07`.
- **Pipeline:**
  1. Fit `StandardScaler` -> `SelectKBest(k=20)` -> `SMOTE` -> `XGBoost` on **100% of WESAD**.
  2. Freeze pipeline.
  3. Pass Dataset B windows through frozen pipeline to generate predicted stress probabilities.
- **Metrics:** External ROC-AUC, PR-AUC, F1. (Using Dataset B Baseline vs All Stress Tasks).
- **Expected Outputs:** Cross-dataset performance metrics.
- **Plots:** External ROC Curve.

## EXPERIMENT 4: Task-Specific Stress Response Analysis
**Objective:** Analyze how the model responds to specific acute stressors in Dataset B (e.g., TMCT vs Real Opinion vs Subtract).
- **Inputs:** Dataset B external predictions from Exp 3.
- **Statistical Tests:** Kruskal-Wallis H-test on subject-aggregated predicted stress probabilities across tasks, followed by Dunn's post-hoc tests.
- **Expected Outputs:** Identification of which tasks elicited the strongest biomarker response.
- **Plots:** Boxplot of predicted stress probabilities across Dataset B tasks.

## EXPERIMENT 5: Temporal Decay Comparison
**Objective:** Compare temporal stress decay in WESAD against task progression in Dataset B.
- **Inputs:** 
  - WESAD Stress windows (split into Early, Middle, Late chronologically per subject).
  - Dataset B Task windows.
- **Analysis:** Plot the temporal trajectory of predicted stress probability. Does WESAD adaptation (Early > Late) mirror Dataset B task severity variations?
- **Plots:** Line plots showing temporal progression of stress probability.

## EXPERIMENT 6: SHAP Biomarker Interpretation
**Objective:** Identify the physiological drivers of the cross-dataset model.
- **Inputs:** The final frozen XGBoost model from Exp 3.
- **Analysis:** Calculate SHAP values on the WESAD training set and Dataset B test set independently.
- **Expected Outputs:** Ranking of the most important physiological features.
- **Plots:** SHAP Summary Beeswarm plot, showing directionality (e.g., higher EDA mean -> higher stress probability).
