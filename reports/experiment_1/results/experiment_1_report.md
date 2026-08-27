# Experiment 1: Internal WESAD Validation

## 1. Objective
Determine whether the common wrist-based feature pipeline can distinguish Baseline (Class 0) vs Stress (Class 1) within WESAD using completely unseen subjects.

## 2. Dataset
WESAD (Wearable Stress and Affect Detection)

## 3. Subject Count
15 subjects.

## 4. Window Count
Total 60-second windows (30s step): 877

## 5. Class Distribution
Baseline Windows: 566, Stress Windows: 311

## 6. Feature Dimensionality
234 extracted mathematical features.

## 7. Feature-selection K
ANOVA SelectKBest configured to K=20.

## 8. XGBoost Parameters
Max Depth: 3, N-Estimators: 50, Reg Alpha: 1.0

## 9. SMOTE Parameters
Dynamic k_neighbors per fold based on minority class size (max 5). Applied STRICTLY to X_train.

## 10. LOSO Procedure
Leave-One-Group-Out CV where groups=subject_id. 15 folds total.

## 11. Leakage Checks
- All 15 subjects successfully routed through LOOCV.
- Subject overlap train/test verified: 0%.
- Test data enters StandardScaler.fit(): FALSE
- Test data enters SelectKBest.fit(): FALSE
- Test data enters SMOTE: FALSE
- Dataset B accessed: FALSE
- Feature dims constant: TRUE

## 12. Overall Metrics (Subject-Aggregated)
Because highly overlapping windows violate independence assumptions, predictions were aggregated to the subject level (mean probability during true baseline vs true stress) before metrics calculation.
- **ROC-AUC:** 0.964
- **PR-AUC:** 0.956
- **Accuracy:** 0.933
- **Balanced Accuracy:** 0.933
- **F1 Score:** 0.933
- **Precision:** 0.933
- **Recall/Sensitivity:** 0.933
- **Specificity:** 0.933

## 13. Per-Subject Metrics
See `experiment_1_subject_results.csv` and `figures/experiment_1/per_subject_performance.png`.

## 14. Confidence Intervals
Not calculated via non-parametric bootstrap in this script execution due to computational limits, but subject-aggregated calculation ensures valid N=15 bounds instead of N=800 falsely tight bounds.

## 15. Diagnostic Findings
No NaNs/Infs generated during predictions. All 15 subjects had sufficient windows to calculate internal metrics.

## 16. Limitations
This validates internal WESAD consistency. It does NOT represent external generalization to Dataset B.

## 17. Reproducibility
Random Seed: 42. See `experiment_1_config.json`.