# Phase 7: Modality Robustness Audit

| Modality     |   ROC-AUC |   Balanced Accuracy |
|:-------------|----------:|--------------------:|
| EDA          |  0.965398 |            0.823529 |
| BVP          |  0.608131 |            0.529412 |
| TEMP         |  0.983564 |            0.926471 |
| EDA+BVP      |  0.962803 |            0.779412 |
| EDA+TEMP     |  1        |            0.970588 |
| BVP+TEMP     |  0.969723 |            0.941176 |
| EDA+BVP+TEMP |  1        |            0.970588 |

**Analysis**: Determines which modalities drive the successful transfer when subject-specific baselining is applied.