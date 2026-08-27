# Final Scientific Pipeline Audit

## A. DATA LOADING
- **WESAD Loader:** Implemented in `data_loaders.py`. Correctly extracts synchronized 700Hz label arrays and dynamically slices the multi-frequency raw E4 signals (EDA=4Hz, TEMP=4Hz, BVP=64Hz, ACC=32Hz) exclusively for Label 1 (Baseline) and Label 2 (Stress). No arbitrary sub-phase labels are invented.
- **Dataset B Loader:** Parses `tags.csv` to reconstruct timestamp-bounded tasks aligned with the V1/V2 protocol.
- **Verdict:** Solid. Signal synchronization is strictly maintained without dangerous resampling.

## B. WINDOWING
- **Mechanics:** 60-second fixed duration, 30-second sliding step.
- **Boundaries:** The `sliding_window` generator enforces strict boundaries. Windows are generated independently per condition block (e.g., inside WESAD Stress), preventing any single window from overlapping two conditions.
- **Padding:** No padding is used. If a phase has <60s of data, the window is skipped.
- **Leakage:** Because the generator runs entirely within a single subject and condition, no window crosses subject boundaries, making LOSO-CV inherently safe from overlap-induced leakage.

## C. FEATURES
- **Manifest:** 39 mathematical features extracted per signal array (Statistical, Shape, Time-Series, Spectral). Evaluated on 6 channels (EDA, TEMP, BVP, ACC_X, ACC_Y, ACC_Z), yielding **234 features**.
- **Equivalence:** The feature space is mathematically identical for both datasets.
- **Leakage:** No feature incorporates absolute timestamps, subject IDs, or explicit labels.
- **Derived Signals:** HR and IBI have been permanently excluded from this pipeline because they cannot be reliably derived cross-dataset without proprietary Empatica software.

## D. PREPROCESSING
- **Current Defect (Legacy Code):** In the original `multimodalai.py` script, `preprocess_signal()` applied standardization (`z-score`) *before* windowing and *before* CV splitting.
- **Methodological Fix for P2:** Standardization (e.g., `StandardScaler`) **must** be moved inside the CV fold. The scaler must be `.fit(X_train)` and `.transform(X_test)`.
- **Baseline Normalization:** If global baseline normalization is desired (e.g., subtracting a subject's resting EDA), it must only subtract the mean of the *Baseline* condition, rather than the global mean of the recording, to prevent the stress response magnitude from damping the baseline features.

## E. FEATURE SELECTION
- **Current Method:** `SelectKBest(f_classif, k)`.
- **Nesting:** Must be rigidly nested inside the CV fold (`.fit(X_train)`, `.transform(X_test)`).
- **Global Selection:** Any prior logic utilizing SHAP or ANOVA on the entire dataset to pre-select features is scientifically invalid and will be removed.

## F. CLASS BALANCING (SMOTE)
- **Mechanics:** SMOTE will be applied **only** to `X_train, y_train` within each LOSO fold.
- **Risk Assessment:** SMOTE on 50% overlapping windows introduces highly collinear synthetic samples. While this does inflate the *effective* sample size for the XGBoost tree-building process, it is scientifically permissible because the *validation* set (the held-out subject) is completely untouched and contains strictly real, unaltered windows. It will not artificially inflate the final evaluation metrics.

## G. CROSS-VALIDATION
- **Strategy:** Leave-One-Subject-Out (LOSO) CV on WESAD.
- **Independence:** Windows from the same subject will never be split between train and test.

## H. CROSS-DATASET VALIDATION
- **Design:** Train final pipeline (Scaler -> Feature Selection -> SMOTE -> XGBoost) on **100% of WESAD**.
- **Execution:** Save the frozen pipeline objects. Load Dataset B. Apply the frozen Scaler, frozen Feature Selector, and frozen XGBoost.
- **Integrity:** Absolutely zero Dataset B information will be used to tune hyperparameters, determine the optimal K for feature selection, or fit the scaler. 

## I. MODEL
- **XGBoost:** Hyperparameters (e.g., `max_depth=3`, `n_estimators=50`) must be fixed or tuned exclusively via a nested CV loop on WESAD.
- **Baseline Model:** A Logistic Regression (L1-regularized) baseline should be included to prove whether the non-linear complexity of XGBoost is actually beneficial.

## J. EVALUATION
- **Metrics:** ROC-AUC, PR-AUC, F1, Balanced Accuracy.
- **Subject-Level Uncertainty:** Because overlapping windows violate independence assumptions, calculating p-values on window-level predictions is invalid. We will aggregate predictions to the **subject-level** (e.g., subject-average probability of stress) before computing confidence intervals or conducting statistical tests.

## K. ABLATION
- Evaluated systematically: 1) EDA only, 2) BVP only, 3) TEMP only, 4) ACC only, 5) EDA+BVP, 6) All combined.

## L. TEMPORAL ANALYSIS
- **WESAD:** Because WESAD labels are a monolithic "Stress" block (~10 mins), we will split the chronologically ordered stress windows for each subject into Early (0-33%), Middle (33-66%), and Late (66-100%).
- **Dataset B:** Task boundaries are explicitly provided (TMCT, Real Opinion, Subtract).
- **Comparison:** We will analyze whether the temporal decay of stress in WESAD (Early vs Late) mirrors the task-specific stress magnitudes in Dataset B (e.g., TMCT vs Subtract).

## M. SHAP
- Calculated exclusively on the final models. Used strictly for post-hoc interpretation (e.g., identifying whether EDA mean or BVP spectral power drove the model). It will not be used to iteratively refine the feature set.

## N. STATISTICAL ANALYSIS
- Avoid raw window-level t-tests.
- Use **Linear Mixed-Effects Models (LMM)** with `subject_id` as a random effect, or aggregate predictions to the subject level and use non-parametric paired tests (e.g., Wilcoxon signed-rank) to compare Baseline vs Stress probabilities.

## O. DATA QUALITY & EXCLUSIONS
- **f07 (Dataset B):** PRIMARY ANALYSIS EXCLUSION. Documented hardware failure for BVP/TEMP. Cannot be evaluated by a multimodal model requiring these signals.
- **f14 (Dataset B):** SENSITIVITY-ANALYSIS CANDIDATE. Documented Bluetooth loss. We will include it, but flag it for robustness checks.
- **S02 (Dataset B):** SENSITIVITY-ANALYSIS CANDIDATE. Documented duplicated signals. Included in primary, but requires ablation check.

## P. FEATURE COUNT
- 234 features for 15 WESAD subjects (approx. 877 windows) is dangerously close to the `p > n` regime (where n = independent subjects). This poses an extreme risk of overfitting.
- **Recommendation:** Implement aggressive regularization. Use `SelectKBest` with a strict `k` (e.g., K=15 or K=20) inside the fold, and enforce L1 regularization (`alpha`) in XGBoost.

## Q. RESEARCH QUESTION ALIGNMENT
Everything now strictly serves the primary research question: generalizability across independent cohorts. All legacy PhysioNet code has been isolated.
