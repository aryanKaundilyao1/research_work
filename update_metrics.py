import os
import re

def update_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w') as f:
        f.write(content)

manuscript_replacements = [
    ("ROC-AUC = 0.772", "ROC-AUC = 0.759"),
    ("AUROC of 0.772", "AUROC of 0.759"),
    ("0.540 to 0.772", "0.540 to 0.759"),
    ("ROC-AUC of 0.772", "ROC-AUC of 0.759"),
    ("ROC-AUC: 0.772", "ROC-AUC: 0.759"),
    ("[0.643, 0.880]", "[0.629, 0.871]"),
    ("AUROC of 0.754", "AUROC of 0.739"),
    ("0.980", "0.999"),
    ("0.6667 for Top-10", "1.0000 for Top-10"), # Wait, the Jaccard for Top-10 is now 1.000
]

update_file("reports/FINAL_MANUSCRIPT_MASTER.md", manuscript_replacements)

# Now, we also need to fix the dashboard
dashboard_replacements = [
    ("1.000", "0.759"), # Fix the 1.000 that the subagent put for baseline-relative
    ("0.970", "0.670"), # Balanced accuracy
    ("0.941", "0.661"), # Sensitivity
    ("0.9527", "0.999"), # Spearman rho
    ("1.000, 1.000", "0.629, 0.871"), # Bootstrap CI
]

update_file("dashboard/src/pages/Results.jsx", dashboard_replacements)
update_file("dashboard/src/pages/Experiments.jsx", dashboard_replacements)

print("Updates completed.")
