# Phase 8: Simple Model Robustness Audit

| Condition                |   ROC-AUC |   Balanced Accuracy |
|:-------------------------|----------:|--------------------:|
| Internal WESAD (LR)      |  0.933333 |            0.933333 |
| External Dataset B (LR)  |  0.905709 |            0.808824 |
| External Dataset B (XGB) |  1        |            0.970588 |

**Analysis**: Evaluates if the high performance is dependent on non-linear XGBoost architecture or if the baseline-relative representation is linearly separable.