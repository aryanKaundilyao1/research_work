import os
import sys
import numpy as np
import pandas as pd
import shap

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import WESAD_ROOT, DATASET_B_ROOT, MODALITIES, WINDOW_SIZE, STEP_SIZE
from data_loaders import load_all_wesad, load_all_dataset_b
from windowing import sliding_window
from features import build_feature_matrix
from pipeline import run_nested_cv, train_final_model, predict_external
from metrics import calculate_metrics

def prepare_data(modalities=MODALITIES):
    """Loads datasets, extracts windows, and builds feature matrices for both datasets."""
    print(f"Loading data for modalities: {modalities}")
    w_segs = load_all_wesad(WESAD_ROOT)
    db_segs = load_all_dataset_b(DATASET_B_ROOT)
    
    # Exclude constrained subjects here (e.g., f07)
    db_segs = [s for s in db_segs if s['subject_id'] != 'f07']
    
    w_wins = sliding_window(w_segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
    db_wins = sliding_window(db_segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
    
    df_w = build_feature_matrix(w_wins, allowed_modalities=modalities)
    df_db = build_feature_matrix(db_wins, allowed_modalities=modalities)
    
    # Binary labeling
    df_w['label'] = df_w['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
    df_db['label'] = df_db['task'].apply(lambda x: 0 if 'Baseline' in x or 'Rest' in x else 1)
    
    return df_w, df_db

def exp1_internal_validation(df_w):
    """Experiment 1: WESAD Internal LOSO-CV"""
    print("\n--- EXPERIMENT 1: Internal Validation (LOSO-CV) ---")
    feat_cols = [c for c in df_w.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
    
    X = df_w[feat_cols]
    y = df_w['label']
    groups = df_w['subject_id']
    
    oof_preds, fold_models = run_nested_cv(X, y, groups)
    metrics = calculate_metrics(y, oof_preds, groups=groups)
    print(f"Internal Validation AUC: {metrics['roc_auc']:.3f}")
    return metrics, oof_preds

def exp2_ablation():
    """Experiment 2: Modality Ablation"""
    print("\n--- EXPERIMENT 2: Ablation Study ---")
    subsets = [['EDA'], ['BVP'], ['TEMP'], ['ACC'], ['EDA', 'BVP'], MODALITIES]
    results = {}
    
    for subset in subsets:
        df_w, _ = prepare_data(modalities=subset)
        feat_cols = [c for c in df_w.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
        X = df_w[feat_cols]
        y = df_w['label']
        groups = df_w['subject_id']
        
        oof_preds, _ = run_nested_cv(X, y, groups)
        metrics = calculate_metrics(y, oof_preds, groups=groups)
        results[", ".join(subset)] = metrics['roc_auc']
        print(f"Modality {subset} -> AUC: {metrics['roc_auc']:.3f}")
        
    return results

def exp3_external_validation(df_w, df_db):
    """Experiment 3: Cross-Dataset Generalization"""
    print("\n--- EXPERIMENT 3: Cross-Dataset External Validation ---")
    feat_cols = [c for c in df_w.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
    
    X_w = df_w[feat_cols]
    y_w = df_w['label']
    
    X_db = df_db[feat_cols]
    y_db = df_db['label']
    groups_db = df_db['subject_id']
    
    frozen_pipeline = train_final_model(X_w, y_w)
    db_preds = predict_external(frozen_pipeline, X_db)
    
    metrics = calculate_metrics(y_db, db_preds, groups=groups_db)
    print(f"External Validation AUC: {metrics['roc_auc']:.3f}")
    
    # Save predictions into df for task analysis
    df_db_results = df_db.copy()
    df_db_results['pred_prob'] = db_preds
    return metrics, frozen_pipeline, df_db_results

def exp4_task_specific_analysis(df_db_results):
    """Experiment 4: Dataset B Task-Specific Predictions"""
    print("\n--- EXPERIMENT 4: Task-Specific Analysis ---")
    # Group by subject and task to find mean probability per subject per task
    task_agg = df_db_results.groupby(['subject_id', 'task'])['pred_prob'].mean().reset_index()
    
    for task in task_agg['task'].unique():
        avg_prob = task_agg[task_agg['task'] == task]['pred_prob'].mean()
        print(f"Task: {task:20s} | Avg Predicted Stress Probability: {avg_prob:.3f}")

def exp5_temporal_decay(df_w, oof_preds):
    """Experiment 5: WESAD Temporal Analysis"""
    print("\n--- EXPERIMENT 5: Temporal Decay ---")
    df_w['pred_prob'] = oof_preds
    
    df_stress = df_w[df_w['task'] == 'Stress'].copy()
    # Normalize window indices per subject to 0-1 for early/mid/late splitting
    df_stress['rank'] = df_stress.groupby('subject_id')['window_idx'].rank(pct=True)
    
    df_stress['phase'] = pd.cut(df_stress['rank'], bins=[0, 0.33, 0.66, 1.0], labels=['Early', 'Middle', 'Late'])
    
    phase_agg = df_stress.groupby(['subject_id', 'phase'])['pred_prob'].mean().reset_index()
    for phase in ['Early', 'Middle', 'Late']:
        avg_prob = phase_agg[phase_agg['phase'] == phase]['pred_prob'].mean()
        print(f"WESAD {phase} Stress | Avg Predicted Probability: {avg_prob:.3f}")

def exp6_shap_interpretation(frozen_pipeline, df_w, df_db):
    """Experiment 6: SHAP Values"""
    print("\n--- EXPERIMENT 6: SHAP Interpretation ---")
    model = frozen_pipeline['model']
    scaler = frozen_pipeline['scaler']
    selector = frozen_pipeline['selector']
    
    feat_cols = [c for c in df_w.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
    selected_features = np.array(feat_cols)[selector.get_support()]
    
    # We transform the datasets
    X_w_sel = selector.transform(scaler.transform(df_w[feat_cols]))
    X_db_sel = selector.transform(scaler.transform(df_db[feat_cols]))
    
    explainer = shap.TreeExplainer(model)
    shap_w = explainer.shap_values(X_w_sel)
    shap_db = explainer.shap_values(X_db_sel)
    
    print("SHAP explainer successfully built. Top feature indices can be extracted.")
    return explainer, shap_w, shap_db, selected_features

def run_all_experiments():
    """Main orchestrator for P2 experiments (Do not run yet)."""
    pass

if __name__ == "__main__":
    print("Experiments skeleton loaded. Execute specific functions to run.")
