import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import PROJECT_ROOT, WESAD_ROOT, DATASET_B_ROOT, WINDOW_SIZE, STEP_SIZE, RANDOM_SEED, K_BEST
from data_loaders import load_all_wesad, load_all_dataset_b
from windowing import sliding_window
from features import build_feature_matrix
from pipeline import get_base_model
from metrics import aggregate_subject_predictions
from hardening_utils import apply_baseline_relative_transform
from hardening_robustness import train_and_eval, get_metrics

def evaluate_pipeline(w_wins, b_wins, allowed_modalities, exclude_subjects):
    df_w = build_feature_matrix(w_wins, allowed_modalities=allowed_modalities)
    feat_cols = [c for c in df_w.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
    X_train_raw = df_w[feat_cols]
    y_train = df_w['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    
    k = min(K_BEST, X_train_scaled.shape[1])
    selector = SelectKBest(f_classif, k=k)
    X_train_sel = selector.fit_transform(X_train_scaled, y_train)
    
    sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=5)
    X_train_res, y_train_res = sm.fit_resample(X_train_sel, y_train)
    
    model = get_base_model()
    model.fit(X_train_res, y_train_res)
    
    df_b = build_feature_matrix(b_wins, allowed_modalities=allowed_modalities)
    stress_tasks = ["TMCT", "Real Opinion", "Opposite Opinion", "Subtract"]
    valid_tasks = ["Baseline"] + stress_tasks
    df_b_filtered = df_b[df_b['task'].isin(valid_tasks)].copy()
    df_b_filtered['label'] = df_b_filtered['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
    
    mask = ~df_b_filtered['subject_id'].isin(exclude_subjects)
    df_eval = df_b_filtered[mask].copy()
    
    # Handle missing features explicitly
    for col in feat_cols:
        if col not in df_eval.columns:
            df_eval[col] = 0.0
            
    X_test_raw = df_eval[feat_cols].fillna(0)
    X_test_scaled = scaler.transform(X_test_raw)
    X_test_sel = selector.transform(X_test_scaled)
    df_eval['prob'] = model.predict_proba(X_test_sel)[:, 1]
    
    y_true, y_prob = aggregate_subject_predictions(df_eval['label'].values, df_eval['prob'].values, df_eval['subject_id'].values)
    return get_metrics(y_true, y_prob)

def main():
    reports_dir = os.path.join(PROJECT_ROOT, "reports", "final_hardening")
    os.makedirs(reports_dir, exist_ok=True)
    
    print("Loading datasets...")
    w_segs_raw = load_all_wesad(WESAD_ROOT)
    b_segs_raw = load_all_dataset_b(DATASET_B_ROOT)
    
    # Precompute relative datasets
    w_segs_rel = apply_baseline_relative_transform(w_segs_raw)
    b_segs_rel = apply_baseline_relative_transform(b_segs_raw)
    
    # Precompute windows
    w_wins_abs = sliding_window(w_segs_raw, window_size=WINDOW_SIZE, step=STEP_SIZE)
    b_wins_abs = sliding_window(b_segs_raw, window_size=WINDOW_SIZE, step=STEP_SIZE)
    w_wins_rel = sliding_window(w_segs_rel, window_size=WINDOW_SIZE, step=STEP_SIZE)
    b_wins_rel = sliding_window(b_segs_rel, window_size=WINDOW_SIZE, step=STEP_SIZE)
    
    # ---------------------------------------------------------
    # PHASE 6: NORMALIZATION x ACC FACTORIAL ABLATION
    # ---------------------------------------------------------
    print("--- STARTING PHASE 6: NORMALIZATION x ACC FACTORIAL ---")
    
    exclude_standard = ['S02', 'f07', 'f14']
    
    print("  Evaluating Absolute + ACC (Exp 3)...")
    abs_acc = evaluate_pipeline(w_wins_abs, b_wins_abs, ['EDA', 'BVP', 'TEMP', 'ACC'], exclude_standard)
    
    print("  Evaluating Absolute - ACC (Exp 4)...")
    abs_no_acc = evaluate_pipeline(w_wins_abs, b_wins_abs, ['EDA', 'BVP', 'TEMP'], exclude_standard)
    
    print("  Evaluating Relative - ACC (Exp 5)...")
    rel_no_acc = evaluate_pipeline(w_wins_rel, b_wins_rel, ['EDA', 'BVP', 'TEMP'], exclude_standard)
    
    print("  Evaluating Relative + ACC (NEW)...")
    rel_acc = evaluate_pipeline(w_wins_rel, b_wins_rel, ['EDA', 'BVP', 'TEMP', 'ACC'], exclude_standard)
    
    res_phase6 = [
        {'Condition': 'Absolute + ACC (Exp 3)', 'ROC-AUC': abs_acc[0], 'Balanced Accuracy': abs_acc[2]},
        {'Condition': 'Absolute - ACC (Exp 4)', 'ROC-AUC': abs_no_acc[0], 'Balanced Accuracy': abs_no_acc[2]},
        {'Condition': 'Relative + ACC (NEW)', 'ROC-AUC': rel_acc[0], 'Balanced Accuracy': rel_acc[2]},
        {'Condition': 'Relative - ACC (Exp 5)', 'ROC-AUC': rel_no_acc[0], 'Balanced Accuracy': rel_no_acc[2]}
    ]
    df_p6 = pd.DataFrame(res_phase6)
    df_p6.to_csv(os.path.join(reports_dir, "normalization_acc_factorial.csv"), index=False)
    
    with open(os.path.join(reports_dir, "normalization_acc_factorial.md"), "w") as f:
        f.write("# Phase 6: Normalization × ACC Factorial Ablation\n\n")
        f.write(df_p6.to_markdown(index=False))
        f.write("\n\n**Analysis**: Evaluates the interaction between modality inclusion (ACC) and physiological representation (Absolute vs Relative). It determines if the presence of ACC degrades a relative model, or if relative normalization rescues the ACC model.")
        
    # ---------------------------------------------------------
    # PHASE 10: EXCLUSION SENSITIVITY
    # ---------------------------------------------------------
    print("--- STARTING PHASE 10: EXCLUSION SENSITIVITY ---")
    
    # A. Primary cohort (S02, f07, f14 excluded)
    # B. Include S02 (f07, f14 excluded)
    # C. Exclude S02 (Primary)
    # D. Exclude f14 (Wait, f14 has missing data, we can fill with 0, which evaluate_pipeline handles)
    # Let's test combinations carefully:
    
    ex_tests = [
        {'Cohort': 'Primary (Exclude S02, f07, f14)', 'Excludes': ['S02', 'f07', 'f14']},
        {'Cohort': 'Include S02 (Exclude f07, f14)', 'Excludes': ['f07', 'f14']},
        {'Cohort': 'Include f14 (Exclude S02, f07)', 'Excludes': ['S02', 'f07']},
        {'Cohort': 'Include S02 & f14 (Exclude f07)', 'Excludes': ['f07']},
        {'Cohort': 'Include All (No Exclusions)', 'Excludes': []}
    ]
    
    res_phase10 = []
    for test in ex_tests:
        print(f"  Testing cohort: {test['Cohort']}")
        auc, pr, bal_acc, sens, spec = evaluate_pipeline(w_wins_rel, b_wins_rel, ['EDA', 'BVP', 'TEMP'], test['Excludes'])
        
        # Calculate N
        df_b = build_feature_matrix(b_wins_rel, allowed_modalities=['EDA', 'BVP', 'TEMP'])
        valid_tasks = ["Baseline", "TMCT", "Real Opinion", "Opposite Opinion", "Subtract"]
        df_b_filtered = df_b[df_b['task'].isin(valid_tasks)].copy()
        mask = ~df_b_filtered['subject_id'].isin(test['Excludes'])
        n_subjects = df_b_filtered[mask]['subject_id'].nunique()
        
        res_phase10.append({
            'Cohort': test['Cohort'],
            'N Subjects': n_subjects,
            'ROC-AUC': auc,
            'Balanced Accuracy': bal_acc
        })
        
    df_p10 = pd.DataFrame(res_phase10)
    df_p10.to_csv(os.path.join(reports_dir, "exclusion_sensitivity.csv"), index=False)
    
    with open(os.path.join(reports_dir, "exclusion_sensitivity.md"), "w") as f:
        f.write("# Phase 10: Exclusion Sensitivity Audit\n\n")
        f.write(df_p10.to_markdown(index=False))
        f.write("\n\n**Analysis**: Demonstrates the impact of including anomalous subjects (S02) or subjects with hardware failures (f07, f14) on the final reported metrics.")

    print("Phases 6 and 10 completed successfully.")

if __name__ == "__main__":
    main()
