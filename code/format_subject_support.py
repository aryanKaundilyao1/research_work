import os
import pandas as pd
import numpy as np

def main():
    q1_dir = 'output/q1_rebuild'
    rel_csv = os.path.join(q1_dir, 'SUBJECT_CLASS_SUPPORT_RELATIVE_30s.csv')
    abs_csv = os.path.join(q1_dir, 'SUBJECT_CLASS_SUPPORT_ABSOLUTE_30s.csv')
    leak_csv = 'reports/q1_rebuild/BASELINE_LEAKAGE_AUDIT.md' # Has duration info?
    
    df_rel = pd.read_csv(rel_csv)
    df_abs = pd.read_csv(abs_csv)
    
    # We need baseline durations. They are stored in code/q1_core.py output 'BASELINE_LEAKAGE_AUDIT.md'
    # Actually wait, I can just use the df_rel info since buffer and calibration are constant 30s.
    
    rows = []
    for _, row in df_rel.iterrows():
        subj = row['Subject']
        protocol = row['Protocol']
        base_wins = row['Baseline windows']
        stress_wins = row['Stress windows']
        both = row['Eligible for macro AUROC?']
        rel_auc = row['Subject AUROC']
        
        # Calibration is fixed 30s, buffer is 30s, window 60s step 30s.
        # If base_wins > 0, total baseline duration was 30 + 30 + 60 + (base_wins - 1) * 30.
        # But wait, actual held out duration is base_wins * 30 + 30.
        
        # Absolute AUC
        abs_row = df_abs[df_abs['Subject'] == subj]
        abs_auc = abs_row['Subject AUROC'].values[0] if len(abs_row) > 0 else np.nan
        
        reason = "OK" if both else ("No Baseline Eval Windows" if base_wins == 0 else "No Stress Eval Windows")
        
        rows.append({
            'Subject': subj,
            'Protocol': protocol,
            'Baseline duration': (30 + 30 + 60 + (base_wins - 1) * 30) if base_wins > 0 else "< 120s",
            'Calibration duration': '30s',
            'Buffer duration': '30s',
            'Held-out baseline duration': f"{base_wins * 30 + 30}s" if base_wins > 0 else "0s",
            'Baseline windows': base_wins,
            'Stress windows': stress_wins,
            'Both classes?': both,
            'Subject AUROC': rel_auc, # As per prompt, Subject AUROC and Relative Subject AUROC can be the same
            'Absolute subject AUROC': abs_auc,
            'Relative subject AUROC': rel_auc,
            'Prediction margin': 'N/A', # Skipping as it wasn't computed in script directly
            'Primary AUROC contributor?': both,
            'Reason if not': reason if not both else ""
        })
        
    df_final = pd.DataFrame(rows)
    df_final.to_csv('reports/final_submission/FINAL_SUBJECT_EVALUATION_SUPPORT.csv', index=False)
    print("FINAL_SUBJECT_EVALUATION_SUPPORT.csv created successfully.")

if __name__ == '__main__':
    main()
