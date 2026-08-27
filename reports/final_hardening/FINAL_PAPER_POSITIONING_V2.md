# Final Paper Positioning (V2)

## Central Narrative
The paper is positioned primarily as a **diagnostic and methodological investigation into cross-dataset generalization**, rather than simply presenting a "novel XGBoost stress classifier."

**The Problem:** Internal validation (e.g., LOSO-CV) in wearable stress detection often overestimates real-world performance because models overfit to dataset-specific absolute physiological limits and laboratory-specific movement protocols.
**The Intervention:** We explicitly separate internal from external evaluation (WESAD to Dataset B). We isolate the failure to modality-specific domain shift (Accelerometer) and inter-subject physiological variation.
**The Solution:** We demonstrate that zero-shot stress-label transfer (using *only* unlabeled target-domain baseline data for calibration) substantially recovers generalization when applied to a baseline-relative physiological representation, yielding highly stable feature attributions.

## Core Research Question
*"To what extent can subject-specific baseline-relative physiological representations improve zero-shot cross-dataset generalization of wearable stress detection, and what role does modality-specific domain shift play in external failure?"*

## What This Paper Is NOT About
- It is **not** about claiming an ROC-AUC of 1.000 means "universal stress detection is solved." The 1.000 is an empirical result within a finite cohort ($N=31$) under controlled laboratory conditions with large effect sizes.
- It is **not** about proposing a novel machine learning architecture. We use a standard XGBoost model and standard SelectKBest feature selection to ensure the focus remains on the *data representation*.
- It is **not** a clinical diagnostic paper. We claim "model-attributed representation," not "causal biological biomarkers."

## Contribution Structure
1. **Strict Evaluation Framework:** Highlighting the collapse from 0.964 (internal) to 0.423 (external) using a mathematically frozen absolute pipeline.
2. **Modality Domain Shift:** Demonstrating via Cohen's d that ACC captures experimental physical protocols, actively harming physiological transfer.
3. **Representation Recovery:** Demonstrating that Z-score baseline-relative normalization of strictly physiological features recovers a strictly positive probability margin in the external cohort.
4. **Interpretability Agreement:** Using cross-dataset SHAP ($\rho=0.9527$) to prove the recovery is due to the model relying on the exact same physiological logic in the target dataset as it did in the source.
