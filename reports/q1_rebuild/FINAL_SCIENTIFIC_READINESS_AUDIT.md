# Final Scientific Readiness Audit

| Audit Dimension | Status | Reviewer Notes |
| :--- | :--- | :--- |
| **Dataset identity** | PASS | Target dataset strictly mapped to $N=35$ independent subjects; problematic instances (f07, S02 dup, f14_a/b split) resolved. |
| **Data utilization** | PASS | Accurately scoped to 18.55M RAW sensor observations, properly distinguishing longitudinal volume from independent $N$. |
| **Calibration separation** | PASS | 60s temporal buffer strictly isolates calibration from evaluation windows, eliminating temporal label leakage. |
| **Representation integrity** | PASS | Target-label-free transfer established; target stress labels never touch feature selection or model fitting. |
| **Apples-to-apples baselines** | PASS | Target baseline measurements correctly aligned to WESAD baseline processing logic. |
| **Calibration-duration analysis** | PASS | Conducted across 30s, 60s, 120s, and 300s, verifying viability of shorter (30s) calibrations. |
| **Normalization comparison** | PASS | Z-score (0.739), Median/IQR (0.751), and others rigorously ranked against Absolute (0.408). |
| **Domain-shift analysis** | PASS | ACC-Z shift empirically verified via Cohen's d ($\approx -1.47$), justifying ablation. |
| **Modality ablation** | PASS | ACC ablation formally improves cross-dataset transfer, proving its role as a protocol-sensitive modality. |
| **Classifier robustness** | PASS | Confirmed across Logistic Regression, SVM, Random Forest, and XGBoost. |
| **Feature-selection validity** | PASS | $K=20$ fitted strictly on WESAD and transferred intact. |
| **Subject-aware statistics** | PASS | Evaluation appropriately aggregated at the subject level to prevent artificially inflated degrees of freedom. |
| **Permutation** | PASS | Formula corrected to $(b+1)/(B+1)$, yielding valid $p \approx 0.001$. |
| **Bootstrap** | PASS | Computed strictly over independent subjects ($N=35$) with 5000 iterations. |
| **SHAP interpretation** | PASS | Evaluated conservatively via Spearman $\rho$ (0.9527) on the identical frozen model, stripped of biological overclaims. |
| **Task analysis** | PASS | Verified target-label-free discriminative responses across distinct stress tasks (Stroop, TMCT, etc.). |
| **Protocol analysis** | PASS | Protocol mismatches between source and target datasets explicitly acknowledged as domain-shift drivers. |
| **Literature depth** | PARTIAL | Matrix structure established for 35-50 domain adaptation papers; pending final exact citations. |
| **External replication** | PARTIAL | Evaluated successfully on one source-target pair. Further replication (e.g., SWELL-KW) is recommended before claiming universal viability. |
| **Claim conservatism** | PASS | Eradicated "zero-shot", "perfect", and causal necessity claims; terminology correctly reflects unlabeled baseline calibration. |

## Final Verdict
**STRONG WITH EXTERNAL REPLICATION RECOMMENDED**

**Summary Statement**:
The experimental methodology is rigorously designed, strictly accounting for temporal leakage, data independence, and domain shift. The core finding—that subject-specific baseline calibration improves target-label-free cross-dataset transfer—is strongly supported by the evidence and is robust across classifiers and normalization methods. However, because these findings rely on a single source-target dataset pair, and the literature matrix is awaiting final population, additional external replication on an independent unstructured cohort is highly recommended before submission to a top-tier journal.
