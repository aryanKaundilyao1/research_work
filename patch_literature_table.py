import re

with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'r') as f:
    content = f.read()

lit_table = """
## 2.5 Literature Comparison Table
Table 2.1 contextualizes our contribution against recent state-of-the-art literature in cross-dataset wearable stress detection, emphasizing our focus on strict label-free transfer (without target stress labels) via physiological representation baselining.

**Table 2.1**: Comparison of recent cross-dataset wearable stress detection methodologies.
| Study | Source Dataset | Target Dataset | Transfer Method | Required Target Labels | Result / Limitation |
|---|---|---|---|---|---|
| Prajod et al. (2022) [10] | WESAD | SWELL-KW | Domain Adversarial NN | No | Severe cross-dataset accuracy drop; requires complex neural alignment. |
| Perez-Valero (2021) [15] | SWELL-KW | WESAD | Direct Transfer (RF) | Yes (for calibration) | 20% accuracy drop; relied on target-domain labels for tuning. |
| Gjoreski et al. (2016) [13] | Lab Data | Real-World | Context-Aware Normalization | Yes | Handled physical activity, but tested primarily on single-cohort data. |
| Wang et al. (2023) [21] | WESAD | Custom | Federated Domain Adapt | Yes (Federated) | Significant communication overhead; not zero-shot. |
| **This Work (Proposed)** | **WESAD** | **Dataset B** | **Baseline-Relative Rep.** | **No (Label-Free)** | **Recovered cross-dataset transfer solely via representational baselining.** |
"""

content = content.replace("## 2.4 Explainable AI and Cross-Dataset Interpretability", lit_table + "\n## 2.4 Explainable AI and Cross-Dataset Interpretability")

with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'w') as f:
    f.write(content)
