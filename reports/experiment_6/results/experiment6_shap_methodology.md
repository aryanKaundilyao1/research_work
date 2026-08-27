# Experiment 6 Reproducibility Checklist

- Exactly 117 features: False
- EDA/BVP/TEMP only: True (ACC excluded)
- Normalization unchanged: True (Subject-specific baseline applied)
- Frozen XGBoost model: True
- Dataset B never fitted: True
- No threshold tuning: True
- No new feature selection: True
- Same Dataset B exclusions: True (f07, f14, S02 excluded)