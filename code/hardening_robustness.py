import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import LeaveOneGroupOut
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score, recall_score, confusion_matrix
from sklearn.linear_model import LogisticRegression

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import PROJECT_ROOT, WESAD_ROOT, DATASET_B_ROOT, WINDOW_SIZE, STEP_SIZE, RANDOM_SEED, K_BEST
from data_loaders import load_all_wesad, load_all_dataset_b
from windowing import sliding_window
from features import build_feature_matrix
from pipeline import get_base_model, run_nested_cv
from metrics import aggregate_subject_predictions
from hardening_utils import apply_baseline_relative_transform

def get_metrics(y_true, y_prob):
    y_pred = (y_prob >= 0.5).astype(int)
    if len(np.unique(y_true)) > 1:
        try:
            auc = roc_auc_score(y_true, y_prob)
            pr = average_precision_score(y_true, y_prob)
        except:
            auc = np.nan
            pr = np.nan
    else:
        auc = np.nan
        pr = np.nan
        
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    sens = recall_score(y_true, y_pred, zero_division=0)
    
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    return auc, pr, bal_acc, sens, spec

def train_and_eval(w_wins, b_wins, allowed_modalities, model_type='xgb'):
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
    
    if model_type == 'xgb':
        model = get_base_model()
    else:
        model = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
        
    model.fit(X_train_res, y_train_res)
    
    df_b = build_feature_matrix(b_wins, allowed_modalities=allowed_modalities)
    stress_tasks = ["TMCT", "Real Opinion", "Opposite Opinion", "Subtract"]
    valid_tasks = ["Baseline"] + stress_tasks
    df_b_filtered = df_b[df_b['task'].isin(valid_tasks)].copy()
    df_b_filtered['label'] = df_b_filtered['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
    
    mask = ~df_b_filtered['subject_id'].isin(['S02', 'f07', 'f14'])
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
    
    # ---------------------------------------------------------
    # PHASE 5: BASELINE DURATION SENSITIVITY
    # ---------------------------------------------------------
    print("--- STARTING PHASE 5: BASELINE DURATION SENSITIVITY ---")
    durations = [30, 60, 120, 180, 300, None] # None = Full baseline
    duration_labels = ['30s', '60s', '120s', '180s', '300s', 'Full']
    
    res_phase5 = []
    
    for dur, label in zip(durations, duration_labels):
        print(f"  Testing duration: {label}")
        w_segs_rel = apply_baseline_relative_transform(w_segs_raw, baseline_duration_sec=dur)
        b_segs_rel = apply_baseline_relative_transform(b_segs_raw, baseline_duration_sec=dur)
        
        w_wins = sliding_window(w_segs_rel, window_size=WINDOW_SIZE, step=STEP_SIZE)
        b_wins = sliding_window(b_segs_rel, window_size=WINDOW_SIZE, step=STEP_SIZE)
        
        auc, pr, bal_acc, sens, spec = train_and_eval(w_wins, b_wins, ['EDA', 'BVP', 'TEMP'])
        res_phase5.append({
            'Duration': label,
            'ROC-AUC': auc,
            'PR-AUC': pr,
            'Balanced Accuracy': bal_acc,
            'Sensitivity': sens,
            'Specificity': spec
        })
        
    df_p5 = pd.DataFrame(res_phase5)
    df_p5.to_csv(os.path.join(reports_dir, "baseline_duration_sensitivity.csv"), index=False)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_p5, x='Duration', y='ROC-AUC', marker='o', label='ROC-AUC')
    sns.lineplot(data=df_p5, x='Duration', y='Balanced Accuracy', marker='o', label='Balanced Acc')
    plt.title('Performance vs Baseline Duration (Zero-Shot on Dataset B)')
    plt.ylim(0.5, 1.05)
    plt.savefig(os.path.join(reports_dir, "baseline_duration_sensitivity.png"))
    plt.close()
    
    with open(os.path.join(reports_dir, "baseline_duration_audit.md"), "w") as f:
        f.write("# Phase 5: Baseline Duration Sensitivity Audit\n\n")
        f.write(df_p5.to_markdown(index=False))
        f.write("\n\n**Analysis**: Evaluates if the transfer success is robust to extremely short calibration periods.")
        
    # ---------------------------------------------------------
    # PHASE 7: MODALITY ROBUSTNESS
    # ---------------------------------------------------------
    print("--- STARTING PHASE 7: MODALITY ROBUSTNESS ---")
    modalities = [
        ['EDA'], ['BVP'], ['TEMP'],
        ['EDA', 'BVP'], ['EDA', 'TEMP'], ['BVP', 'TEMP'],
        ['EDA', 'BVP', 'TEMP']
    ]
    mod_labels = ['EDA', 'BVP', 'TEMP', 'EDA+BVP', 'EDA+TEMP', 'BVP+TEMP', 'EDA+BVP+TEMP']
    
    w_segs_rel_full = apply_baseline_relative_transform(w_segs_raw)
    b_segs_rel_full = apply_baseline_relative_transform(b_segs_raw)
    w_wins_full = sliding_window(w_segs_rel_full, window_size=WINDOW_SIZE, step=STEP_SIZE)
    b_wins_full = sliding_window(b_segs_rel_full, window_size=WINDOW_SIZE, step=STEP_SIZE)
    
    res_phase7 = []
    
    for mods, label in zip(modalities, mod_labels):
        print(f"  Testing modalities: {label}")
        auc, pr, bal_acc, sens, spec = train_and_eval(w_wins_full, b_wins_full, mods)
        res_phase7.append({
            'Modality': label,
            'ROC-AUC': auc,
            'Balanced Accuracy': bal_acc
        })
        
    df_p7 = pd.DataFrame(res_phase7)
    df_p7.to_csv(os.path.join(reports_dir, "relative_modality_ablation.csv"), index=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_p7, x='Modality', y='ROC-AUC')
    plt.axhline(0.5, color='red', linestyle='--')
    plt.xticks(rotation=45)
    plt.title('Modality Ablation under Relative Normalization (Dataset B ROC-AUC)')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, "relative_modality_ablation.png"))
    plt.close()
    
    with open(os.path.join(reports_dir, "relative_modality_audit.md"), "w") as f:
        f.write("# Phase 7: Modality Robustness Audit\n\n")
        f.write(df_p7.to_markdown(index=False))
        f.write("\n\n**Analysis**: Determines which modalities drive the successful transfer when subject-specific baselining is applied.")
        
    # ---------------------------------------------------------
    # PHASE 8: SIMPLE MODEL ROBUSTNESS
    # ---------------------------------------------------------
    print("--- STARTING PHASE 8: SIMPLE MODEL ROBUSTNESS ---")
    
    # Internal WESAD LR (nested CV)
    df_w_full = build_feature_matrix(w_wins_full, allowed_modalities=['EDA', 'BVP', 'TEMP'])
    feat_cols = [c for c in df_w_full.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
    X_w = df_w_full[feat_cols]
    y_w = df_w_full['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
    g_w = df_w_full['subject_id']
    
    print("  Running WESAD internal nested CV for LR...")
    
    # Custom nested CV for LR
    logo = LeaveOneGroupOut()
    oof_preds_lr = np.zeros(len(y_w))
    
    for train_idx, test_idx in logo.split(X_w, y_w, g_w):
        X_train, y_train = X_w.iloc[train_idx], y_w.iloc[train_idx]
        X_test = X_w.iloc[test_idx]
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        k = min(K_BEST, X_train_scaled.shape[1])
        selector = SelectKBest(f_classif, k=k)
        X_train_sel = selector.fit_transform(X_train_scaled, y_train)
        X_test_sel = selector.transform(X_test_scaled)
        
        sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=5)
        X_train_res, y_train_res = sm.fit_resample(X_train_sel, y_train)
        
        model = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
        model.fit(X_train_res, y_train_res)
        oof_preds_lr[test_idx] = model.predict_proba(X_test_sel)[:, 1]
        
    y_true_w_lr, y_prob_w_lr = aggregate_subject_predictions(y_w.values, oof_preds_lr, g_w.values)
    lr_w_auc, _, lr_w_bal_acc, _, _ = get_metrics(y_true_w_lr, y_prob_w_lr)
    
    # External Dataset B LR
    print("  Running Dataset B inference for LR...")
    lr_b_auc, _, lr_b_bal_acc, _, _ = train_and_eval(w_wins_full, b_wins_full, ['EDA', 'BVP', 'TEMP'], model_type='lr')
    xgb_b_auc, _, xgb_b_bal_acc, _, _ = train_and_eval(w_wins_full, b_wins_full, ['EDA', 'BVP', 'TEMP'], model_type='xgb')
    
    res_phase8 = [
        {'Condition': 'Internal WESAD (LR)', 'ROC-AUC': lr_w_auc, 'Balanced Accuracy': lr_w_bal_acc},
        {'Condition': 'External Dataset B (LR)', 'ROC-AUC': lr_b_auc, 'Balanced Accuracy': lr_b_bal_acc},
        {'Condition': 'External Dataset B (XGB)', 'ROC-AUC': xgb_b_auc, 'Balanced Accuracy': xgb_b_bal_acc}
    ]
    df_p8 = pd.DataFrame(res_phase8)
    df_p8.to_csv(os.path.join(reports_dir, "model_comparison.csv"), index=False)
    
    with open(os.path.join(reports_dir, "model_comparison.md"), "w") as f:
        f.write("# Phase 8: Simple Model Robustness Audit\n\n")
        f.write(df_p8.to_markdown(index=False))
        f.write("\n\n**Analysis**: Evaluates if the high performance is dependent on non-linear XGBoost architecture or if the baseline-relative representation is linearly separable.")
        
    print("Phases 5, 7, 8 completed successfully.")

if __name__ == "__main__":
    main()
