import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import PROJECT_ROOT, WINDOW_SIZE, STEP_SIZE

def apply_baseline_relative_transform(segments, baseline_duration_sec=None):
    """
    Applies subject-specific baseline normalization to raw signals.
    Optionally restricts the baseline to the FIRST `baseline_duration_sec` seconds.
    """
    transformed = []
    
    # Group by subject
    subjects = list(set([s['subject_id'] for s in segments]))
    
    for subj in subjects:
        subj_segs = [s for s in segments if s['subject_id'] == subj]
        
        # 1. Identify baseline segments for this subject
        baseline_segs = [s for s in subj_segs if s['task'] == 'Baseline']
        if not baseline_segs:
            transformed.extend(subj_segs)
            continue
            
        # 2. Calculate baseline mean & std per channel
        baseline_stats = {}
        for ch in ['EDA', 'BVP', 'TEMP']:
            all_ch_data = []
            for bs in baseline_segs:
                if ch in bs['signals']:
                    all_ch_data.append(bs['signals'][ch])
                    
            if all_ch_data:
                concat_data = np.concatenate(all_ch_data)
                
                # Apply duration limit if specified
                if baseline_duration_sec is not None:
                    # Dataset B Hz approximations based on Emaptica E4 or similar WESAD devices:
                    # EDA=4Hz, BVP=64Hz, TEMP=4Hz. 
                    hz = 64 if ch == 'BVP' else 4
                    max_samples = hz * baseline_duration_sec
                    concat_data = concat_data[:max_samples]
                    
                m = np.mean(concat_data)
                s = np.std(concat_data)
                if s == 0:
                    s = 1.0
                baseline_stats[ch] = (m, s)
                
        # 3. Transform ALL segments for this subject
        for seg in subj_segs:
            new_seg = seg.copy()
            new_seg['signals'] = {}
            for ch, data in seg['signals'].items():
                if ch in baseline_stats:
                    m, s = baseline_stats[ch]
                    new_seg['signals'][ch] = (np.array(data) - m) / s
                else:
                    new_seg['signals'][ch] = data 
            transformed.append(new_seg)
            
    return transformed
