# Phase 3: Subject-Level Bootstrap Audit

- **Number of Iterations:** 5000
- **Resampling Strategy:** Subject-level with replacement (N=34)

## 95% Confidence Intervals

| Metric            |   Observed |   CI_Lower |   CI_Upper |
|:------------------|-----------:|-----------:|-----------:|
| ROC-AUC           |   1        |   1        |          1 |
| Balanced Accuracy |   0.970588 |   0.926471 |          1 |
| Sensitivity       |   0.941176 |   0.852941 |          1 |
| Specificity       |   1        |   1        |          1 |

## Degeneracy Analysis

In 4985 out of 5000 iterations, the bootstrap yielded a perfect 1.000 AUC or was undefined (single class sampled). This occurs because the margin of separation for the observed data is so large that resampling almost always constructs a perfectly separable set. The confidence interval for ROC-AUC is practically degenerate (e.g., [1.0, 1.0] or very close to it), indicating that the observed perfect separation is highly robust to subject-level variance within this cohort.