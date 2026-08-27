import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import copy

from config import RANDOM_SEED, K_BEST, XGB_MAX_DEPTH, XGB_N_ESTIMATORS, XGB_REG_ALPHA, XGB_LEARNING_RATE, XGB_SUBSAMPLE

def get_base_model():
    return XGBClassifier(
        n_estimators=XGB_N_ESTIMATORS,
        max_depth=XGB_MAX_DEPTH,
        learning_rate=XGB_LEARNING_RATE,
        subsample=XGB_SUBSAMPLE,
        reg_alpha=XGB_REG_ALPHA,
        random_state=RANDOM_SEED,
        eval_metric='logloss'
    )

def run_nested_cv(X, y, groups):
    """
    Executes Leave-One-Subject-Out CV for WESAD internal validation.
    Strictly nests Scaling, Feature Selection, and SMOTE within the training fold.
    Returns the out-of-fold predictions.
    """
    logo = LeaveOneGroupOut()
    
    oof_preds = np.zeros(len(y))
    fold_models = []
    
    for fold, (train_idx, test_idx) in enumerate(logo.split(X, y, groups)):
        X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        X_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
        
        # 1. Scaling (Fit only on training data)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 2. Feature Selection (Fit only on training data)
        k = min(K_BEST, X_train_scaled.shape[1])
        selector = SelectKBest(f_classif, k=k)
        X_train_sel = selector.fit_transform(X_train_scaled, y_train)
        X_test_sel = selector.transform(X_test_scaled)
        
        # 3. SMOTE (Apply only to training data)
        n_minority = min(np.sum(y_train == 0), np.sum(y_train == 1))
        k_neighbors = min(5, n_minority - 1)
        if k_neighbors > 0:
            sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=k_neighbors)
            X_train_res, y_train_res = sm.fit_resample(X_train_sel, y_train)
        else:
            X_train_res, y_train_res = X_train_sel, y_train
            
        # 4. XGBoost Training
        model = get_base_model()
        model.fit(X_train_res, y_train_res)
        
        # 5. Prediction on strictly held-out test subject
        preds = model.predict_proba(X_test_sel)[:, 1]
        oof_preds[test_idx] = preds
        
        # Save model elements if interpretation is needed later
        fold_models.append({
            'scaler': scaler,
            'selector': selector,
            'model': model
        })
        
    return oof_preds, fold_models

def train_final_model(X, y):
    """
    Trains the final pipeline on 100% of WESAD data.
    Used exclusively for External Cross-Dataset Generalization.
    """
    # 1. Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Feature Selection
    k = min(K_BEST, X_scaled.shape[1])
    selector = SelectKBest(f_classif, k=k)
    X_sel = selector.fit_transform(X_scaled, y)
    
    # 3. SMOTE
    n_minority = min(np.sum(y == 0), np.sum(y == 1))
    k_neighbors = min(5, n_minority - 1)
    if k_neighbors > 0:
        sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=k_neighbors)
        X_res, y_res = sm.fit_resample(X_sel, y)
    else:
        X_res, y_res = X_sel, y
        
    # 4. XGBoost Training
    model = get_base_model()
    model.fit(X_res, y_res)
    
    return {
        'scaler': scaler,
        'selector': selector,
        'model': model
    }

def predict_external(frozen_pipeline, X_external):
    """
    Applies the frozen WESAD pipeline to an external dataset (Dataset B)
    WITHOUT any refitting or data leakage.
    """
    scaler = frozen_pipeline['scaler']
    selector = frozen_pipeline['selector']
    model = frozen_pipeline['model']
    
    X_ext_scaled = scaler.transform(X_external)
    X_ext_sel = selector.transform(X_ext_scaled)
    preds = model.predict_proba(X_ext_sel)[:, 1]
    
    return preds
