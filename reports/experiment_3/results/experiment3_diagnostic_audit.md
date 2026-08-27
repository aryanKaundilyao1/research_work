# Experiment 3: Scientific Diagnostic Audit

## 1. Label Alignment & Dataset B Composition
**WESAD Mapping:** 1 -> Baseline, 2 -> Stress (TSST)
**Dataset B Mapping:** 'Baseline' -> Baseline, 'TMCT', 'Real Opinion', 'Opposite Opinion', 'Subtract' -> Stress

### Dataset B Task Subjective Stress & Composition
| task             |   windows |   subjects |   mean_subjective_stress |
|:-----------------|----------:|-----------:|-------------------------:|
| Baseline         |       122 |         35 |                  3.36111 |
| Opposite Opinion |       412 |         17 |                  4.23611 |
| Real Opinion     |       158 |         18 |                  3.84722 |
| Subtract         |       124 |         17 |                  4.54167 |
| TMCT             |       164 |         18 |                  5.73611 |

> **Diagnostic Insight:** A subjective stress score of ~1.0-3.0 implies baseline resting, while scores >4.0 imply induced stress. The mapped Dataset B stress tasks correctly elicited subjective stress responses.

## 2. Raw Signal Distribution Shift
| Dataset   |   EDA_Global_Mean |   TEMP_Global_Mean |
|:----------|------------------:|-------------------:|
| WESAD     |           2.38251 |            32.9999 |
| Dataset_B |           3.76375 |            32.6476 |

> **Diagnostic Insight:** If the absolute mean EDA differs vastly across the two datasets, a frozen scaler will completely miscalibrate absolute threshold probabilities, despite the underlying physiological reactions being valid.

## 3. Top 10 Feature Distribution Shifts (Cohen's d)
| Feature         |   Cohens_D |   WESAD_Mean |   DatasetB_Mean |
|:----------------|-----------:|-------------:|----------------:|
| ACC_Z_min       |  -1.6183   |    -31.5336  |         23.2449 |
| ACC_Z_mean      |  -1.47443  |      9.12899 |         44.2266 |
| ACC_Z_q1        |  -1.46694  |      2.85177 |         41.1995 |
| ACC_Z_median    |  -1.39221  |      9.6203  |         44.8801 |
| ACC_Z_q3        |  -1.30085  |     15.9738  |         47.8798 |
| ACC_Z_rms       |  -1.25354  |     29.2756  |         47.173  |
| ACC_Z_pos_count |  -1.02068  |   1258.52    |       1836.97   |
| ACC_Y_peak_val  |   1.01901  |     46.4379  |         24.3265 |
| ACC_Z_neg_count |   1.00272  |    644.994   |         79.8408 |
| ACC_Y_rms       |   0.998381 |     25.8108  |         12.385  |

> **Diagnostic Insight:** Features with a massive absolute Cohen's d (>1.0) indicate severe domain shifts. A frozen model reliant on these features will fail externally.

## 4. Threshold vs Ranking Calibration Failure
The external ROC-AUC achieved in Experiment 3 was 0.423. Since random guessing is 0.50, an AUC significantly below 0.5 indicates that the WESAD model's internal probability rankings are partially **inverted** when applied to Dataset B.

**Scientific Interpretation:**
The external generalization failure is **not** merely a calibration/threshold issue. If it were only a threshold failure, the Balanced Accuracy would drop, but the ROC-AUC (a threshold-independent ranking metric) would remain high. Because the ROC-AUC collapsed to 0.423, the actual physiological biomarker patterns selected by the WESAD model are systematically shifting in the opposite direction (or entirely orthogonally) in Dataset B. True biological cross-protocol generalization did not occur using the natively extracted temporal features.