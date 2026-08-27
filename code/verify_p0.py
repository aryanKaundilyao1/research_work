import os
import sys
import numpy as np

# Add local path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loaders import load_all_wesad, load_all_dataset_b, WESAD_FS
from windowing import sliding_window

def main():
    report = []
    report.append("# P0 Data Loader and Windowing Verification Report\n")
    
    # Paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wesad_root = os.path.join(project_root, "datasets", "WESAD", "WESAD")
    dataset_b_root = os.path.join(project_root, "datasets", "Dataset_B", "wearable-device-dataset-from-induced-stress-and-structured-exercise-sessions-1.0.1")
    
    # ---------------- WESAD VERIFICATION ----------------
    report.append("## WESAD Verification")
    if os.path.exists(wesad_root):
        wesad_segments = load_all_wesad(wesad_root)
        
        subjects = list(set([s['subject_id'] for s in wesad_segments]))
        report.append(f"- **Subjects Loaded:** {len(subjects)} (Expected 15)")
        
        wesad_windows_60 = sliding_window(wesad_segments, window_size=60, step=30)
        
        report.append("\n### WESAD Subject Breakdown")
        
        total_baseline_duration = 0
        total_stress_duration = 0
        
        for subj in sorted(subjects):
            subj_segs = [s for s in wesad_segments if s['subject_id'] == subj]
            baseline_dur = sum([len(s['signals']['EDA']) / s['fs']['EDA'] for s in subj_segs if s['task'] == 'Baseline'])
            stress_dur = sum([len(s['signals']['EDA']) / s['fs']['EDA'] for s in subj_segs if s['task'] == 'Stress'])
            
            total_baseline_duration += baseline_dur
            total_stress_duration += stress_dur
            
            subj_windows = [w for w in wesad_windows_60 if w['subject_id'] == subj]
            
            report.append(f"- **{subj}:** Baseline: {baseline_dur/60:.2f}m, Stress: {stress_dur/60:.2f}m, Windows (60s, 30s step): {len(subj_windows)}")
            
        report.append(f"\n- **Total 60s windows:** {len(wesad_windows_60)}")
        report.append(f"- **Signal Sampling Rates:** {WESAD_FS}")
        
        # Missing value check
        missing = sum([np.isnan(w['signals']['EDA']).sum() for w in wesad_windows_60])
        report.append(f"- **Missing values in WESAD EDA windows:** {missing}")
        
    else:
        report.append("WESAD root not found.")
        wesad_windows_60 = []

    # ---------------- DATASET B VERIFICATION ----------------
    report.append("\n## Dataset B Verification")
    if os.path.exists(dataset_b_root):
        db_segments = load_all_dataset_b(dataset_b_root)
        
        subjects = list(set([s['subject_id'] for s in db_segments]))
        v1_count = sum(1 for s in subjects if s.startswith('S'))
        v2_count = sum(1 for s in subjects if s.startswith('f'))
        
        report.append(f"- **Subjects Loaded:** {len(subjects)} (V1: {v1_count}, V2: {v2_count})")
        
        tasks_found = list(set([s['task'] for s in db_segments]))
        report.append(f"- **Tasks Discovered:** {', '.join(tasks_found)}")
        
        db_windows_60 = sliding_window(db_segments, window_size=60, step=30)
        
        report.append("\n### Dataset B Subject Breakdown (Sample)")
        
        # Print a few to avoid huge report
        for subj in sorted(subjects)[:5]:
            subj_segs = [s for s in db_segments if s['subject_id'] == subj]
            subj_windows = [w for w in db_windows_60 if w['subject_id'] == subj]
            
            durations = []
            for s in subj_segs:
                if 'EDA' in s['signals']:
                    dur = len(s['signals']['EDA']) / s['fs']['EDA']
                    durations.append(f"{s['task']}: {dur/60:.2f}m")
            
            report.append(f"- **{subj}:** {', '.join(durations)} | Windows: {len(subj_windows)}")
            
        report.append(f"\n- **Total 60s windows:** {len(db_windows_60)}")
        if len(db_segments) > 0:
            report.append(f"- **Signal Sampling Rates:** {db_segments[0]['fs']}")
            
        constrained_subjects = [s for s in subjects if s in ['S02', 'f07', 'f14']]
        report.append(f"- **Constrained Subjects loaded:** {constrained_subjects}")
        
    else:
        report.append("Dataset B root not found.")
        db_windows_60 = []

    # ---------------- STRUCTURAL CONSISTENCY CHECK ----------------
    report.append("\n## Structural Consistency Check")
    all_windows = wesad_windows_60 + db_windows_60
    
    passed = True
    for w in all_windows:
        if 'subject_id' not in w or not w['subject_id']: passed = False
        if 'dataset' not in w or not w['dataset']: passed = False
        if 'task' not in w or not w['task']: passed = False
        if 'fs' not in w or not w['fs']: passed = False
        if 'EDA' not in w['signals']: passed = False
        
    report.append(f"- **All {len(all_windows)} windows have subject_id, dataset, task, fs, and EDA:** {'PASS' if passed else 'FAIL'}")
    
    # Save report
    report_text = "\n".join(report)
    out_path = os.path.join(project_root, "reports", "p0_verification_report.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with open(out_path, "w") as f:
        f.write(report_text)
        
    print(f"Report saved to {out_path}")


if __name__ == "__main__":
    main()
