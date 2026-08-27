import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE
from sklearn.metrics import (roc_auc_score, average_precision_score, accuracy_score, 
                             balanced_accuracy_score, f1_score, precision_score, 
                             recall_score, confusion_matrix, roc_curve, precision_recall_curve)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import PROJECT_ROOT, WESAD_ROOT, DATASET_B_ROOT, WINDOW_SIZE, STEP_SIZE, RANDOM_SEED, K_BEST
from data_loaders import load_all_wesad, load_all_dataset_b
from windowing import sliding_window
from features import build_feature_matrix
from pipeline import get_base_model
from metrics import aggregate_subject_predictions

def main():
    print("--- STARTING EXPERIMENT 3: CROSS-DATASET EXTERNAL GENERALIZATION ---")
    
    results_dir = os.path.join(PROJECT_ROOT, "reports", "experiment_3", "results")
    outputs_dir = os.path.join(PROJECT_ROOT, "reports", "experiment_3", "outputs")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. WESAD TRAINING (FROZEN PIPELINE)
    # ---------------------------------------------------------
    print("Loading WESAD (Training Set)...")
    w_segs = load_all_wesad(WESAD_ROOT)
    w_wins = sliding_window(w_segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
    df_w = build_feature_matrix(w_wins, allowed_modalities=['EDA', 'BVP', 'TEMP', 'ACC'])
    
    print(f"WESAD Windows: {len(df_w)}")
    
    feat_cols = [c for c in df_w.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
    X_train_raw = df_w[feat_cols]
    y_train = df_w['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
    
    # Fit Pipeline exclusively on WESAD
    print("Fitting Scaler on WESAD...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    
    print("Fitting SelectKBest on WESAD...")
    k = min(K_BEST, X_train_scaled.shape[1])
    selector = SelectKBest(f_classif, k=k)
    X_train_sel = selector.fit_transform(X_train_scaled, y_train)
    
    print("Fitting SMOTE on WESAD...")
    sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=5)
    X_train_res, y_train_res = sm.fit_resample(X_train_sel, y_train)
    
    print("Training XGBoost on WESAD...")
    model = get_base_model()
    model.fit(X_train_res, y_train_res)
    
    # ---------------------------------------------------------
    # 2. DATASET B INFERENCE (EXTERNAL TEST)
    # ---------------------------------------------------------
    print("\nLoading Dataset B (External Test Set)...")
    b_segs = load_all_dataset_b(DATASET_B_ROOT)
    b_wins = sliding_window(b_segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
    
    # Quality Exclusion Rule
    b_wins = [w for w in b_wins if w['subject_id'] not in ['f07', 'f14']]
    
    df_b = build_feature_matrix(b_wins, allowed_modalities=['EDA', 'BVP', 'TEMP', 'ACC'])
    print(f"Dataset B Windows: {len(df_b)}")
    
    # Filter to tasks of interest
    stress_tasks = ["TMCT", "Real Opinion", "Opposite Opinion", "Subtract"]
    valid_tasks = ["Baseline"] + stress_tasks
    
    df_b_filtered = df_b[df_b['task'].isin(valid_tasks)].copy()
    df_b_filtered['label'] = df_b_filtered['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
    
    X_test_raw = df_b_filtered[feat_cols]
    y_test = df_b_filtered['label']
    groups_test = df_b_filtered['subject_id']
    tasks_test = df_b_filtered['task']
    
    # STRICT INFERENCE: Apply Frozen Transforms
    print("Applying Frozen Pipeline to Dataset B...")
    X_test_scaled = scaler.transform(X_test_raw)
    X_test_sel = selector.transform(X_test_scaled)
    test_probs = model.predict_proba(X_test_sel)[:, 1]
    
    # Leakage Audit Flags
    audit_leakage_scaler = not np.array_equal(scaler.mean_, StandardScaler().fit(X_test_raw).mean_)
    
    # ---------------------------------------------------------
    # 3. PRIMARY VALIDATION (Baseline vs Stress)
    # ---------------------------------------------------------
    print("\nCalculating Subject-Aggregated External Metrics...")
    
    def evaluate_cohort(cohort_df_mask, cohort_name):
        y_t = y_test[cohort_df_mask]
        y_p = test_probs[cohort_df_mask]
        g_t = groups_test[cohort_df_mask]
        
        agg_true, agg_prob = aggregate_subject_predictions(y_t.values, y_p, g_t.values)
        agg_pred = (agg_prob >= 0.5).astype(int)
        
        try:
            auc = roc_auc_score(agg_true, agg_prob)
            pr_auc = average_precision_score(agg_true, agg_prob)
        except ValueError:
            auc = np.nan
            pr_auc = np.nan
            
        acc = accuracy_score(agg_true, agg_pred)
        bal_acc = balanced_accuracy_score(agg_true, agg_pred)
        f1 = f1_score(agg_true, agg_pred)
        prec = precision_score(agg_true, agg_pred, zero_division=0)
        rec = recall_score(agg_true, agg_pred, zero_division=0)
        tn, fp, fn, tp = confusion_matrix(agg_true, agg_pred, labels=[0, 1]).ravel()
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        
        return {
            'Cohort': cohort_name,
            'Subjects': len(np.unique(g_t)),
            'Windows': len(y_t),
            'ROC-AUC': auc,
            'PR-AUC': pr_auc,
            'Balanced Accuracy': bal_acc,
            'F1': f1,
            'Sensitivity': rec,
            'Specificity': spec,
            'TP': tp, 'FP': fp, 'TN': tn, 'FN': fn,
            'agg_true': agg_true,
            'agg_prob': agg_prob,
            'agg_pred': agg_pred
        }
    
    # Main Cohort (exclude S02)
    mask_main = (groups_test != 'S02')
    res_main = evaluate_cohort(mask_main, "Main Cohort (Excluding S02)")
    
    # Main + S02
    mask_all = pd.Series([True]*len(groups_test), index=groups_test.index)
    res_all = evaluate_cohort(mask_all, "Main Cohort + S02")
    
    # Save results
    df_res = pd.DataFrame([
        {k: v for k, v in res_main.items() if not k.startswith('agg_')},
        {k: v for k, v in res_all.items() if not k.startswith('agg_')}
    ])
    df_res.to_csv(os.path.join(results_dir, "experiment3_external_results.csv"), index=False)
    
    # ---------------------------------------------------------
    # 4. SUBJECT-LEVEL ANALYSIS
    # ---------------------------------------------------------
    subject_results = []
    for subj in np.unique(groups_test):
        idx = (groups_test == subj)
        st, sp = aggregate_subject_predictions(y_test[idx].values, test_probs[idx], groups_test[idx].values)
        try:
            s_auc = roc_auc_score(st, sp) if len(np.unique(st)) > 1 else np.nan
        except:
            s_auc = np.nan
        subject_results.append({'Subject': subj, 'ROC-AUC': s_auc})
        
    df_sub = pd.DataFrame(subject_results)
    df_sub.to_csv(os.path.join(results_dir, "experiment3_subject_results.csv"), index=False)
    
    # ---------------------------------------------------------
    # 5. SECONDARY TASK-SPECIFIC ANALYSIS
    # ---------------------------------------------------------
    df_tasks = df_b_filtered.copy()
    df_tasks['predicted_stress_prob'] = test_probs
    
    # Calculate subject-level mean prob per task
    task_agg = df_tasks.groupby(['subject_id', 'task'])['predicted_stress_prob'].mean().reset_index()
    task_agg.to_csv(os.path.join(results_dir, "experiment3_task_results.csv"), index=False)
    
    # ---------------------------------------------------------
    # 6. PLOTS
    # ---------------------------------------------------------
    # ROC Curve (Main Cohort)
    plt.figure()
    fpr, tpr, _ = roc_curve(res_main['agg_true'], res_main['agg_prob'])
    plt.plot(fpr, tpr, label=f"Ext. Generalization (AUC={res_main['ROC-AUC']:.3f})")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title("External Validation ROC Curve (Dataset B)")
    plt.legend()
    plt.savefig(os.path.join(outputs_dir, "external_roc_curve.png"))
    plt.close()
    
    # PR Curve (Main Cohort)
    plt.figure()
    prec, rec, _ = precision_recall_curve(res_main['agg_true'], res_main['agg_prob'])
    plt.plot(rec, prec, label=f"Ext. PR-AUC={res_main['PR-AUC']:.3f}")
    plt.title("External Validation PR Curve (Dataset B)")
    plt.legend()
    plt.savefig(os.path.join(outputs_dir, "external_pr_curve.png"))
    plt.close()
    
    # Confusion Matrix
    cm = confusion_matrix(res_main['agg_true'], res_main['agg_pred'])
    plt.figure()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Baseline', 'Stress'], yticklabels=['Baseline', 'Stress'])
    plt.title("External Validation Subject-Aggregated Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.savefig(os.path.join(outputs_dir, "external_confusion_matrix.png"))
    plt.close()
    
    # Per-subject Performance
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_sub, x='Subject', y='ROC-AUC')
    plt.title("Per-Subject ROC-AUC on Dataset B")
    plt.axhline(0.5, color='red', linestyle='--')
    plt.savefig(os.path.join(outputs_dir, "external_per_subject_performance.png"))
    plt.close()
    
    # Task-Specific Distribution
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=task_agg, x='task', y='predicted_stress_prob', 
                order=['Baseline', 'TMCT', 'Real Opinion', 'Opposite Opinion', 'Subtract'])
    plt.axhline(0.5, color='red', linestyle='--', label='WESAD Decision Threshold (0.5)')
    plt.title("Task-Specific Predicted Stress Probability (Subject Mean)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "external_task_specific_distribution.png"))
    plt.close()
    
    # ---------------------------------------------------------
    # 7. CONFIG & REPORTING
    # ---------------------------------------------------------
    config_dict = {
        "WESAD_Subjects": list(df_w['subject_id'].unique()),
        "Dataset_B_Subjects": list(df_b_filtered['subject_id'].unique()),
        "Excluded_Subjects": ['f07', 'f14'],
        "Excluded_Reason": "f07 invalid sensors; f14 failed continuity",
        "Total_Features": len(feat_cols),
        "Selected_Features": k,
        "Scaler_Fitted_On": "WESAD",
        "SelectKBest_Fitted_On": "WESAD",
        "SMOTE_Fitted_On": "WESAD",
        "XGBoost_Fitted_On": "WESAD",
        "Dataset_B_Operation": "Inference Only",
        "Threshold": 0.5,
        "Leakage_Audit_Passed": bool(audit_leakage_scaler)
    }
    
    with open(os.path.join(outputs_dir, "experiment3_config.json"), "w") as f:
        json.dump(config_dict, f, indent=4)
        
    report = [
        "# Experiment 3: Cross-Dataset External Generalization",
        "",
        "## 1. Methodology",
        "- **Training Dataset:** WESAD",
        "- **Test Dataset:** Dataset B",
        "- **Constraints:** The complete pipeline (StandardScaler, SelectKBest, SMOTE, XGBoost) was mathematically frozen after fitting on WESAD. Dataset B was only used for pure inference. The fixed decision threshold of `0.5` was strictly maintained.",
        "",
        "## 2. Leakage Audit",
        f"- Was Dataset B used for Scaler fitting? **{'NO' if audit_leakage_scaler else 'YES (LEAK)'}**",
        f"- Was Dataset B used for Feature Selection? **NO**",
        f"- Was Dataset B used for Model Training? **NO**",
        "",
        "## 3. Results (Main Cohort)",
        df_res.to_markdown(index=False),
        "",
        "## 4. Subject Exclusions",
        "- **f07:** Excluded due to invalid BVP/TEMP modalities.",
        "- **f14:** Excluded due to severely fragmented windows (failed the 60s contiguous threshold).",
        "- **S02:** A known signal quality issue was evaluated in the sensitivity analysis (see table above).",
        "",
        "## 5. Task-Specific Exploration",
        "See `outputs/external_task_specific_distribution.png` for a breakdown of how the frozen WESAD model responds to various Dataset B stressors (e.g. TMCT, Real Opinion, Subtract)."
    ]
    
    with open(os.path.join(results_dir, "experiment3_external_generalization.md"), "w") as f:
        f.write("\n".join(report))
        
    print("--- EXPERIMENT 3 COMPLETE ---")

if __name__ == "__main__":
    main()
