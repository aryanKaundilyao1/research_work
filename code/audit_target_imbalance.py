import os
import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score, f1_score, matthews_corrcoef, confusion_matrix, brier_score_loss

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import OUTPUT_DIR, REPORTS_DIR

def run_audit():
    # Load cached target windows and predictions
    Q1_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'q1_rebuild')
    
    # 1. Trace the 17 Baseline Windows
    print("\n--- 1. BASELINE TRACING ---")
    df_splits = pd.read_csv(os.path.join(REPORTS_DIR, 'q1_rebuild', 'BASELINE_SPLITS.csv'))
    print(df_splits[['Subject', 'Held-out baseline duration', 'Evaluation baseline windows', 'Stress windows']].head(10))
    
    non_zero_base = (df_splits['Evaluation baseline windows'] > 0).sum()
    zero_base = (df_splits['Evaluation baseline windows'] == 0).sum()
    total_base = df_splits['Evaluation baseline windows'].sum()
    total_stress = df_splits['Stress windows'].sum()
    
    print(f"Subjects with >=1 held-out baseline window: {non_zero_base}")
    print(f"Subjects with zero held-out baseline windows: {zero_base}")
    print(f"Total held-out baseline windows: {total_base}")
    print(f"Total stress windows: {total_stress}")

    # Create detailed accounting CSV
    df_accounting = df_splits.copy()
    df_accounting['Included in binary eval?'] = df_accounting.apply(
        lambda row: 'Yes' if (row['Evaluation baseline windows'] > 0 and row['Stress windows'] > 0) else 'No', axis=1
    )
    df_accounting['Reason if no eval'] = df_accounting.apply(
        lambda row: 'Insufficient baseline duration (< 180s)' if row['Evaluation baseline windows'] == 0 else '', axis=1
    )
    df_accounting.to_csv(os.path.join(REPORTS_DIR, 'q1_rebuild', 'BASELINE_EVALUATION_ACCOUNTING.csv'), index=False)
    
    # 2. Verify AUROC 0.739
    print("\n--- 2 & 4. WINDOW vs SUBJECT METRICS ---")
    
    df_feats = pd.read_pickle(os.path.join(Q1_OUTPUT_DIR, 'cache', 'df_b_feats_rel.pkl'))
    y_true = (df_feats['task'] != 'Baseline').astype(int)
    
    # Since we need y_prob, we should either load the pipeline or extract it from SUBJECT_LEVEL_METRICS if possible...
    # Actually, we don't have y_prob cached as a file. We can recreate it.
    from q1_feature_pipeline import RigorousSourceTargetPipeline
    df_w = pd.read_pickle(os.path.join(Q1_OUTPUT_DIR, 'cache', 'df_w_feats_rel.pkl'))
    
    X_s = df_w.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    y_s = (df_w['task'] != 'Baseline').astype(int)
    
    X_t = df_feats.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    
    pipeline = RigorousSourceTargetPipeline(k_best=20, clf_type='xgboost')
    pipeline.fit_source(X_s, y_s)
    y_prob = pipeline.predict_proba_target(X_t)
    y_pred = pipeline.predict_target(X_t)
    
    # Window Level
    win_auc = roc_auc_score(y_true, y_prob)
    win_pr = average_precision_score(y_true, y_prob)
    win_bal_acc = balanced_accuracy_score(y_true, y_pred)
    win_f1 = f1_score(y_true, y_pred)
    win_mcc = matthews_corrcoef(y_true, y_pred)
    
    print("WINDOW LEVEL:")
    print(f"AUROC: {win_auc:.3f}")
    print(f"PR-AUC: {win_pr:.3f}")
    print(f"Bal Acc: {win_bal_acc:.3f}")
    print(f"F1: {win_f1:.3f}")
    print(f"MCC: {win_mcc:.3f}")
    
    # 5. PR-AUC audit
    prevalence = np.mean(y_true)
    print(f"\n--- 5. PR-AUC AUDIT ---")
    print(f"Class prevalence (Stress): {prevalence:.3f}")
    print(f"No-skill PR-AUC baseline: {prevalence:.3f}")
    
    # 6. MCC Audit
    print(f"\n--- 6. MCC AUDIT ---")
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:\n", cm)
    
    # Subject Level Primary
    print(f"\n--- 3. FAIR EVALUATION / SUBJECT AWARE ---")
    # For fair subject evaluation, compute AUROC per subject, then macro average
    df = df_feats[['subject_id', 'task']].copy()
    df['y_true'] = y_true
    df['y_prob'] = y_prob
    
    subj_aucs = []
    for subj in df['subject_id'].unique():
        sdf = df[df['subject_id'] == subj]
        if len(sdf['y_true'].unique()) > 1:
            subj_aucs.append(roc_auc_score(sdf['y_true'], sdf['y_prob']))
            
    subj_aucs = np.array(subj_aucs)
    print(f"Subjects with BOTH classes: {len(subj_aucs)}")
    if len(subj_aucs) > 0:
        print(f"Macro Subject AUROC: {np.mean(subj_aucs):.3f}")
        print(f"Median: {np.median(subj_aucs):.3f}")
        
        # Bootstrap
        n_boot = 5000
        boot_means = [np.mean(np.random.choice(subj_aucs, size=len(subj_aucs), replace=True)) for _ in range(n_boot)]
        ci_lower = np.percentile(boot_means, 2.5)
        ci_upper = np.percentile(boot_means, 97.5)
        print(f"95% CI for Macro AUROC: [{ci_lower:.3f}, {ci_upper:.3f}]")
        
    # V1 vs V2
    print(f"\n--- 10. V1 vs V2 ---")
    # v1 subjects usually have 'S' prefix, v2 have 'f' prefix in target (Hongn dataset notation? Let's check IDs)
    for prefix, name in [('S', 'V1 (Stroop first)'), ('f', 'V2 (Subtract first)')]:
        v_df = df[df['subject_id'].astype(str).str.startswith(prefix)]
        if len(v_df) > 0 and len(v_df['y_true'].unique()) > 1:
            v_auc = roc_auc_score(v_df['y_true'], v_df['y_prob'])
            v_base = len(v_df[v_df['y_true'] == 0])
            v_stress = len(v_df[v_df['y_true'] == 1])
            print(f"{name}: N={len(v_df['subject_id'].unique())}, Base Win={v_base}, Stress Win={v_stress}, AUROC={v_auc:.3f}")
            
if __name__ == "__main__":
    run_audit()
