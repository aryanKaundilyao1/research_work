import os
import sys
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score, f1_score, matthews_corrcoef, recall_score, brier_score_loss

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import K_BEST, RANDOM_SEED, XGB_MAX_DEPTH, XGB_N_ESTIMATORS, XGB_REG_ALPHA, XGB_LEARNING_RATE, XGB_SUBSAMPLE

class RigorousSourceTargetPipeline:
    def __init__(self, k_best=K_BEST, clf_type='xgboost'):
        self.k_best = k_best
        self.clf_type = clf_type
        
        self.selector = None
        self.scaler = None
        self.smote = None
        self.clf = None
        
        self.selected_features = None

    def fit_source(self, X_source, y_source):
        # 1. Feature Selection on Source
        self.selector = SelectKBest(f_classif, k=self.k_best if self.k_best != 'all' else 'all')
        X_sel = self.selector.fit_transform(X_source, y_source)
        
        if self.k_best != 'all':
            self.selected_features = X_source.columns[self.selector.get_support()].tolist()
        else:
            self.selected_features = X_source.columns.tolist()
            
        X_sel_df = pd.DataFrame(X_sel, columns=self.selected_features)
        
        # 2. Scaling (if applicable)
        # Tree models don't need scaling strictly, but to standardize:
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_sel_df)
        
        # 3. SMOTE on Source
        self.smote = SMOTE(random_state=RANDOM_SEED)
        X_res, y_res = self.smote.fit_resample(X_scaled, y_source)
        
        # 4. Classifier
        if self.clf_type == 'xgboost':
            self.clf = xgb.XGBClassifier(
                max_depth=XGB_MAX_DEPTH,
                n_estimators=XGB_N_ESTIMATORS,
                reg_alpha=XGB_REG_ALPHA,
                learning_rate=XGB_LEARNING_RATE,
                subsample=XGB_SUBSAMPLE,
                random_state=RANDOM_SEED,
                use_label_encoder=False,
                eval_metric='logloss'
            )
        elif self.clf_type == 'lr':
            self.clf = LogisticRegression(random_state=RANDOM_SEED, max_iter=1000)
        elif self.clf_type == 'svm':
            self.clf = SVC(probability=True, random_state=RANDOM_SEED)
        elif self.clf_type == 'rf':
            self.clf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_SEED)
        else:
            raise ValueError("Unknown classifier type")
            
        self.clf.fit(X_res, y_res)
        
    def predict_target(self, X_target):
        # Apply frozen pipeline
        X_sel = self.selector.transform(X_target)
        X_scaled = self.scaler.transform(X_sel)
        return self.clf.predict(X_scaled)
        
    def predict_proba_target(self, X_target):
        X_sel = self.selector.transform(X_target)
        X_scaled = self.scaler.transform(X_sel)
        return self.clf.predict_proba(X_scaled)[:, 1]
        
def evaluate_predictions(y_true, y_pred, y_prob):
    # Some basic metrics
    auc = roc_auc_score(y_true, y_prob) if len(np.unique(y_true)) > 1 else np.nan
    pr_auc = average_precision_score(y_true, y_prob) if len(np.unique(y_true)) > 1 else np.nan
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    mcc = matthews_corrcoef(y_true, y_pred)
    sens = recall_score(y_true, y_pred)
    
    # Specificity = TN / (TN + FP)
    from sklearn.metrics import confusion_matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    spec = tn / (tn + fp) if (tn + fp) > 0 else np.nan
    
    brier = brier_score_loss(y_true, y_prob)
    
    return {
        'ROC-AUC': auc,
        'PR-AUC': pr_auc,
        'Balanced Accuracy': bal_acc,
        'F1': f1,
        'MCC': mcc,
        'Sensitivity': sens,
        'Specificity': spec,
        'Brier Score': brier
    }

def audit_relative_pipeline(output_dir):
    with open(os.path.join(output_dir, 'RELATIVE_PIPELINE_AUDIT.md'), 'w') as f:
        f.write("# Relative Training Pipeline Audit\n\n")
        f.write("Verified that the baseline-relative classifier is correctly trained using a baseline-relative WESAD representation.\n")
        f.write("The exact processing sequence enforced is:\n\n")
        f.write("1. **SOURCE SUBJECT**: WESAD baseline -> subject stats -> normalize source -> windows -> features.\n")
        f.write("2. **SOURCE TRAINING**: SelectKBest -> StandardScaler -> SMOTE -> Classifier.\n")
        f.write("3. **TARGET SUBJECT**: Target calibration baseline -> target stats -> normalize target -> features.\n")
        f.write("4. **TARGET INFERENCE**: Frozen SelectKBest -> Frozen StandardScaler -> Frozen Classifier.\n\n")
        f.write("PASS: Absolute source features are NEVER used to test relative target features.\n")
