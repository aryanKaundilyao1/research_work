import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import WESAD_ROOT, WINDOW_SIZE, STEP_SIZE
from data_loaders import load_all_wesad
from windowing import sliding_window
from features import build_feature_matrix
from exp2_runner import run_ablation_condition
from metrics import aggregate_subject_predictions
from sklearn.metrics import roc_auc_score

def main():
    print("Extracting Subject-Level Results for Exp 2 Audit...")
    
    exp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports", "experiment_2", "results")
    
    w_segs = load_all_wesad(WESAD_ROOT)
    w_wins = sliding_window(w_segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
    
    conditions = {
        "EDA": ['EDA'],
        "BVP": ['BVP'],
        "EDA_BVP": ['EDA', 'BVP'],
        "EDA_BVP_TEMP": ['EDA', 'BVP', 'TEMP'],
        "FULL": ['EDA', 'BVP', 'TEMP', 'ACC']
    }
    
    subject_aucs = {subj: {} for subj in ['S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S13', 'S14', 'S15', 'S16', 'S17']}
    
    for cond_name, mods in conditions.items():
        print(f"Re-extracting {cond_name} deterministically...")
        df_w = build_feature_matrix(w_wins, allowed_modalities=mods)
        df_w['label'] = df_w['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
        
        oof_y_true, oof_y_prob, oof_groups = run_ablation_condition(df_w, mods)
        
        for subj in np.unique(oof_groups):
            idx = np.where(np.array(oof_groups) == subj)[0]
            s_true, s_prob = aggregate_subject_predictions(np.array(oof_y_true)[idx], np.array(oof_y_prob)[idx], [subj]*len(idx))
            
            try:
                s_auc = roc_auc_score(s_true, s_prob) if len(np.unique(s_true)) > 1 else np.nan
            except:
                s_auc = np.nan
            subject_aucs[subj][cond_name] = s_auc
            
    # Build dataframe
    df_sub = pd.DataFrame.from_dict(subject_aucs, orient='index')
    df_sub.index.name = 'Subject'
    df_sub.reset_index(inplace=True)
    
    csv_path = os.path.join(exp_dir, "experiment2_subject_results.csv")
    df_sub.to_csv(csv_path, index=False)
    print(f"Saved {csv_path}")
    
    # Paired Performance Differences & Statistical Tests
    print("\n--- PAIRED DIFFERENCES (Subject-Level AUC) ---")
    
    comparisons = [
        ("FULL", "BVP"),
        ("FULL", "EDA"),
        ("FULL", "EDA_BVP"),
        ("FULL", "EDA_BVP_TEMP")
    ]
    
    for m1, m2 in comparisons:
        diffs = df_sub[m1] - df_sub[m2]
        mean_diff = diffs.mean()
        
        # Wilcoxon signed-rank test
        # Note: If differences are exactly zero for all, wilcoxon raises ValueError
        try:
            stat, p_val = wilcoxon(df_sub[m1], df_sub[m2], zero_method='zsplit')
        except ValueError:
            p_val = 1.0
            
        print(f"{m1} vs {m2}: Mean Diff = {mean_diff:+.3f} | p-value = {p_val:.4f}")

if __name__ == "__main__":
    main()
