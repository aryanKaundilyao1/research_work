import os
import sys
import pickle
import numpy as np
import pandas as pd
import time
from datetime import datetime
import xgboost as xgb
import shap
from scipy.stats import ks_2samp, wasserstein_distance, spearmanr, kendalltau

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import WESAD_ROOT, DATASET_B_ROOT, REPORTS_DIR, OUTPUT_DIR, WINDOW_SIZE, STEP_SIZE, RANDOM_SEED
from data_loaders import load_all_wesad, load_all_dataset_b
from windowing import sliding_window
from features import build_feature_matrix
from q1_core import apply_strict_baseline_relative_transform
from q1_feature_pipeline import RigorousSourceTargetPipeline, evaluate_predictions
from q1_experiments import run_domain_shift_analysis

Q1_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'q1_rebuild')
Q1_REPORTS_DIR = os.path.join(REPORTS_DIR, 'q1_rebuild')
os.makedirs(os.path.join(Q1_OUTPUT_DIR, 'cache2'), exist_ok=True)

def get_cached_or_compute(cache_file, compute_fn):
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    print(f"Computing {cache_file}")
    data = compute_fn()
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
    return data

def run_experiment_pipeline(X_s, y_s, X_t, y_t, clf_type='xgboost', k_best=20):
    pipeline = RigorousSourceTargetPipeline(k_best=k_best, clf_type=clf_type)
    pipeline.fit_source(X_s, y_s)
    y_pred = pipeline.predict_target(X_t)
    y_prob = pipeline.predict_proba_target(X_t)
    res = evaluate_predictions(y_t, y_pred, y_prob)
    return res, pipeline, y_pred, y_prob

