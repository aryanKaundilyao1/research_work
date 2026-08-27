# Experiment 5 Methodology Audit

## Constraint Verification
- **Identical Windowing:** TRUE (60s window, 30s step)
- **Identical Cohort:** TRUE (Excluded f07, f14, and S02)
- **Identical Threshold:** TRUE (0.5)
- **Baseline Leakage:** 0 (Baseline stats computed exclusively from task=='Baseline')
- **ACC Features Absent:** TRUE
- **No Dataset B Fitting:** TRUE (Scaler Leakage Audit Passed: True)