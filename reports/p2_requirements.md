# P2 Model Training Requirements (Engineering Checklist)

## Data Preparation
- [ ] Ensure `data_loaders.py` and `windowing.py` outputs are passed to the P2 training script natively.
- [ ] Write a `build_feature_matrix(dataset_segments)` function that orchestrates the `extract_features` function purely for EDA, TEMP, BVP, ACC_X, ACC_Y, and ACC_Z.
- [ ] Hard-code the exclusion of Subject `f07` (Dataset B) in the dataset loading phase for full-modality models.

## Training Architecture (WESAD Internal)
- [ ] Create a `run_nested_cv(X, y, groups)` function that takes the feature matrix, labels, and subject IDs.
- [ ] Instantiate `LeaveOneGroupOut()` with groups mapped strictly to `subject_id`.
- [ ] INSIDE THE FOLD LOOP:
  - [ ] Fit `StandardScaler()` on `X_train`. Transform `X_train` and `X_test`.
  - [ ] Fit `SelectKBest(f_classif, k=20)` on the scaled `X_train`. Transform `X_train` and `X_test`.
  - [ ] Fit `SMOTE(random_state=42)` on the selected `X_train`.
  - [ ] Train `XGBClassifier(random_state=42)` on the balanced, selected, and scaled `X_train`.
  - [ ] Generate `.predict_proba()` on `X_test`.

## Evaluation Architecture
- [ ] Write an `aggregate_subject_predictions(y_true, y_prob, groups)` function.
- [ ] Compute ROC-AUC and PR-AUC using the subject-aggregated probabilities, NOT the raw window probabilities.
- [ ] Write statistical functions to compute 95% Confidence Intervals for all metrics.

## Cross-Dataset Pipeline Construction
- [ ] Write `train_final_model(X_wesad, y_wesad)` that applies Scaler -> Selector -> SMOTE -> XGBoost to 100% of WESAD data.
- [ ] Save the fitted Scaler, fitted Selector, and trained XGBoost objects.
- [ ] Write `predict_external(model_bundle, X_dataset_b)` that transforms Dataset B identically and generates predictions.

## Ablation Management
- [ ] Parameterize the `build_feature_matrix` function to accept `modalities=['EDA', 'BVP']` to easily support Experiment 2 without code duplication.

## Model Interpretation
- [ ] Integrate the `shap` library to calculate feature importances exclusively on the models trained in `train_final_model`.

## Code Cleanliness
- [ ] Entirely delete `multimodalai.py` or move it to a `/legacy` folder. The P2 implementation must be written from scratch in `train_p2.py` utilizing the P0 modules to ensure zero accidental contamination from the PhysioNet code.
