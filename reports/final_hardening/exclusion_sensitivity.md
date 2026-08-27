# Phase 10: Exclusion Sensitivity Audit

| Cohort                          |   N Subjects |   ROC-AUC |   Balanced Accuracy |
|:--------------------------------|-------------:|----------:|--------------------:|
| Primary (Exclude S02, f07, f14) |           34 |         1 |            0.970588 |
| Include S02 (Exclude f07, f14)  |           35 |         1 |            0.971429 |
| Include f14 (Exclude S02, f07)  |           34 |         1 |            0.970588 |
| Include S02 & f14 (Exclude f07) |           35 |         1 |            0.971429 |
| Include All (No Exclusions)     |           36 |         1 |            0.972222 |

**Analysis**: Demonstrates the impact of including anomalous subjects (S02) or subjects with hardware failures (f07, f14) on the final reported metrics.