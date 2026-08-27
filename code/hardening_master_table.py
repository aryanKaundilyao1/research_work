import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import PROJECT_ROOT

def main():
    reports_dir = os.path.join(PROJECT_ROOT, "reports", "final_hardening")
    
    fact_path = os.path.join(reports_dir, "normalization_acc_factorial.csv")
    boot_path = os.path.join(reports_dir, "bootstrap_results.csv")
    
    if not os.path.exists(fact_path) or not os.path.exists(boot_path):
        print("Missing required CSVs")
        return
        
    df_fact = pd.read_csv(fact_path)
    df_boot = pd.read_csv(boot_path)
    
    # We want a master table
    table_data = []
    
    # Absolute + ACC (Exp 3)
    row_abs_acc = df_fact[df_fact['Condition'] == 'Absolute + ACC (Exp 3)'].iloc[0]
    table_data.append({
        'Experiment': 'Absolute + ACC (Exp 3)',
        'Dataset': 'Dataset B',
        'N subjects': 31,
        'Representation': 'Absolute',
        'ACC Included': 'Yes',
        'ROC-AUC': f"{row_abs_acc['ROC-AUC']:.3f}",
        'Balanced Accuracy': f"{row_abs_acc['Balanced Accuracy']:.3f}",
        '95% CI': 'N/A'
    })
    
    # Absolute - ACC (Exp 4)
    row_abs_no_acc = df_fact[df_fact['Condition'] == 'Absolute - ACC (Exp 4)'].iloc[0]
    table_data.append({
        'Experiment': 'Absolute - ACC (Exp 4)',
        'Dataset': 'Dataset B',
        'N subjects': 31,
        'Representation': 'Absolute',
        'ACC Included': 'No',
        'ROC-AUC': f"{row_abs_no_acc['ROC-AUC']:.3f}",
        'Balanced Accuracy': f"{row_abs_no_acc['Balanced Accuracy']:.3f}",
        '95% CI': 'N/A'
    })
    
    # Relative - ACC (Exp 5)
    row_rel_no_acc = df_fact[df_fact['Condition'] == 'Relative - ACC (Exp 5)'].iloc[0]
    
    # Get CI for ROC-AUC from bootstrap
    boot_auc_row = df_boot[df_boot['Metric'] == 'ROC-AUC'].iloc[0]
    ci_str = f"[{boot_auc_row['CI_Lower']:.3f}, {boot_auc_row['CI_Upper']:.3f}]"
    
    table_data.append({
        'Experiment': 'Relative - ACC (Exp 5, Final)',
        'Dataset': 'Dataset B',
        'N subjects': 31,
        'Representation': 'Relative (Baseline)',
        'ACC Included': 'No',
        'ROC-AUC': f"{row_rel_no_acc['ROC-AUC']:.3f}",
        'Balanced Accuracy': f"{row_rel_no_acc['Balanced Accuracy']:.3f}",
        '95% CI': ci_str
    })
    
    # Relative + ACC (NEW)
    row_rel_acc = df_fact[df_fact['Condition'] == 'Relative + ACC (NEW)'].iloc[0]
    table_data.append({
        'Experiment': 'Relative + ACC (Factorial)',
        'Dataset': 'Dataset B',
        'N subjects': 31,
        'Representation': 'Relative (Baseline)',
        'ACC Included': 'Yes',
        'ROC-AUC': f"{row_rel_acc['ROC-AUC']:.3f}",
        'Balanced Accuracy': f"{row_rel_acc['Balanced Accuracy']:.3f}",
        '95% CI': 'N/A'
    })
    
    df_master = pd.DataFrame(table_data)
    
    with open(os.path.join(reports_dir, "final_statistical_table.md"), "w") as f:
        f.write("# Phase 15: Final Statistical Table\n\n")
        f.write(df_master.to_markdown(index=False))
        
    print("Master table created.")

if __name__ == "__main__":
    main()
