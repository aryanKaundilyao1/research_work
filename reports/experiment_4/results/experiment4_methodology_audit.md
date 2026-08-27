# Experiment 4 Methodology Audit

## Constraint Verification
- **Identical Windowing:** TRUE (60s window, 30s step)
- **Identical Cohort:** TRUE (Excluded f07, f14, and S02)
- **Identical Threshold:** TRUE (0.5)
- **Identical Label Mapping:** TRUE (Baseline vs TMCT/Real/Opposite/Subtract)
- **ACC Features Absent:** TRUE (Extracted only EDA, BVP, TEMP)
- **Feature Dimensions:** 117 features total.
- **No Dataset B Fitting:** TRUE (Scaler Leakage Audit Passed: True)