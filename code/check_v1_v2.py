import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import REPORTS_DIR

def analyze_v1_v2():
    df_feats = pd.read_pickle(os.path.join(REPORTS_DIR, '..', 'q1_rebuild', 'cache', 'df_b_feats_rel.pkl'))
    y_true = (df_feats['task'] != 'Baseline').astype(int)
    
    from q1_feature_pipeline import RigorousSourceTargetPipeline
    df_w = pd.read_pickle(os.path.join(REPORTS_DIR, '..', 'q1_rebuild', 'cache', 'df_w_feats_rel.pkl'))
    
    X_s = df_w.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    y_s = (df_w['task'] != 'Baseline').astype(int)
    
    X_t = df_feats.drop(columns=['window_idx', 'subject_id', 'task', 'dataset'])
    
    pipeline = RigorousSourceTargetPipeline(k_best=20, clf_type='xgboost')
    pipeline.fit_source(X_s, y_s)
    y_prob = pipeline.predict_proba_target(X_t)
    
    df = df_feats[['subject_id', 'task']].copy()
    df['y_true'] = y_true
    df['y_prob'] = y_prob
    
    print("\n--- 10. V1 vs V2 Detailed ---")
    for prefix, name in [('S', 'V1 (Stroop first)'), ('f', 'V2 (Subtract first)')]:
        v_df = df[df['subject_id'].astype(str).str.startswith(prefix)]
        v_base = len(v_df[v_df['y_true'] == 0])
        v_stress = len(v_df[v_df['y_true'] == 1])
        
        if len(v_df) > 0 and len(v_df['y_true'].unique()) > 1:
            v_auc = roc_auc_score(v_df['y_true'], v_df['y_prob'])
        else:
            v_auc = np.nan
            
        print(f"{name}: N={len(v_df['subject_id'].unique())}, Base Win={v_base}, Stress Win={v_stress}, AUROC={v_auc}")

if __name__ == "__main__":
    analyze_v1_v2()
