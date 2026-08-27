# Phase 6: Normalization × ACC Factorial Ablation

| Condition              |   ROC-AUC |   Balanced Accuracy |
|:-----------------------|----------:|--------------------:|
| Absolute + ACC (Exp 3) |  0.42301  |            0.441176 |
| Absolute - ACC (Exp 4) |  0.539792 |            0.514706 |
| Relative + ACC (NEW)   |  1        |            0.970588 |
| Relative - ACC (Exp 5) |  1        |            0.970588 |

**Analysis**: Evaluates the interaction between modality inclusion (ACC) and physiological representation (Absolute vs Relative). It determines if the presence of ACC degrades a relative model, or if relative normalization rescues the ACC model.