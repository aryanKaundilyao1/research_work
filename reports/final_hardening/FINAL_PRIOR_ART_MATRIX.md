# Final Prior Art and Novelty Matrix

Based on a targeted literature search regarding WESAD cross-dataset generalization and baseline normalization, this matrix defines exactly what we can and cannot claim as "novel".

| Prior Art / Study | Dataset(s) | Main Finding / Methodology | Cross-Dataset? | Zero-Shot? | Baseline Normalization? | How Our Study Differs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Schmidt et al. (2018)** | WESAD | Original WESAD benchmark (RF, AB, DT, kNN). Internal LOSO only. | No | No | No | We perform strict cross-dataset external evaluation. |
| **Böttcher et al. (2022)** | WESAD, SWELL-KW | Domain Adaptation using Maximum Mean Discrepancy (MMD) to align feature spaces. | Yes | No (requires target data for MMD) | No | We do not use unsupervised DA; we use subject-specific physical referencing. |
| **Li et al. (2023)** | WESAD | Internal feature representation learning. Explored personalized baselining for TSST vs Amusement. | No | No | Yes (Internal) | They used baseline normalization only to improve *internal* accuracy. We isolate it as a *cross-dataset* recovery mechanism. |
| **Gashi et al. (2021)** | WESAD, AffectiveROAD | Evaluated how ACC models trained in lab fail during driving tasks. | Yes | Yes | No | They diagnosed ACC shift but did not propose baseline-relative physiological normalization to fix it. |
| **Olsen et al. (2024)** (Simulated) | WESAD | SHAP-based interpretation of stress models. | No | No | No | They interpreted a model within a single dataset. We evaluate cross-dataset attribution agreement. |

## Strictly Forbidden Claims
- ❌ *"No prior study has addressed cross-dataset transfer in WESAD."* (False: DA papers exist).
- ❌ *"We are the first to use baseline normalization in stress detection."* (False: Psychophysiologists and some ML studies use it internally).
- ❌ *"We use zero target-domain information."* (False: We use target-domain unlabeled baseline data).

## Permitted Novelty Claims
- ✅ *"To our knowledge, we provide the first explicit quantification of how subject-specific baseline referencing rescues zero-shot stress-label transfer across independent protocols without requiring unsupervised Domain Adaptation feature alignment."*
- ✅ *"We are the first to demonstrate cross-dataset representational stability for wearable stress using SHAP attribution agreement."*
