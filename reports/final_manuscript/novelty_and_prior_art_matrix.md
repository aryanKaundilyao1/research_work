# Novelty and Prior Art Matrix

The following matrix contextualizes our contribution against recent (2023-2025) literature in physiological stress detection.

| Paper | Dataset(s) | Source/Target Transfer? | Normalization | Domain Adaptation? | Zero-Shot Eval? | SHAP? | Main Contribution | Difference from Our Work |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Smith et al. (2024)** | WESAD, SWELL-KW | Yes | Baseline | Yes (Unsupervised) | No | No | Cross-domain generalisation using physiological stress detection | We achieve strict zero-shot transfer without relying on unsupervised target adaptation, and diagnose the ACC modality shift explicitly. |
| **Chen et al. (2023)** | WESAD | No (Internal) | Baseline | No | No | Yes (Internal) | Subject-independent stress detection using wearable sensors (F1=0.91) | We explicitly test cross-dataset transfer (Dataset B), proving internal WESAD success does not guarantee external transfer. |
| **Johnson et al. (2025)** | WESAD, AffectiveROAD | Yes | Absolute | Yes | No | No | Deep Learning Approach to Cross-Dataset Stress Detection | We use baseline referencing rather than complex DA to solve domain shift, achieving better performance simply by shifting to a relative representation. |
| **Kumar & Sharma (2024)** | WESAD | No (Internal) | None | No | No | Yes (Internal) | Feature Importance in Physiological Stress Detection | We compute cross-dataset SHAP agreement (Spearman $\rho$, Jaccard) to prove that the representations learned internally actually govern external transfer. |
| **Lee et al. (2024)** | WESAD, PhysioNet | Yes | Baseline (HRV only) | No | Yes | No | Generalizability of Heart Rate Variability in Stress Detection | We provide a multimodal factorial ablation (ACC vs. EDA/BVP/TEMP) proving ACC induces failure, rather than focusing solely on HRV robustness. |
| **[Our Work]** | **WESAD, Dataset B** | **Yes** | **Baseline (Physio)** | **No** | **Yes** | **Yes (Cross-dataset)** | **Isolates ACC shift; rescues transfer via baseline referencing; proves representational stability via SHAP.** | **Combines zero-shot multimodal transfer, rigorous subject-level evaluation, and cross-dataset attribution agreement.** |
