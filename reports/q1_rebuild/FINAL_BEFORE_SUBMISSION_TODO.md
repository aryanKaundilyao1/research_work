# FINAL BEFORE SUBMISSION TODO

==================================================
## A. MUST DO BEFORE FACULTY RESUBMISSION
==================================================

1. **Format High-Resolution Figures**
   - **WHAT**: Generate publication-ready `.pdf` or `.png` (300dpi) plots from the results CSVs (ROC-AUC curves, SHAP summary plots, Domain shift heatmaps).
   - **WHY**: Visual evidence is strictly required for the committee to assess effect sizes and validation robustness.
   - **EXACT STEPS**: 
     1. Run `python code/generate_figures.py` (needs to be written).
     2. Verify axis limits and legends.
     3. Insert into `FINAL_MANUSCRIPT_REBUILD_V2.md`.
   - **EXPECTED TIME**: 2 hours.
   - **FILES AFFECTED**: `figures/`, `FINAL_MANUSCRIPT_REBUILD_V2.md`

2. **Run Protocol V1 vs V2 Stratified Analysis**
   - **WHAT**: Compare transfer metrics between Target Dataset V1 (Stroop first) and V2 (Subtract first).
   - **WHY**: Protocol mismatch is listed as a major domain shift factor. Validating if V1 or V2 transferred better will strengthen the argument.
   - **EXACT STEPS**: 
     1. Parse participant IDs (`S` vs `f`).
     2. Group true/predicted probabilities.
     3. Calculate ROC-AUC per group.
   - **EXPECTED TIME**: 1 hour.
   - **FILES AFFECTED**: `reports/q1_rebuild/PROTOCOL_STRATIFIED.csv`

==================================================
## B. MUST DO BEFORE JOURNAL SUBMISSION
==================================================

1. **Complete Literature Integration**
   - Expand `FINAL_LITERATURE_MATRIX.csv` to 35-50 references. Add in-text citations.
2. **Format Supplementary Material**
   - Package all `reports/q1_rebuild/` audits into a single PDF appendix.
3. **Reproducibility Package**
   - Clean the `code/` directory, add a strict `requirements.txt`, and document the execution order.

==================================================
## C. STRONGLY RECOMMENDED FOR Q1
==================================================

1. **Second External Target Dataset**
   - **Scientific Benefit**: Proves that the subject-specific baseline referencing isn't overfitted to the Hongn et al. dataset. Highly expected for top-tier wearable generalized ML papers.
   - **Implementation Difficulty**: Medium-High. Requires harmonizing a new dataset (e.g., SWELL-KW), processing windows, and running the pipeline.
   - **Estimated Work**: 2-3 days.
   - **Can manuscript proceed without it?**: Yes, but the chance of major revision or rejection from Q1 is higher.

==================================================
## D. OPTIONAL
==================================================

1. **Deep Learning Baseline (1D-CNN or Transformer)**
   - Train an end-to-end model to show if representation learning overcomes the ACC domain shift better than handcrafted features.
2. **Additional Classifiers**
   - Add LightGBM or CatBoost. (Optional since XGBoost is already well-validated).
