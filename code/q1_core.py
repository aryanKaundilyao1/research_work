import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import REPORTS_DIR, OUTPUT_DIR, WINDOW_SIZE, STEP_SIZE

def apply_strict_baseline_relative_transform(segments, calib_duration_sec=30, buffer_sec=30, norm_type='zscore'):
    """
    Applies strict baseline normalization, ensuring chronological separation.
    Extracts calibration stats from [0, calib_duration_sec] of the Baseline task.
    Leaves a buffer of [calib_duration_sec, calib_duration_sec + buffer_sec] unused.
    Evaluates only on Baseline data AFTER calib_duration_sec + buffer_sec, and Stress tasks.
    """
    transformed = []
    audit_rows = []
    
    subjects = sorted(list(set([s['subject_id'] for s in segments])))
    
    for subj in subjects:
        subj_segs = [s for s in segments if s['subject_id'] == subj]
        
        baseline_segs = [s for s in subj_segs if s['task'] == 'Baseline']
        if not baseline_segs:
            continue
            
        bs = baseline_segs[0] 
        baseline_stats = {}
        
        calib_start_time = bs['start_time']
        if isinstance(calib_start_time, (int, float)):
            calib_end_time = calib_start_time + calib_duration_sec
            eval_start_time = calib_end_time + buffer_sec
        else:
            calib_end_time = calib_start_time + timedelta(seconds=calib_duration_sec)
            eval_start_time = calib_end_time + timedelta(seconds=buffer_sec)
            
        total_dur_sec = 0
        
        for ch in ['EDA', 'BVP', 'TEMP', 'ACC']:
            if ch in bs['signals']:
                sig = bs['signals'][ch]
                fs = bs['fs'][ch]
                
                total_dur_sec = len(sig) / fs
                
                calib_samples = int(calib_duration_sec * fs)
                if calib_samples > len(sig):
                    calib_samples = len(sig)
                    
                calib_data = sig[:calib_samples]
                
                if norm_type == 'zscore':
                    m = np.mean(calib_data, axis=0)
                    s = np.std(calib_data, axis=0)
                    s = np.where(s == 0, 1.0, s)
                    baseline_stats[ch] = (m, s)
                elif norm_type == 'mad':
                    m = np.median(calib_data, axis=0)
                    mad = np.median(np.abs(calib_data - m), axis=0)
                    mad = np.where(mad == 0, 1.0, mad)
                    baseline_stats[ch] = (m, mad)
                elif norm_type == 'mean_center':
                    m = np.mean(calib_data, axis=0)
                    baseline_stats[ch] = (m, 1.0)
                elif norm_type == 'minmax':
                    min_v = np.min(calib_data, axis=0)
                    max_v = np.max(calib_data, axis=0)
                    range_v = max_v - min_v
                    range_v = np.where(range_v == 0, 1.0, range_v)
                    baseline_stats[ch] = (min_v, range_v)
                elif norm_type == 'median_iqr':
                    m = np.median(calib_data, axis=0)
                    q75, q25 = np.percentile(calib_data, [75, 25], axis=0)
                    iqr = q75 - q25
                    iqr = np.where(iqr == 0, 1.0, iqr)
                    baseline_stats[ch] = (m, iqr)
                else:
                    baseline_stats[ch] = (0.0, 1.0)
                    
        held_out_dur = max(0, total_dur_sec - calib_duration_sec - buffer_sec)
        
        audit_rows.append({
            'Subject': subj,
            'Baseline_Duration': total_dur_sec,
            'Calibration_Start': calib_start_time,
            'Calibration_End': calib_end_time,
            'Buffer_End': eval_start_time,
            'First_Eval_Baseline': eval_start_time,
            'HeldOut_Baseline_Dur': held_out_dur,
        })
        
        for seg in subj_segs:
            new_seg = seg.copy()
            new_seg['signals'] = {}
            
            if seg['task'] == 'Baseline':
                if held_out_dur <= 0:
                    continue
                    
                new_seg['start_time'] = eval_start_time
                for ch, data in seg['signals'].items():
                    fs = seg['fs'][ch]
                    start_idx = int((calib_duration_sec + buffer_sec) * fs)
                    if start_idx >= len(data):
                        continue
                    sliced_data = data[start_idx:]
                    if ch in baseline_stats:
                        loc, scale = baseline_stats[ch]
                        new_seg['signals'][ch] = (sliced_data - loc) / scale
                    else:
                        new_seg['signals'][ch] = sliced_data
                transformed.append(new_seg)
            else:
                for ch, data in seg['signals'].items():
                    if ch in baseline_stats:
                        loc, scale = baseline_stats[ch]
                        new_seg['signals'][ch] = (data - loc) / scale
                    else:
                        new_seg['signals'][ch] = data
                transformed.append(new_seg)
                
    return transformed, audit_rows

def audit_leakage(windows, audit_rows, output_dir):
    df_audit = pd.DataFrame(audit_rows)
    win_counts = []
    
    for _, row in df_audit.iterrows():
        subj = row['Subject']
        subj_wins = [w for w in windows if w['subject_id'] == subj]
        eval_base_wins = len([w for w in subj_wins if w['task'] == 'Baseline'])
        stress_wins = len([w for w in subj_wins if w['task'] != 'Baseline'])
        
        raw_overlap_count = 0
        buffer_end = row['Buffer_End']
        
        for w in subj_wins:
            if w['task'] == 'Baseline':
                w_start = w['window_start_time']
                if w_start < buffer_end:
                    raw_overlap_count += 1
                    
        win_counts.append({
            'Subject': subj,
            'Baseline duration': row['Baseline_Duration'],
            'Calibration start': row['Calibration_Start'],
            'Calibration end': row['Calibration_End'],
            'Buffer end': row['Buffer_End'],
            'First evaluation window start': row['First_Eval_Baseline'],
            'Held-out baseline duration': row['HeldOut_Baseline_Dur'],
            'Held-out baseline windows': eval_base_wins,
            'Stress windows': stress_wins,
            'Raw overlap count': raw_overlap_count,
            'PASS/FAIL': 'FAIL' if raw_overlap_count > 0 else 'PASS'
        })
        
    df_res = pd.DataFrame(win_counts)
    df_res.to_csv(os.path.join(output_dir, 'BASELINE_SPLITS.csv'), index=False)
    
    with open(os.path.join(output_dir, 'BASELINE_LEAKAGE_AUDIT.md'), 'w') as f:
        f.write("# Baseline Calibration Leakage Audit\n\n")
        f.write(f"Total Subjects Audited: {len(df_res)}\n")
        f.write(f"Subjects Failed: {(df_res['Raw overlap count'] > 0).sum()}\n\n")
        f.write(df_res.to_markdown())
        
    return df_res
