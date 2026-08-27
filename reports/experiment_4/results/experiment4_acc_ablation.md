# Experiment 4: ACC Ablation for Cross-Dataset Generalization

## 1. Objective
To test whether the massive orientation/distribution shift in the Accelerometer (ACC) channels between WESAD and Dataset B was the sole cause of the external generalization collapse in Experiment 3.

## 2. Methodology Audit Summary
The pipeline was completely restricted to EDA, BVP, and TEMP features. 
As verified by the automated methodology audit:
- The Dataset B test cohort (34 main subjects) and 60-second window structures were perfectly preserved.
- The pipeline was completely rebuilt and explicitly **frozen** on WESAD training data (Threshold = 0.5).
- Zero Dataset B data was used to fit the scaler, selector, or model.
- ACC features were completely excluded from the input matrix.

## 3. Numerical Results

| Metric              | EXP 3 (Full Modality) | EXP 4 (ACC Ablated) | Absolute $\Delta$ |
|---------------------|-----------------------|---------------------|-------------------|
| **ROC-AUC**         | 0.423                 | 0.539               | +0.116            |
| **PR-AUC**          | 0.445                 | 0.495               | +0.050            |
| **Balanced Acc**    | 0.441                 | 0.514               | +0.073            |
| **F1 Score**        | 0.136                 | 0.440               | +0.304            |
| **Sensitivity**     | 0.088                 | 0.382               | +0.294            |
| **Specificity**     | 0.794                 | 0.647               | -0.147            |

## 4. Scientific Interpretation (CASE 3)

The results strictly fall under **CASE 3: Performance improves somewhat but remains poor**.

By removing the corrupted Accelerometer signals, the model's fundamental ranking logic was successfully rescued from being entirely inverted (ROC-AUC increased from 0.423 to 0.539). The model is now capable of identifying some stressed subjects, resulting in a massive relative +334% jump in Sensitivity (from ~8.8% to 38.2%). 

However, despite resolving the inversion, the absolute performance remains barely better than random chance (Balanced Accuracy ~0.51, ROC-AUC ~0.54). 

**Conclusion:** 
The severe ACC domain shift identified during the Exp 3 diagnostic was indeed a major, destructive contributor to the external failure, as dropping it reversed the penalty. However, removing it does **not** solve the broader generalization problem. The purely physiological biomarkers (EDA, BVP, TEMP) that were highly predictive of the TSST in WESAD (Exp 1 and 2) still fail to natively generalize to Dataset B's stressors (TMCT, Opinion, Subtract) using rigid, absolute global calibration.

## 5. Recommendation for Next Experiment
Because the baseline physiology distributions (e.g. skin conductance and baseline heart rate variance) shift violently across different datasets, cohorts, and physical environments, rigid `StandardScaler` transformations fail across datasets. 

**Recommendation:** Experiment 5 should investigate **Subject-level Domain Adaptation** (e.g., using intra-subject normalization / z-scoring each subject against their own baseline rather than a global WESAD mean) to see if relative physiological changes are conserved across datasets even when absolute calibration fails.
