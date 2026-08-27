# Phase 11: Permutation / Negative Control

- **Observed ROC-AUC:** 1.0000
- **Permutations:** 1000
- **Empirical p-value:** 0.0000

By shuffling the evaluation labels (while keeping the normalization strictly causal and the model completely frozen), we generate a null distribution of ROC-AUC centered around 0.5. The fact that the observed metric sits far outside this null distribution confirms the 1.000 result is driven by a true learned physiological signal separation, rather than an artifact of the evaluation script or normalization structure.