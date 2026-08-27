import os
import glob
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

WESAD_FS = {'EDA': 4, 'TEMP': 4, 'BVP': 64, 'ACC': 32}
LABEL_FS = 700

def load_wesad_subject(filepath):
    """
    Load a single WESAD subject from a .pkl file.
    Extracts wrist signals and Baseline (1) / Stress (2) segments.
    """
    subject_id = os.path.basename(filepath).split('.')[0]
    
    with open(filepath, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
        
    labels = data['label'].flatten()
    signals = data['signal']['wrist']
    
    # Find contiguous blocks of label 1 (Baseline) and label 2 (Stress)
    # We will compute the start and end index in the 700Hz label array
    segments = []
    
    # Create mask for allowed labels
    allowed = (labels == 1) | (labels == 2)
    
    # Find boundaries
    diffs = np.diff(allowed.astype(int))
    starts = np.where(diffs == 1)[0] + 1
    ends = np.where(diffs == -1)[0] + 1
    
    if allowed[0]:
        starts = np.insert(starts, 0, 0)
    if allowed[-1]:
        ends = np.append(ends, len(labels))
        
    for start, end in zip(starts, ends):
        block_label = labels[start]
        task_name = "Baseline" if block_label == 1 else "Stress"
        
        # We need to slice each modality using proportional indices
        seg_signals = {}
        for sig_name, fs in WESAD_FS.items():
            sig_data = signals[sig_name]
            # Convert 700Hz index to target fs index
            start_idx = int(start * fs / LABEL_FS)
            end_idx = int(end * fs / LABEL_FS)
            
            # Bound check
            end_idx = min(end_idx, len(sig_data))
            
            seg_signals[sig_name] = sig_data[start_idx:end_idx]
            
        segments.append({
            'subject_id': subject_id,
            'dataset': 'WESAD',
            'task': task_name,
            'signals': seg_signals,
            'fs': WESAD_FS,
            'start_time': start / LABEL_FS,  # seconds from start
            'end_time': end / LABEL_FS
        })
        
    return segments


def load_dataset_b_subject(subject_dir, subject_id, tasks_order):
    """
    Load a single Dataset B subject.
    tasks_order defines the task names corresponding to each segment.
    """
    segments = []
    tags_path = os.path.join(subject_dir, "tags.csv")
    
    if not os.path.exists(tags_path):
        return segments
        
    try:
        tags = pd.read_csv(tags_path, header=None, names=['timestamp'])
        tags['timestamp'] = pd.to_datetime(tags['timestamp'])
    except Exception:
        return segments

    # S02, f07, f14 constraints based on data_constraints.txt
    if subject_id == 'f07':
        # BVP and TEMP are invalid, we will skip this subject for full multimodal analysis 
        # or load what we can. We'll load what we can.
        pass

    # Load E4 CSVs
    signals_raw = {}
    fs_dict = {}
    start_times = {}
    
    for sig_name in ['EDA', 'TEMP', 'BVP', 'ACC']:
        path = os.path.join(subject_dir, f"{sig_name}.csv")
        if not os.path.exists(path):
            continue
            
        df = pd.read_csv(path, header=None)
        start_time_str = df.iloc[0, 0]
        try:
            # First row is datetime string for this dataset
            start_time = pd.to_datetime(start_time_str)
        except ValueError:
            # Just in case it's a standard unix timestamp
            start_time = pd.to_datetime(float(start_time_str), unit='s')
            
        fs = float(df.iloc[1, 0])
        data = df.iloc[2:].values.astype(float)
        
        signals_raw[sig_name] = data
        fs_dict[sig_name] = fs
        start_times[sig_name] = start_time

    # We assume all signals start at approximately the same time, but we'll use each signal's own start_time
    if len(tags) - 1 > len(tasks_order):
        # We have more tags than tasks, truncate tasks
        task_names = tasks_order[:len(tags)-1]
    else:
        task_names = tasks_order
        
    for i in range(len(task_names)):
        if i+1 >= len(tags):
            break
            
        t_start = tags.iloc[i]['timestamp']
        t_end = tags.iloc[i+1]['timestamp']
        task = task_names[i]
        
        seg_signals = {}
        for sig_name, data in signals_raw.items():
            fs = fs_dict[sig_name]
            sig_start = start_times[sig_name]
            
            # calculate indices
            start_idx = int((t_start - sig_start).total_seconds() * fs)
            end_idx = int((t_end - sig_start).total_seconds() * fs)
            
            start_idx = max(0, start_idx)
            end_idx = min(len(data), end_idx)
            
            seg_signals[sig_name] = data[start_idx:end_idx]
            
        segments.append({
            'subject_id': subject_id,
            'dataset': 'Dataset_B',
            'task': task,
            'signals': seg_signals,
            'fs': fs_dict,
            'start_time': t_start,
            'end_time': t_end
        })
        
    return segments

def load_all_wesad(root_dir):
    all_segments = []
    pkl_files = glob.glob(os.path.join(root_dir, "S*", "S*.pkl"))
    for pkl in pkl_files:
        all_segments.extend(load_wesad_subject(pkl))
    return all_segments

def load_all_dataset_b(root_dir):
    # Determine task orders based on V1 / V2
    # V1: Baseline, Stroop, First Rest, TMCT, Second Rest, Real Opinion, Opposite Opinion, Subtract
    # V2: Baseline, Subtract, First Rest, TMCT, Second Rest, Real Opinion, Opposite Opinion, Stroop
    v1_tasks = ["Baseline", "Stroop", "First Rest", "TMCT", "Second Rest", "Real Opinion", "Opposite Opinion", "Subtract"]
    v2_tasks = ["Baseline", "Subtract", "First Rest", "TMCT", "Second Rest", "Real Opinion", "Opposite Opinion", "Stroop"]
    
    # Read Stress_Level to map subjects to versions
    v1_df = pd.read_csv(os.path.join(root_dir, "Stress_Level_v1.csv"), index_col=0)
    v2_df = pd.read_csv(os.path.join(root_dir, "Stress_Level_v2.csv"), index_col=0)
    
    v1_subjects = v1_df.index.tolist()
    v2_subjects = v2_df.index.tolist()
    
    stress_dir = os.path.join(root_dir, "Wearable_Dataset", "STRESS")
    subjects = os.listdir(stress_dir)
    
    all_segments = []
    for subj in subjects:
        subj_dir = os.path.join(stress_dir, subj)
        if not os.path.isdir(subj_dir):
            continue
            
        if subj in v1_subjects:
            tasks_order = v1_tasks
        elif subj in v2_subjects:
            tasks_order = v2_tasks
        else:
            # Default to V1 if unknown (e.g. some subjects might not have subjective ratings)
            tasks_order = v1_tasks
            
        segs = load_dataset_b_subject(subj_dir, subj, tasks_order)
        all_segments.extend(segs)
        
    return all_segments
