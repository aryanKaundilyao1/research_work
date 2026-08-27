# Gaps Remaining Before Submission

This checklist details the final administrative and technical steps required before the manuscript can be submitted to the target venue (e.g., IEEE JBHI, ACM IMWUT).

## 1. Administrative Gaps
- [ ] **Author Details:** Insert the final list of authors, exact institutional affiliations, and contact emails.
- [ ] **Ethics Statement:** Add a statement confirming that data collection for both WESAD and Dataset B was approved by the respective Institutional Review Boards (IRB) and that participants provided informed consent.
- [ ] **Dataset Access Statement:** Provide details on how reviewers/readers can access WESAD (publicly available) and Dataset B (state if it is publicly available, available upon request, or proprietary).
- [ ] **Code Availability:** Add a statement regarding the open-source release of the evaluation pipeline and baseline-normalization scripts (e.g., a GitHub repository link).
- [ ] **Dataset B Citation:** Replace the `[VERIFY FROM SOURCE]` placeholder with the actual citation for Dataset B.

## 2. Technical and Formatting Gaps
- [ ] **Figure Generation:** The actual high-resolution vector images (e.g., EPS or PDF format) for Figure 1 (Block Diagram), Figure 2 (Bar Chart), and Figure 6 (SHAP Scatter) need to be compiled. Current project files contain PNGs for Figures 4 and 5, which may need to be re-exported at 300+ DPI for publication.
- [ ] **Template Compliance:** The current `manuscript_draft.tex` uses standard IEEEtran. Ensure this exactly matches the specific conference/journal template requirements (e.g., double-blind formatting if the venue requires anonymous submission).
- [ ] **Supplementary Material Compilation:** Combine the supplementary tables and secondary robustness plots (e.g., permutation null distribution, baseline duration plot) into a single `Supplementary_Material.pdf` document.

## 3. Metric Verification (Final Pass)
- [ ] Confirm the exact demographic breakdowns (e.g., age, gender ratios) for both datasets in Table I.
- [ ] Verify if F1 score, Sensitivity, and Specificity can/should be calculated retroactively for Experiment 3 and 4, or if leaving them as "NR" (Not Reported) is acceptable to the target journal.
