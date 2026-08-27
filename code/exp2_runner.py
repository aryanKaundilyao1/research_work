import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import (roc_auc_score, average_precision_score, accuracy_score, 
                             balanced_accuracy_score, f1_score, precision_score, 
                             recall_score, confusion_matrix, roc_curve, precision_recall_curve)
from imblearn.over_sampling import SMOTE

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import (PROJECT_ROOT, WESAD_ROOT, WINDOW_SIZE, STEP_SIZE, 
                    RANDOM_SEED, K_BEST)
from data_loaders import load_all_wesad
from windowing import sliding_window
from features import build_feature_matrix
from pipeline import get_base_model
from metrics import aggregate_subject_predictions

def run_ablation_condition(df, allowed_modalities):
    feat_cols = [c for c in df.columns if c not in ['window_idx', 'subject_id', 'dataset', 'task', 'label']]
    
    X = df[feat_cols]
    y = df['label']
    groups = df['subject_id']
    
    logo = LeaveOneGroupOut()
    
    oof_y_true = []
    oof_y_prob = []
    oof_groups = []
    
    for fold, (train_idx, test_idx) in enumerate(logo.split(X, y, groups)):
        X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        X_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
        test_subject = groups.iloc[test_idx].values[0]
        
        # 1. Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 2. SelectKBest
        k = min(K_BEST, X_train_scaled.shape[1])
        selector = SelectKBest(f_classif, k=k)
        X_train_sel = selector.fit_transform(X_train_scaled, y_train)
        X_test_sel = selector.transform(X_test_scaled)
        
        # 3. SMOTE
        n_minority = min(np.sum(y_train == 0), np.sum(y_train == 1))
        k_neighbors = min(5, n_minority - 1)
        if k_neighbors > 0:
            sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=k_neighbors)
            X_train_res, y_train_res = sm.fit_resample(X_train_sel, y_train)
        else:
            X_train_res, y_train_res = X_train_sel, y_train
            
        # 4. XGBoost
        model = get_base_model()
        model.fit(X_train_res, y_train_res)
        
        preds = model.predict_proba(X_test_sel)[:, 1]
        
        oof_y_true.extend(y_test.values)
        oof_y_prob.extend(preds)
        oof_groups.extend([test_subject] * len(preds))
        
    return oof_y_true, oof_y_prob, oof_groups


