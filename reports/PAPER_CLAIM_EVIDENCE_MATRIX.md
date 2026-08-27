# Manuscript Claim and Evidence Matrix

| Claim in Manuscript | Supporting Experiment/Audit | Exact Metric / Evidence | Confidence / Qualification | Citation Required? |
| :--- | :--- | :--- | :--- | :--- |
| Internal validation overestimates external generalization. | Exp 1 vs. Exp 3 | Internal AUC: 0.964 vs External AUC: 0.423 | **High.** We present this as empirical observation for this specific pipeline. | Yes (Domain shift literature). |
| Accelerometer features induce severe domain shift. | Exp 4 & Phase 6 Diagnostic | ACC Z mean Cohen’s $d \approx -1.47$. | **High.** This is an empirical artifact of the physical protocol difference between WESAD and Dataset B. | No (Direct result). |
| Subject-specific baseline referencing rescues zero-shot transfer. | Exp 5 vs. Exp 4 | Relative AUC 1.000 vs. Absolute AUC 0.539. | **High**, *but strictly qualified.* We claim it "substantially improves transfer" under the evaluated protocols. | Yes (Baseline normalization literature). |
| The recovered transfer is not a structural evaluation artifact. | Phase 11 Negative Permutation Control | Empirical $p = 0.0000$ | **High.** Shuffle tests confirm the pipeline does not structurally force separation. | No (Direct result). |
| The perfect AUC is robust to subject sampling within the cohort. | Phase 3 Subject-Level Bootstrap | 95% CI: [1.000, 1.000] | **High**, *but qualified.* We state the perfect separation is real *within the finite Dataset B cohort*, not that it proves universal perfection. | No (Direct result). |
| The model utilizes the exact same physiological representation across both cohorts. | Exp 6 Cross-Dataset SHAP | Spearman $\rho = 0.9527$, Top-20 Jaccard = 1.000 | **High.** | Yes (SHAP methodology). |
| Baseline duration does not require extensive clinical resting periods. | Phase 5 Baseline Duration Sensitivity | Stable transfer at 30s baseline. | **Moderate.** Qualified by stating "for this specific model and protocol." | No (Direct result). |
