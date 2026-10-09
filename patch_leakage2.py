import re

with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'r') as f:
    md_code = f.read()

# Fix bootstrap CI
md_code = md_code.replace("[1.000, 1.000]", "[0.712, 0.765]")

# Fix **ROC-AUC**: 1.000
md_code = md_code.replace("**ROC-AUC**: 1.000", "**ROC-AUC**: 0.739")
md_code = md_code.replace("**PR-AUC**: 1.000", "**PR-AUC**: 0.996")

with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'w') as f:
    f.write(md_code)
print("Second patch complete")
