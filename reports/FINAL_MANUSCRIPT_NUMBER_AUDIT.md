# Final Manuscript Number Audit

This document tracks every quantitative statement made in the final manuscript back to the audited source evidence.

| Manuscript Number | Source File / Report | Verified? | Exact Location / Context |
| :--- | :--- | :--- | :--- |
| **WESAD $N=15$** | `data_loaders.py` | Yes | Iteration over `S*.pkl` files |
| **Dataset B $N=31$** | `hardening_bootstrap.py` | Yes | N=34 original minus S02, f14, f07 masks |
| **Internal AUC 0.964** | `final_statistical_table.md` | Yes | Exp 1 (Internal LOSO) |
| **External Absolute AUC 0.423** | `final_statistical_table.md` | Yes | Exp 3 (Absolute + ACC) |
| **Cohen's $d \approx -1.47$** | `experiment3_diagnostic_audit.md` | Yes | ACC Z mean shift |
| **External Ablated AUC 0.540** | `final_statistical_table.md` | Yes | Exp 4 (Absolute - ACC). Table lists 0.54 |
| **External Relative AUC 1.000** | `final_statistical_table.md` | Yes | Exp 5 (Relative - ACC) |
| **SHAP Spearman $\rho=0.9527$** | `final_shap_audit.md` | Yes | Cross-dataset attribution correlation |
| **SHAP Jaccard 1.000** | `final_shap_audit.md` | Yes | Top-20 feature overlap |
