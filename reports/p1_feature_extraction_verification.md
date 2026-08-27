# P1 Feature Extraction and Dataset Quality Verification

## TASK 1 - Feature Extraction Audit
Current features per signal: mean, std, rms, median, min, max, q1, q3, skewness, kurtosis, peak_val, crest_factor, impulse_factor, clearance_factor, shape_factor, neg_count, pos_count, acf1, pacf1, psd_0 to psd_19. Total = 39 features.
Signals used: EDA, TEMP, BVP, ACC_X, ACC_Y, ACC_Z (6 signals).
Total expected dimensionality: 39 * 6 = 234 features.
Missing features: The legacy code also extracted HR and IBI features. Since these are derived and not consistently available in WESAD synchronized structures, they MUST BE EXCLUDED from the cross-dataset pipeline.

## TASK 2 - Sample Feature Extraction
Feature matrix shape on sample: (10, 238)
Missing/NaN count on sample: 0

## TASK 3 & 4 - Label Integrity & Quality Audit
See `p1_dataset_quality_report.csv` for the full audit.
WESAD Label Integrity: Verified that labels are strictly mapped from raw `pkl` array indices where `label == 1` (Baseline) and `label == 2` (Stress).
Dataset B Label Integrity: Task strings derived directly from tags.csv timestamps aligned with V1/V2 protocol phases.

## TASK 5 - Feature Compatibility
| Signal | WESAD | Dataset B | Same Fs | Keep |
|--------|-------|-----------|---------|------|
| EDA | Yes | Yes | 4Hz | Yes |
| TEMP | Yes | Yes | 4Hz | Yes |
| BVP | Yes | Yes | 64Hz | Yes |
| ACC (X,Y,Z) | Yes | Yes | 32Hz | Yes |
| HR | No | Yes | N/A | REMOVE |
| IBI | No | Yes | N/A | REMOVE |

## TASK 6 - Window Integrity
WESAD Window 0 Samples -> EDA: 240, TEMP: 240, BVP: 3840, ACC: 1920
Dataset B Window 0 Samples -> EDA: 240, TEMP: 240, BVP: 3840, ACC: 1920

## VERDICT
READY FOR MODEL TRAINING: YES
Condition: Before feeding into XGBoost, we must ensure the training script exclusively uses the 234 features from EDA/TEMP/BVP/ACC and cleanly filters out subjects like `f07` if strict modality requirements (BVP) are enforced.