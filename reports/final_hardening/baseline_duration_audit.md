# Phase 5: Baseline Duration Sensitivity Audit

| Duration   |   ROC-AUC |   PR-AUC |   Balanced Accuracy |   Sensitivity |   Specificity |
|:-----------|----------:|---------:|--------------------:|--------------:|--------------:|
| 30s        |  0.842561 | 0.874745 |            0.735294 |      0.676471 |      0.794118 |
| 60s        |  0.894464 | 0.93074  |            0.838235 |      0.676471 |      1        |
| 120s       |  0.883218 | 0.929409 |            0.794118 |      0.588235 |      1        |
| 180s       |  0.885813 | 0.926688 |            0.794118 |      0.588235 |      1        |
| 300s       |  0.901384 | 0.933811 |            0.794118 |      0.588235 |      1        |
| Full       |  1        | 1        |            0.970588 |      0.941176 |      1        |

**Analysis**: Evaluates if the transfer success is robust to extremely short calibration periods.