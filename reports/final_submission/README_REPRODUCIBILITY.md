# Reproducibility Guide: Cross-Dataset Wearable Stress Detection

## 1. Environment Setup
To reproduce the canonical results of this study, install the required dependencies:
```bash
pip install -r requirements.txt
```

## 2. Dataset Preparation
1. Download **WESAD** (Source Domain) and place the `WESAD/` directory inside `data/source/`.
2. Download **Hongn et al. Wearable Stress Dataset** (Target Domain) and place it inside `data/target/`.

## 3. Executing the Final Reproducibility Pipeline
The entire experimental closure is encapsulated in a single reproducibility script that strictly enforces chronological dataset evaluation and baseline calibration parameters (30s calibration + 30s buffer).

Run the pipeline:
```bash
python3 code/run_final_reproducibility_pipeline.py
```

### Outputs Generated:
1. `OUTPUT_DIR/SUBJECT_CLASS_SUPPORT.csv`: Target cohort evaluation structure.
2. Console readout of 95% Bootstrap Confidence Intervals (N=5000) for AUROC and Delta AUROC.
3. SHAP attribution stability metrics ($\rho$, $\tau$, Jaccard).

## 4. Re-generating Figures
To recreate the high-resolution vector figures used in the manuscript from the canonical result registry:
```bash
python3 code/generate_final_figures.py
```
Outputs will be saved as PDFs/PNGs in `figures/final_submission/`.

## 5. Random Seeds & Hardware
All operations utilizing pseudo-random number generators (e.g., XGBoost, Bootstrap sampling, SMOTE) are strictly anchored to `random_seed=42`. Results were verified on local CPU computation; XGBoost execution times represent $< 5$ms inference latency per window.