def extract_features_for_norm(norm_type, w_segs_raw, b_segs_raw, calib_dur=60, buffer=60):
    cache_w = os.path.join(Q1_OUTPUT_DIR, 'cache2', f'w_feats_{norm_type}_{calib_dur}.pkl')
    cache_b = os.path.join(Q1_OUTPUT_DIR, 'cache2', f'b_feats_{norm_type}_{calib_dur}.pkl')
    
    def compute_w():
        if norm_type == 'absolute':
            segs = w_segs_raw
        else:
            segs, _ = apply_strict_baseline_relative_transform(w_segs_raw, calib_dur, buffer, norm_type)
        wins = sliding_window(segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
        return build_feature_matrix(wins)
        
    def compute_b():
        if norm_type == 'absolute':
            segs = b_segs_raw
        else:
            segs, _ = apply_strict_baseline_relative_transform(b_segs_raw, calib_dur, buffer, norm_type)
        wins = sliding_window(segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
        return build_feature_matrix(wins)

    df_w = get_cached_or_compute(cache_w, compute_w)
    df_b = get_cached_or_compute(cache_b, compute_b)
    return df_w, df_b

def main():
    print("Loading raw segments...")
    w_segs_raw = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'w_segs_raw.pkl'),
        lambda: load_all_wesad(WESAD_ROOT)
    )
    b_segs_raw = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'b_segs_raw.pkl'),
        lambda: load_all_dataset_b(DATASET_B_ROOT)
    )
    b_segs_raw = [s for s in b_segs_raw if s['subject_id'] != 'f07']

    # PART B: Normalization Benchmark
    print("Part B: Normalization Benchmark")
    norms = ['absolute', 'zscore', 'mad', 'mean_center', 'minmax', 'median_iqr']
    norm_results = []
    
    for norm in norms:
        print(f"Running normalization: {norm}")
        df_w, df_b = extract_features_for_norm(norm, w_segs_raw, b_segs_raw)
        
        X_s = df_w.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_s = (df_w['task'] != 'Baseline').astype(int)
        
        X_t = df_b.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_t = (df_b['task'] != 'Baseline').astype(int)
        
        res, _, _, _ = run_experiment_pipeline(X_s, y_s, X_t, y_t)
        res['Representation'] = norm
        res['N'] = df_b['subject_id'].nunique()
        res['Baseline windows'] = sum(y_t == 0)
        res['Stress windows'] = sum(y_t == 1)
        norm_results.append(res)
        
    pd.DataFrame(norm_results).to_csv(os.path.join(Q1_REPORTS_DIR, 'NORMALIZATION_COMPARISON_CORRECTED.csv'), index=False)
    
    # PART C: Calibration Duration
    print("Part C: Calibration Duration")
    dur_results = []
    for dur in [30, 60, 120, 300]:
        print(f"Running duration: {dur}")
        df_w, df_b = extract_features_for_norm('zscore', w_segs_raw, b_segs_raw, calib_dur=dur)
        X_s = df_w.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_s = (df_w['task'] != 'Baseline').astype(int)
        X_t = df_b.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_t = (df_b['task'] != 'Baseline').astype(int)
        
        res, _, _, _ = run_experiment_pipeline(X_s, y_s, X_t, y_t)
        res['Calibration Duration (s)'] = dur
        dur_results.append(res)
    pd.DataFrame(dur_results).to_csv(os.path.join(Q1_REPORTS_DIR, 'CALIBRATION_DURATION_RESULTS_CORRECTED.csv'), index=False)

    # Re-load standard base (60s zscore) and absolute for remaining ablations
    df_w_rel, df_b_rel = extract_features_for_norm('zscore', w_segs_raw, b_segs_raw)
    df_w_abs, df_b_abs = extract_features_for_norm('absolute', w_segs_raw, b_segs_raw)
    
    # PART F: Domain Shift
    print("Part F: Domain Shift")
    run_domain_shift_analysis(df_w_abs, df_b_abs, Q1_REPORTS_DIR)
    
    # PART G: Modality Ablation
    print("Part G: Modality Ablation")
    mod_combs = [
        ['EDA'], ['BVP'], ['TEMP'], ['ACC'],
        ['EDA','BVP'], ['EDA','TEMP'], ['BVP','TEMP'],
        ['EDA','BVP','TEMP'], ['EDA','BVP','TEMP','ACC']
    ]
    
    mod_results = []
    for rep_name, (w_df, b_df) in [('Absolute', (df_w_abs, df_b_abs)), ('Relative', (df_w_rel, df_b_rel))]:
        for mods in mod_combs:
            # filter columns
            feat_cols = [c for c in w_df.columns if c not in ['window_idx', 'subject_id', 'task', 'dataset'] and any(c.startswith(m) for m in mods)]
            
            X_s = w_df[feat_cols]
            y_s = (w_df['task'] != 'Baseline').astype(int)
            X_t = b_df[feat_cols]
            y_t = (b_df['task'] != 'Baseline').astype(int)
            
            res, _, _, _ = run_experiment_pipeline(X_s, y_s, X_t, y_t)
            res['Representation'] = rep_name
            res['Modalities'] = "+".join(mods)
            mod_results.append(res)
            
    pd.DataFrame(mod_results).to_csv(os.path.join(Q1_REPORTS_DIR, 'MODALITY_FACTORIAL_RESULTS_CORRECTED.csv'), index=False)
    
    # PART H: Classifier Robustness
    print("Part H: Classifier Robustness")
    clf_results = []
    clfs = ['lr', 'svm', 'rf', 'xgboost']
    for rep_name, (w_df, b_df) in [('Absolute', (df_w_abs, df_b_abs)), ('Relative', (df_w_rel, df_b_rel))]:
        X_s = w_df.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_s = (w_df['task'] != 'Baseline').astype(int)
        X_t = b_df.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_t = (b_df['task'] != 'Baseline').astype(int)
        
        for clf in clfs:
            res, _, _, _ = run_experiment_pipeline(X_s, y_s, X_t, y_t, clf_type=clf)
            res['Representation'] = rep_name
            res['Classifier'] = clf
            clf_results.append(res)
            
    pd.DataFrame(clf_results).to_csv(os.path.join(Q1_REPORTS_DIR, 'CLASSIFIER_ROBUSTNESS_CORRECTED.csv'), index=False)

    # PART I: Feature Selection
    print("Part I: Feature Selection")
    fs_results = []
    for k in [5, 10, 15, 20, 30, 50, 'all']:
        X_s = df_w_rel.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_s = (df_w_rel['task'] != 'Baseline').astype(int)
        X_t = df_b_rel.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
        y_t = (df_b_rel['task'] != 'Baseline').astype(int)
        
        res, pipeline, _, _ = run_experiment_pipeline(X_s, y_s, X_t, y_t, k_best=k)
        res['K'] = str(k)
        fs_results.append(res)
        
        if k == 20:
            final_features = pipeline.selected_features
            with open(os.path.join(Q1_REPORTS_DIR, 'FINAL_SELECTED_FEATURES_CORRECTED.csv'), 'w') as f:
                f.write("Rank,Feature,Modality,ANOVA_F_score\n")
                scores = pipeline.selector.scores_[pipeline.selector.get_support()]
                # sort
                sorted_idx = np.argsort(scores)[::-1]
                for i, idx in enumerate(sorted_idx):
                    feat = final_features[idx]
                    mod = feat.split('_')[0] if 'ACC' not in feat else 'ACC'
                    f.write(f"{i+1},{feat},{mod},{scores[idx]}\n")
                    
    pd.DataFrame(fs_results).to_csv(os.path.join(Q1_REPORTS_DIR, 'FEATURE_SELECTION_SENSITIVITY_CORRECTED.csv'), index=False)

    # PART M: SHAP
    print("Part M: SHAP")
    X_s = df_w_rel.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
    y_s = (df_w_rel['task'] != 'Baseline').astype(int)
    X_t = df_b_rel.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'], errors='ignore')
    y_t = (df_b_rel['task'] != 'Baseline').astype(int)
    
    res, pipeline, y_pred, y_prob = run_experiment_pipeline(X_s, y_s, X_t, y_t)
    
    # SHAP over target
    explainer = shap.TreeExplainer(pipeline.clf)
    X_t_sel = pipeline.selector.transform(X_t)
    X_t_scaled = pipeline.scaler.transform(X_t_sel)
    shap_vals_t = explainer.shap_values(X_t_scaled)
    mean_abs_shap_t = np.mean(np.abs(shap_vals_t), axis=0)
    
    # SHAP over source
    X_s_sel = pipeline.selector.transform(X_s)
    X_s_scaled = pipeline.scaler.transform(X_s_sel)
    shap_vals_s = explainer.shap_values(X_s_scaled)
    mean_abs_shap_s = np.mean(np.abs(shap_vals_s), axis=0)
    
    rho, _ = spearmanr(mean_abs_shap_s, mean_abs_shap_t)
    tau, _ = kendalltau(mean_abs_shap_s, mean_abs_shap_t)
    
    with open(os.path.join(Q1_REPORTS_DIR, 'SHAP_STABILITY_METRICS.csv'), 'w') as f:
        f.write("Metric,Value\n")
        f.write(f"Spearman rho,{rho}\n")
        f.write(f"Kendall tau,{tau}\n")
        
    print("All tasks completed.")

if __name__ == "__main__":
    main()
