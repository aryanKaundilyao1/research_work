import os
import sys
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, matthews_corrcoef, brier_score_loss, confusion_matrix, average_precision_score, f1_score
from scipy.stats import spearmanr, kendalltau

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import WESAD_ROOT, DATASET_B_ROOT, REPORTS_DIR, OUTPUT_DIR, WINDOW_SIZE, STEP_SIZE
from data_loaders import load_all_wesad, load_all_dataset_b
from windowing import sliding_window
from features import build_feature_matrix
from q1_core import apply_strict_baseline_relative_transform, audit_leakage
from q1_feature_pipeline import RigorousSourceTargetPipeline
from q1_experiments import run_subject_aware_evaluation, run_v1_v2_analysis

Q1_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'q1_rebuild')
Q1_REPORTS_DIR = os.path.join(REPORTS_DIR, 'q1_rebuild')
os.makedirs(Q1_OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(Q1_OUTPUT_DIR, 'cache'), exist_ok=True)

def get_cached_or_compute(cache_file, compute_fn, force=False):
    if not force and os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    data = compute_fn()
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
    return data

def main():
    print("==================================================")
    print("FINAL POST-HOC METRIC VALIDITY RESCUE RUN")
    print("==================================================")
    
    # 1. Load Data
    w_segs_raw = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'w_segs_raw.pkl'),
        lambda: load_all_wesad(WESAD_ROOT)
    )
    b_segs_raw = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'b_segs_raw.pkl'),
        lambda: load_all_dataset_b(DATASET_B_ROOT)
    )
    b_segs_raw = [s for s in b_segs_raw if s['subject_id'] != 'f07']
    
    # 2. Strict Calibration Design (30s calib, 30s buffer) for TARGET
    b_segs_rel, b_audit_rows = apply_strict_baseline_relative_transform(
        b_segs_raw, calib_duration_sec=30, buffer_sec=30, norm_type='zscore'
    )
    
    # 8. Source-Side Representation Consistency (30s vs full)
    # The prompt explicitly asks to compare WESAD with 30s calib.
    w_segs_rel_30, _ = apply_strict_baseline_relative_transform(
        w_segs_raw, calib_duration_sec=30, buffer_sec=30, norm_type='zscore'
    )
    # Let's use 30s for source to match target calibration exactly (symmetric).
    
    b_wins_rel = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'b_wins_rel_30s.pkl'),
        lambda: sliding_window(b_segs_rel, window_size=WINDOW_SIZE, step=STEP_SIZE),
        force=True
    )
    w_wins_rel = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'w_wins_rel_30s.pkl'),
        lambda: sliding_window(w_segs_rel_30, window_size=WINDOW_SIZE, step=STEP_SIZE),
        force=True
    )
    
    # Leakage Audit
    df_leak_audit = audit_leakage(b_wins_rel, b_audit_rows, Q1_REPORTS_DIR)
    if (df_leak_audit['Raw overlap count'] > 0).any():
        print("FAIL: Leakage detected!")
        sys.exit(1)
    
    df_w_feats = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'df_w_feats_rel_30s.pkl'),
        lambda: build_feature_matrix(w_wins_rel),
        force=True
    )
    df_b_feats = get_cached_or_compute(
        os.path.join(Q1_OUTPUT_DIR, 'cache', 'df_b_feats_rel_30s.pkl'),
        lambda: build_feature_matrix(b_wins_rel),
        force=True
    )
    
    # RELATIVE PIPELINE
    X_s = df_w_feats.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    y_s = (df_w_feats['task'] != 'Baseline').astype(int)
    X_t = df_b_feats.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    y_t = (df_b_feats['task'] != 'Baseline').astype(int)
    meta_t = df_b_feats[['window_idx', 'subject_id', 'task', 'dataset']].to_dict('records')
    
    pipe_rel = RigorousSourceTargetPipeline(k_best=20, clf_type='xgboost')
    pipe_rel.fit_source(X_s, y_s)
    y_prob_rel = pipe_rel.predict_proba_target(X_t)
    
    df_subj_rel, mean_auc_rel, ci_rel = run_subject_aware_evaluation(meta_t, y_t, y_prob_rel, Q1_OUTPUT_DIR, name="RELATIVE_30s")
    
    # ABSOLUTE PIPELINE
    # Create absolute windows (raw without transform)
    b_wins_abs = sliding_window(b_segs_raw, window_size=WINDOW_SIZE, step=STEP_SIZE)
    w_wins_abs = sliding_window(w_segs_raw, window_size=WINDOW_SIZE, step=STEP_SIZE)
    df_w_abs = build_feature_matrix(w_wins_abs)
    df_b_abs = build_feature_matrix(b_wins_abs)
    
    X_s_abs = df_w_abs.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    y_s_abs = (df_w_abs['task'] != 'Baseline').astype(int)
    X_t_abs = df_b_abs.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    y_t_abs = (df_b_abs['task'] != 'Baseline').astype(int)
    meta_t_abs = df_b_abs[['window_idx', 'subject_id', 'task', 'dataset']].to_dict('records')
    
    pipe_abs = RigorousSourceTargetPipeline(k_best=20, clf_type='xgboost')
    pipe_abs.fit_source(X_s_abs, y_s_abs)
    y_prob_abs = pipe_abs.predict_proba_target(X_t_abs)
    
    df_subj_abs, mean_auc_abs, ci_abs = run_subject_aware_evaluation(meta_t_abs, y_t_abs, y_prob_abs, Q1_OUTPUT_DIR, name="ABSOLUTE_30s")
    
    # V1 vs V2
    run_v1_v2_analysis(df_subj_rel, Q1_OUTPUT_DIR)
    
    # Delta and Exact Confidence Intervals on matched eligible subjects
    eligible_rel = df_subj_rel[df_subj_rel['Eligible for macro AUROC?']]
    eligible_abs = df_subj_abs[df_subj_abs['Subject'].isin(eligible_rel['Subject'])] # match subjects
    
    aucs_rel = eligible_rel['Subject AUROC'].values
    aucs_abs = eligible_abs['Subject AUROC'].values
    deltas = aucs_rel - aucs_abs
    mean_delta = np.mean(deltas)
    
    np.random.seed(42)
    n_boot = 5000
    boot_deltas = [np.mean(np.random.choice(deltas, size=len(deltas), replace=True)) for _ in range(n_boot)]
    ci_delta_lower = np.percentile(boot_deltas, 2.5)
    ci_delta_upper = np.percentile(boot_deltas, 97.5)
    
    # Secondary Metrics (Participant-Balanced)
    # We balance by giving each participant's windows a weight inversely proportional to their window count in that class
    sample_weights = np.ones(len(y_t))
    for subj in df_b_feats['subject_id'].unique():
        mask_subj = df_b_feats['subject_id'] == subj
        mask_base = mask_subj & (df_b_feats['task'] == 'Baseline')
        mask_stress = mask_subj & (df_b_feats['task'] != 'Baseline')
        
        n_base = mask_base.sum()
        n_stress = mask_stress.sum()
        if n_base > 0: sample_weights[mask_base] = 1.0 / n_base
        if n_stress > 0: sample_weights[mask_stress] = 1.0 / n_stress
        
    y_pred_rel = (y_prob_rel >= 0.5).astype(int)
    bal_acc = balanced_accuracy_score(y_t, y_pred_rel, sample_weight=sample_weights)
    mcc = matthews_corrcoef(y_t, y_pred_rel, sample_weight=sample_weights)
    
    cm = confusion_matrix(y_t, y_pred_rel, sample_weight=sample_weights)
    sens = cm[1,1] / (cm[1,0] + cm[1,1]) if (cm[1,0] + cm[1,1]) > 0 else 0
    spec = cm[0,0] / (cm[0,0] + cm[0,1]) if (cm[0,0] + cm[0,1]) > 0 else 0
    
    brier = brier_score_loss(y_t, y_prob_rel, sample_weight=sample_weights)
    
    # SHAP
    import shap
    X_t_selected = pipe_rel.scaler.transform(pipe_rel.selector.transform(X_t))
    X_s_selected = pipe_rel.scaler.transform(pipe_rel.selector.transform(X_s))
    
    explainer = shap.TreeExplainer(pipe_rel.clf)
    shap_vals_t = explainer.shap_values(X_t_selected)
    mean_shap_t = np.mean(np.abs(shap_vals_t), axis=0)
    
    shap_vals_s = explainer.shap_values(X_s_selected)
    mean_shap_s = np.mean(np.abs(shap_vals_s), axis=0)
    
    rho, _ = spearmanr(mean_shap_s, mean_shap_t)
    tau, _ = kendalltau(mean_shap_s, mean_shap_t)
    
    top_5_s = np.argsort(mean_shap_s)[-5:]
    top_5_t = np.argsort(mean_shap_t)[-5:]
    jacc_5 = len(np.intersect1d(top_5_s, top_5_t)) / len(np.union1d(top_5_s, top_5_t))
    
    top_10_s = np.argsort(mean_shap_s)[-10:]
    top_10_t = np.argsort(mean_shap_t)[-10:]
    jacc_10 = len(np.intersect1d(top_10_s, top_10_t)) / len(np.union1d(top_10_s, top_10_t))
    
    print("\n==================================================")
    print("15. FINAL OUTPUT")
    print("==================================================")
    print(f"Target cohort N = {len(df_subj_rel)}")
    print(f"Subjects with both evaluation classes = {len(eligible_rel)}")
    print(f"Coverage = {len(eligible_rel)}/{len(df_subj_rel)} = {len(eligible_rel)/len(df_subj_rel)*100:.1f}%")
    print(f"Subjects with zero baseline evaluation windows = {(df_subj_rel['Baseline windows'] == 0).sum()}")
    print(f"Baseline evaluation windows = {df_subj_rel['Baseline windows'].sum()}")
    print(f"Stress evaluation windows = {df_subj_rel['Stress windows'].sum()}")
    print(f"Median baseline windows per contributing subject = {eligible_rel['Baseline windows'].median()}")
    
    print(f"\nPRIMARY macro subject AUROC = {mean_auc_rel:.4f}")
    print(f"95% CI = [{ci_rel[0]:.4f}, {ci_rel[1]:.4f}]")
    print(f"Median subject AUROC = {eligible_rel['Subject AUROC'].median():.4f}")
    print(f"IQR = {eligible_rel['Subject AUROC'].quantile(0.75) - eligible_rel['Subject AUROC'].quantile(0.25):.4f}")
    
    print(f"\nCorrected absolute macro AUROC = {np.mean(aucs_abs):.4f}")
    print(f"Corrected relative macro AUROC = {mean_auc_rel:.4f}")
    print(f"Corrected delta = {mean_delta:.4f}")
    print(f"Delta 95% CI = [{ci_delta_lower:.4f}, {ci_delta_upper:.4f}]")
    
    print(f"\nBalanced Accuracy = {bal_acc:.4f}")
    print(f"MCC = {mcc:.4f}")
    print(f"Sensitivity = {sens:.4f}")
    print(f"Specificity = {spec:.4f}")
    print(f"Brier = {brier:.4f}")
    print(f"ECE = N/A")
    
    v1_rel = df_subj_rel[df_subj_rel['Protocol'] == 'V1']
    v2_rel = df_subj_rel[df_subj_rel['Protocol'] == 'V2']
    print(f"\nV1 AUROC = {v1_rel[v1_rel['Eligible for macro AUROC?']]['Subject AUROC'].mean():.4f}")
    print(f"V1 N = {len(v1_rel)}")
    print(f"V2 AUROC = {v2_rel[v2_rel['Eligible for macro AUROC?']]['Subject AUROC'].mean():.4f}")
    print(f"V2 N = {len(v2_rel)}")
    
    print(f"\nCanonical SHAP rho = {rho:.4f}")
    print(f"SHAP tau = {tau:.4f}")
    print(f"SHAP Top-5 Jaccard = {jacc_5:.4f}")
    print(f"SHAP Top-10 Jaccard = {jacc_10:.4f}")
    
    print(f"\nCalibration leakage: {'PASS' if (df_leak_audit['Raw overlap count'] == 0).all() else 'FAIL'}")

if __name__ == "__main__":
    main()
