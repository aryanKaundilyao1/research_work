# Experiment 2: Modality Ablation

## 1. Objective
Determine the impact of specific sensor modalities on the model's ability to discriminate Baseline vs Stress.

## 2. Experimental Constraints
- WESAD Dataset ONLY.
- Identical LOOCV architecture, parameter settings, and subject-aggregation logic from Experiment 1.
- No hyperparameter tuning or modality-specific adjustments.

## 3. Modality Comparison Table
| Condition                 | Modalities       |   ROC-AUC |   PR-AUC |   Balanced Accuracy |       F1 |   Sensitivity |   Specificity |
|:--------------------------|:-----------------|----------:|---------:|--------------------:|---------:|--------------:|--------------:|
| A. EDA only               | EDA              |  0.906667 | 0.938423 |            0.833333 | 0.83871  |      0.866667 |      0.8      |
| B. BVP only               | BVP              |  0.964444 | 0.962317 |            0.866667 | 0.866667 |      0.866667 |      0.866667 |
| C. EDA + BVP              | EDA+BVP          |  0.915556 | 0.919322 |            0.9      | 0.896552 |      0.866667 |      0.933333 |
| D. EDA + BVP + TEMP       | EDA+BVP+TEMP     |  0.915556 | 0.925988 |            0.9      | 0.896552 |      0.866667 |      0.933333 |
| E. EDA + BVP + TEMP + ACC | EDA+BVP+TEMP+ACC |  0.964444 | 0.955809 |            0.933333 | 0.933333 |      0.933333 |      0.933333 |

## 4. Scientific Interpretation
The highest performing modality combinations reveal whether multimodal fusion genuinely improves the model's robustness or if the classification is predominantly driven by a single highly-sensitive signal (e.g., EDA).
See `figures/experiment_2/` for visual ROC, PR, and per-subject comparisons.