def main():
    print("--- STARTING EXPERIMENT 2: MODALITY ABLATION ---")
    
    results_dir = os.path.join(PROJECT_ROOT, "reports", "experiment_2", "results")
    outputs_dir = os.path.join(PROJECT_ROOT, "reports", "experiment_2", "outputs")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    
    print("Loading WESAD...")
    w_segs = load_all_wesad(WESAD_ROOT)
    w_wins = sliding_window(w_segs, window_size=WINDOW_SIZE, step=STEP_SIZE)
    
    conditions = {
        "A. EDA only": ['EDA'],
        "B. BVP only": ['BVP'],
        "C. EDA + BVP": ['EDA', 'BVP'],
        "D. EDA + BVP + TEMP": ['EDA', 'BVP', 'TEMP'],
        "E. EDA + BVP + TEMP + ACC": ['EDA', 'BVP', 'TEMP', 'ACC']
    }
    
    results = []
    subject_results = []
    
    plt_roc = plt.figure(figsize=(8, 8))
    plt_pr = plt.figure(figsize=(8, 8))
    
    for condition_name, mods in conditions.items():
        print(f"Running condition: {condition_name} with {mods}")
        df_w = build_feature_matrix(w_wins, allowed_modalities=mods)
        df_w['label'] = df_w['task'].apply(lambda x: 0 if x == 'Baseline' else 1)
        
        oof_y_true, oof_y_prob, oof_groups = run_ablation_condition(df_w, mods)
        
        agg_true, agg_prob = aggregate_subject_predictions(oof_y_true, oof_y_prob, oof_groups)
        agg_pred = (agg_prob >= 0.5).astype(int)
        
        auc = roc_auc_score(agg_true, agg_prob)
        pr_auc = average_precision_score(agg_true, agg_prob)
        acc = accuracy_score(agg_true, agg_pred)
        bal_acc = balanced_accuracy_score(agg_true, agg_pred)
        f1 = f1_score(agg_true, agg_pred)
        prec = precision_score(agg_true, agg_pred)
        rec = recall_score(agg_true, agg_pred)
        
        tn, fp, fn, tp = confusion_matrix(agg_true, agg_pred, labels=[0, 1]).ravel()
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        
        results.append({
            'Condition': condition_name,
            'Modalities': "+".join(mods),
            'ROC-AUC': auc,
            'PR-AUC': pr_auc,
            'Balanced Accuracy': bal_acc,
            'F1': f1,
            'Sensitivity': rec,
            'Specificity': spec
        })
        
        # Subject level
        for subj in np.unique(oof_groups):
            idx = np.where(np.array(oof_groups) == subj)[0]
            s_true, s_prob = aggregate_subject_predictions(np.array(oof_y_true)[idx], np.array(oof_y_prob)[idx], [subj]*len(idx))
            
            try:
                s_auc = roc_auc_score(s_true, s_prob) if len(np.unique(s_true)) > 1 else np.nan
            except:
                s_auc = np.nan
                
            subject_results.append({
                'Condition': condition_name,
                'Subject': subj,
                'ROC-AUC': s_auc
            })
            
        # ROC Plot
        plt.figure(plt_roc.number)
        fpr, tpr, _ = roc_curve(agg_true, agg_prob)
        plt.plot(fpr, tpr, label=f'{condition_name} (AUC={auc:.3f})')
        
        # PR Plot
        plt.figure(plt_pr.number)
        precision, recall, _ = precision_recall_curve(agg_true, agg_prob)
        plt.plot(recall, precision, label=f'{condition_name} (PR={pr_auc:.3f})')

    df_res = pd.DataFrame(results)
    df_res.to_csv(os.path.join(results_dir, "experiment2_ablation_results.csv"), index=False)
    
    df_sub = pd.DataFrame(subject_results)
    
    # Finalize ROC Plot
    plt.figure(plt_roc.number)
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.title('Modality Ablation: Subject-Aggregated ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.savefig(os.path.join(outputs_dir, "ablation_roc_curve.png"))
    plt.close(plt_roc)
    
    # Finalize PR Plot
    plt.figure(plt_pr.number)
    plt.title('Modality Ablation: Subject-Aggregated PR Curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.savefig(os.path.join(outputs_dir, "ablation_pr_curve.png"))
    plt.close(plt_pr)
    
    # Per-Subject Comparison Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_sub, x='Subject', y='ROC-AUC', hue='Condition')
    plt.title('Per-Subject ROC-AUC Across Modalities')
    plt.axhline(0.5, color='red', linestyle='--')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "ablation_subject_comparison.png"))
    plt.close()
    
    # Write Markdown Report
    report = [
        "# Experiment 2: Modality Ablation",
        "",
        "## 1. Objective",
        "Determine the impact of specific sensor modalities on the model's ability to discriminate Baseline vs Stress.",
        "",
        "## 2. Experimental Constraints",
        "- WESAD Dataset ONLY.",
        "- Identical LOOCV architecture, parameter settings, and subject-aggregation logic from Experiment 1.",
        "- No hyperparameter tuning or modality-specific adjustments.",
        "",
        "## 3. Modality Comparison Table",
        df_res.to_markdown(index=False),
        "",
        "## 4. Scientific Interpretation",
        "The highest performing modality combinations reveal whether multimodal fusion genuinely improves the model's robustness or if the classification is predominantly driven by a single highly-sensitive signal (e.g., EDA).",
        "See `figures/experiment_2/` for visual ROC, PR, and per-subject comparisons."
    ]
    
    with open(os.path.join(results_dir, "experiment2_report.md"), "w") as f:
        f.write("\n".join(report))
        
    print("--- EXPERIMENT 2 COMPLETE ---")

if __name__ == "__main__":
    main()
