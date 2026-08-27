import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, balanced_accuracy_score, accuracy_score, confusion_matrix

def aggregate_subject_predictions(y_true, y_prob, groups):
    """
    Because windows from the same subject are highly correlated, evaluating metrics
    at the raw window level violates independence assumptions and falsely tightens CIs.
    This aggregates window-level predicted probabilities to the subject level per condition.
    
    Since we only have binary labels (0=Baseline, 1=Stress), for a given subject we might
    have baseline windows and stress windows. We should aggregate the probabilities for 
    the true Baseline windows and true Stress windows separately per subject.
    """
    df = pd.DataFrame({'y_true': y_true, 'y_prob': y_prob, 'subject': groups})
    
    # We want to find the subject's average predicted probability when they were in Baseline (y_true=0)
    # and when they were in Stress (y_true=1).
    agg_df = df.groupby(['subject', 'y_true'])['y_prob'].mean().reset_index()
    
    agg_y_true = agg_df['y_true'].values
    agg_y_prob = agg_df['y_prob'].values
    
    return agg_y_true, agg_y_prob

def calculate_metrics(y_true, y_prob, groups=None):
    """
    Calculates the required metrics. If groups is provided, applies subject-level aggregation first.
    """
    if groups is not None:
        y_true, y_prob = aggregate_subject_predictions(y_true, y_prob, groups)
        
    y_pred = (y_prob >= 0.5).astype(int)
    
    auc = roc_auc_score(y_true, y_prob)
    pr_auc = average_precision_score(y_true, y_prob)
    f1 = f1_score(y_true, y_pred)
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    return {
        'roc_auc': auc,
        'pr_auc': pr_auc,
        'f1': f1,
        'balanced_accuracy': bal_acc,
        'accuracy': acc,
        'sensitivity': sensitivity,
        'specificity': specificity,
        'n_samples_evaluated': len(y_true)
    }
