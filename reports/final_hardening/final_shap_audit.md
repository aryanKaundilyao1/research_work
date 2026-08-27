# Phase 12: Final SHAP Audit

## 1. Feature Attribution Ranking Agreement
- **Spearman Correlation (ρ):** 0.9527
- **Pearson Correlation (r):** 0.9182

## 2. Top-N Overlap & Jaccard Similarity
| Metric | Overlap | Jaccard Score |
|--------|---------|---------------|
| Top-5 | 4/5 | 0.6667 |
| Top-10 | 8/10 | 0.6667 |
| Top-20 | 20/20 | 1.0000 |

## 3. Modality-Level Attribution Proportions
| Modality | WESAD (Internal) | Dataset B (External) |
|----------|------------------|----------------------|
| EDA | 55.8% | 39.3% |
| BVP | 5.9% | 6.7% |
| TEMP | 38.3% | 54.0% |

## Interpretation
The high Spearman correlation and Jaccard similarity indicate that the model relies on the same **predictive feature representation** across both datasets. We explicitly do NOT claim these are causal biomarkers, but rather stable model-attributed features that successfully transfer under relative normalization.