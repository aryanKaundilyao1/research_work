import numpy as np
import pandas as pd
from scipy import stats, signal as sp_signal
from statsmodels.tsa.stattools import acf, pacf

def extract_features(seg, prefix=""):
    """
    Extracts exactly 39 features per signal array.
    """
    seg = np.array(seg, dtype=float)
    seg = seg[~np.isnan(seg)]

    if len(seg) < 10:
        # Fallback if window is mostly NaNs or severely broken
        return {f"{prefix}feat_{i}": 0 for i in range(39)}

    feats = {}

    # --- Basic statistics (10 features) ---
    mean_val  = np.mean(seg)
    std_val   = np.std(seg) + 1e-8
    rms_val   = np.sqrt(np.mean(seg**2))
    peak_val  = np.max(np.abs(seg))
    mean_abs  = np.mean(np.abs(seg)) + 1e-8
    mean_sqrt = np.mean(np.sqrt(np.abs(seg))) + 1e-8

    feats[f"{prefix}mean"]      = mean_val
    feats[f"{prefix}std"]       = std_val
    feats[f"{prefix}rms"]       = rms_val
    feats[f"{prefix}median"]    = np.median(seg)
    feats[f"{prefix}min"]       = np.min(seg)
    feats[f"{prefix}max"]       = np.max(seg)
    feats[f"{prefix}q1"]        = np.percentile(seg, 25)
    feats[f"{prefix}q3"]        = np.percentile(seg, 75)
    feats[f"{prefix}skewness"]  = stats.skew(seg)
    feats[f"{prefix}kurtosis"]  = stats.kurtosis(seg)

    # --- Shape features (7 features) ---
    feats[f"{prefix}peak_val"]        = peak_val
    feats[f"{prefix}crest_factor"]    = peak_val / (rms_val + 1e-8)
    feats[f"{prefix}impulse_factor"]  = peak_val / mean_abs
    feats[f"{prefix}clearance_factor"]= peak_val / (mean_sqrt ** 2)
    feats[f"{prefix}shape_factor"]    = rms_val / mean_abs
    feats[f"{prefix}neg_count"]       = np.sum(seg < 0)
    feats[f"{prefix}pos_count"]       = np.sum(seg > 0)

    # --- Time series features (2 features) ---
    try:
        acf_vals  = acf(seg, nlags=1, fft=True)
        pacf_vals = pacf(seg, nlags=1)
        feats[f"{prefix}acf1"]  = acf_vals[1]
        feats[f"{prefix}pacf1"] = pacf_vals[1]
    except:
        feats[f"{prefix}acf1"]  = 0
        feats[f"{prefix}pacf1"] = 0

    # --- Spectral features (20 features) ---
    try:
        nperseg = min(len(seg), 64)
        _, psd = sp_signal.welch(seg, nperseg=nperseg)
        psd_20 = np.interp(np.linspace(0, 1, 20), np.linspace(0, 1, len(psd)), psd)
        for i, val in enumerate(psd_20):
            feats[f"{prefix}psd_{i}"] = val
    except:
        for i in range(20):
            feats[f"{prefix}psd_{i}"] = 0

    return feats

def extract_window_features(window, allowed_modalities=None):
    """
    Extracts features for a single sliding window dict.
    Optionally restricts to allowed_modalities (e.g., ['EDA', 'BVP'] for ablation).
    """
    row = {}
    for sig_name, sig_data in window['signals'].items():
        if allowed_modalities and sig_name not in allowed_modalities:
            continue
            
        if sig_name == 'ACC':
            # ACC is always 3-axis
            if sig_data.ndim > 1 and sig_data.shape[1] >= 3:
                for i, axis in enumerate(['X', 'Y', 'Z']):
                    feats = extract_features(sig_data[:, i], prefix=f"ACC_{axis}_")
                    row.update(feats)
            else:
                # Fallback if structure is malformed
                for axis in ['X', 'Y', 'Z']:
                    feats = extract_features([0], prefix=f"ACC_{axis}_")
                    row.update(feats)
        else:
            feats = extract_features(sig_data, prefix=f"{sig_name}_")
            row.update(feats)
    return row

def build_feature_matrix(windows, allowed_modalities=None):
    """
    Iterates over all windows and builds a pandas DataFrame with features and metadata.
    """
    rows = []
    for i, w in enumerate(windows):
        feats = extract_window_features(w, allowed_modalities)
        meta = {
            'window_idx': i,
            'subject_id': w['subject_id'],
            'dataset': w['dataset'],
            'task': w['task']
        }
        meta.update(feats)
        rows.append(meta)
        
    df = pd.DataFrame(rows)
    df.fillna(0, inplace=True)
    return df
