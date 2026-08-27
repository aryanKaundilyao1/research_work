# Old vs. New Paper Difference Matrix

This matrix establishes exactly why the new manuscript is a fundamentally different and stronger scientific contribution compared to the previous paper.

| Dimension | Previous Paper | New Paper | Scientific Improvement |
| :--- | :--- | :--- | :--- |
| **Research Question** | Can temporal phase segmentation improve stress classification within an exam? | How severely do absolute representations fail across datasets, and can baseline calibration recover them? | Shifts from internal feature engineering to addressing the fundamental barrier of real-world generalization. |
| **Scientific Hypothesis** | Stress responses change dynamically from the beginning to the end of an exam. | Absolute physiological levels and movement patterns cause domain shift, which can be mitigated by subject-specific baseline referencing. | More fundamental physiological hypothesis separating protocol artifacts from actual stress. |
| **Dataset Design** | Single dataset (Dataset B). | Dual dataset (WESAD as source, Dataset B as independent target). | Enables true out-of-distribution transfer evaluation. |
| **Internal Validation** | LOSO-CV on Dataset B. | LOSO-CV on WESAD. | Establishes a strong (0.964) internal baseline before demonstrating external failure. |
| **External Validation** | None (Single dataset study). | Strict zero-shot stress-label transfer onto Dataset B. | Exposes the fragility of internal validation metrics. |
| **Domain Shift Analysis** | None. | Explicit quantification of ACC distribution shift (Cohen's $d \approx -1.47$). | Diagnoses *why* models fail externally, rather than just reporting the failure. |
| **Cross-Dataset Evaluation** | None. | Yes, strict pipeline freeze. | Proves the necessity of representation changes over model changes. |
| **Baseline Normalization** | Used standard Z-score across the whole dataset/recording internally. | Subject-specific Z-score calibrated strictly on the target subject's *unlabeled baseline* task. | Isolates relative physiological deviations from absolute interpersonal variance. |
| **Accelerometer Analysis** | Used ACC features to boost internal accuracy. | Proves ACC captures protocol-specific motion artifacts and ablates it to improve generalization. | Prevents the model from learning "what an exam looks like" instead of "what stress looks like". |
| **Ablation** | None. | ACC Ablation (Exp 3 vs Exp 4). | Isolates physiological performance from movement confounds. |
| **Statistical Hardening** | Basic permutation test. | 5000-iteration subject-level bootstrap and task-level permutation. | Proves the 1.000 AUC is stable across target subjects and strictly positive in margin. |
| **SHAP Analysis** | Interpreted internal features on a single dataset. | Correlated SHAP vectors across *two different datasets* ($\rho=0.9527$). | Proves the model uses the exact same physiological logic in the target domain as the source domain. |
| **Leakage Prevention** | Standard LOSO-CV. | Strict isolation of Scaler/SelectKBest/SMOTE on Source, explicit zero-shot on Target stress labels. | Prevents both identity leakage and target-domain label leakage. |
| **Subject-Level Inference** | Window-level and aggregated metrics mixed. | Strict subject-aggregated predictions for the final external AUC. | Prevents window-level autocorrelation from artificially inflating the final external metric. |
| **Limitations** | Acknowledged small sample size and single setting. | Aggressively acknowledges that AUC 1.000 is a finite-cohort laboratory artifact. | Demonstrates supreme scientific discipline and preempts reviewer skepticism. |
| **Novelty** | Phase-aware feature extraction. | Experimental demonstration of cross-dataset representation instability and baseline-relative recovery. | Addresses a critical roadblock in wearable affective computing. |
| **Reproducibility** | Standard methods described. | Mathematically audited metrics and explicitly frozen pipeline design. | Highly defensible claims backed by rigorous code tracing. |
