import numpy as np

def sliding_window(segments, window_size=60, step=30):
    """
    Generates non-overlapping (or overlapping) sliding windows from standardized segments.
    
    segments: list of dicts, where each dict has:
       'subject_id'
       'dataset'
       'task'
       'signals' -> dict of numpy arrays (e.g., {'EDA': array, ...})
       'fs' -> dict of sampling frequencies
       'start_time', 'end_time'
       
    window_size: in seconds
    step: in seconds
    """
    windows = []
    
    for seg in segments:
        # Determine the total duration of this segment based on the length of the signals
        # We can use EDA as the reference since it's present in both
        if 'EDA' not in seg['signals']:
            continue
            
        ref_sig = seg['signals']['EDA']
        ref_fs = seg['fs']['EDA']
        duration = len(ref_sig) / ref_fs
        
        # If the segment is shorter than the window size, we skip it
        if duration < window_size:
            continue
            
        # Calculate the number of windows
        num_windows = int(np.floor((duration - window_size) / step)) + 1
        
        for i in range(num_windows):
            start_sec = i * step
            end_sec = start_sec + window_size
            
            win_signals = {}
            for sig_name, sig_data in seg['signals'].items():
                fs = seg['fs'][sig_name]
                
                # Convert time to index
                start_idx = int(start_sec * fs)
                end_idx = int(end_sec * fs)
                
                win_signals[sig_name] = sig_data[start_idx:end_idx]
                
            windows.append({
                'subject_id': seg['subject_id'],
                'dataset': seg['dataset'],
                'task': seg['task'],
                'signals': win_signals,
                'fs': seg['fs'],
                'window_start_time': seg['start_time'] + start_sec if isinstance(seg['start_time'], (int, float)) else None, # for Dataset B this is a datetime, will handle if needed
                'window_end_time': seg['start_time'] + end_sec if isinstance(seg['start_time'], (int, float)) else None
            })
            
    return windows
