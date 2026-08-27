# P0 Data Loader and Windowing Verification Report

## WESAD Verification
- **Subjects Loaded:** 15 (Expected 15)

### WESAD Subject Breakdown
- **S10:** Baseline: 19.67m, Stress: 12.08m, Windows (60s, 30s step): 61
- **S11:** Baseline: 19.67m, Stress: 11.33m, Windows (60s, 30s step): 59
- **S13:** Baseline: 19.67m, Stress: 11.07m, Windows (60s, 30s step): 59
- **S14:** Baseline: 19.67m, Stress: 11.25m, Windows (60s, 30s step): 59
- **S15:** Baseline: 19.58m, Stress: 11.43m, Windows (60s, 30s step): 59
- **S16:** Baseline: 19.67m, Stress: 11.22m, Windows (60s, 30s step): 59
- **S17:** Baseline: 19.68m, Stress: 12.05m, Windows (60s, 30s step): 61
- **S2:** Baseline: 19.07m, Stress: 10.25m, Windows (60s, 30s step): 56
- **S3:** Baseline: 19.00m, Stress: 10.67m, Windows (60s, 30s step): 57
- **S4:** Baseline: 19.30m, Stress: 10.58m, Windows (60s, 30s step): 57
- **S5:** Baseline: 19.97m, Stress: 10.75m, Windows (60s, 30s step): 58
- **S6:** Baseline: 19.67m, Stress: 10.83m, Windows (60s, 30s step): 58
- **S7:** Baseline: 19.77m, Stress: 10.67m, Windows (60s, 30s step): 58
- **S8:** Baseline: 19.48m, Stress: 11.17m, Windows (60s, 30s step): 58
- **S9:** Baseline: 19.67m, Stress: 10.75m, Windows (60s, 30s step): 58

- **Total 60s windows:** 877
- **Signal Sampling Rates:** {'EDA': 4, 'TEMP': 4, 'BVP': 64, 'ACC': 32}
- **Missing values in WESAD EDA windows:** 0

## Dataset B Verification
- **Subjects Loaded:** 36 (V1: 18, V2: 18)
- **Tasks Discovered:** Stroop, Real Opinion, Baseline, Opposite Opinion, Subtract, First Rest, TMCT, Second Rest

### Dataset B Subject Breakdown (Sample)
- **S01:** Baseline: 4.12m, Stroop: 2.92m, First Rest: 1.75m, TMCT: 7.33m, Second Rest: 2.08m, Real Opinion: 5.12m, Opposite Opinion: 0.47m, Subtract: 0.63m | Windows: 38
- **S02:** Baseline: 3.20m, Stroop: 1.43m, First Rest: 1.93m, TMCT: 4.15m, Second Rest: 2.12m, Real Opinion: 5.92m, Opposite Opinion: 0.58m, Subtract: 0.47m | Windows: 28
- **S03:** Baseline: 3.12m, Stroop: 1.45m, First Rest: 1.73m, TMCT: 4.27m, Second Rest: 2.13m, Real Opinion: 4.92m, Opposite Opinion: 0.57m, Subtract: 0.32m | Windows: 26
- **S04:** Baseline: 3.00m, Stroop: 2.63m, First Rest: 1.60m, TMCT: 6.23m, Second Rest: 2.28m, Real Opinion: 5.73m, Opposite Opinion: 0.53m, Subtract: 0.85m | Windows: 35
- **S05:** Baseline: 3.05m, Stroop: 1.65m, First Rest: 1.87m, TMCT: 5.60m, Second Rest: 2.82m, Real Opinion: 3.78m, Opposite Opinion: 0.57m, Subtract: 1.02m | Windows: 30

- **Total 60s windows:** 1654
- **Signal Sampling Rates:** {'EDA': 4.0, 'TEMP': 4.0, 'BVP': 64.0, 'ACC': 32.0}
- **Constrained Subjects loaded:** ['f07', 'S02']

## Structural Consistency Check
- **All 2531 windows have subject_id, dataset, task, fs, and EDA:** PASS