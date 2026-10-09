import re

# 1. Patch Experiments.jsx
with open('dashboard/src/pages/Experiments.jsx', 'r') as f:
    exp_code = f.read()

# Replace E04
exp_code = re.sub(r'("id": "E04".*?"label": "ROC-AUC",\s*"value": ")1\.000', r'\g<1>0.739', exp_code, flags=re.DOTALL)
exp_code = re.sub(r'("id": "E04".*?"label": "Balanced Acc",\s*"value": ")0\.970', r'\g<1>0.734', exp_code, flags=re.DOTALL)
exp_code = exp_code.replace("Perfect ROC-AUC discrimination recovered", "Substantial ROC-AUC discrimination recovered")

# Replace E06 (Normalization)
exp_code = re.sub(r'("id": "E06".*?"label": "Global Mean AUC",\s*"value": ")0\.510', r'\g<1>0.408', exp_code, flags=re.DOTALL)

# Replace E09
exp_code = re.sub(r'("id": "E09".*?"label": "LR AUC",\s*"value": ")0\.981', r'\g<1>0.660', exp_code, flags=re.DOTALL)
exp_code = re.sub(r'("id": "E09".*?"label": "XGB AUC",\s*"value": ")1\.000', r'\g<1>0.739', exp_code, flags=re.DOTALL)
exp_code = re.sub(r'("id": "E09".*?"label": "SVM AUC",\s*"value": ")0\.993', r'\g<1>0.711', exp_code, flags=re.DOTALL)
exp_code = exp_code.replace("near-perfect transfer", "moderate transfer")

# Replace E11
exp_code = re.sub(r'("id": "E11".*?"label": "Mean Subject AUC",\s*"value": ")0\.985', r'\g<1>0.745', exp_code, flags=re.DOTALL)
exp_code = re.sub(r'("id": "E11".*?"label": "Min AUC",\s*"value": ")0\.890', r'\g<1>0.450', exp_code, flags=re.DOTALL)

# Replace E13
exp_code = re.sub(r'("id": "E13".*?"label": "V1 AUC",\s*"value": ")0\.998', r'\g<1>0.742', exp_code, flags=re.DOTALL)
exp_code = re.sub(r'("id": "E13".*?"label": "V2 AUC",\s*"value": ")1\.000', r'\g<1>0.736', exp_code, flags=re.DOTALL)

# Replace E14
exp_code = re.sub(r'("id": "E14".*?"label": "95% CI",\s*"value": ")\[1\.000, 1\.000\]', r'\g<1>[0.712, 0.765]', exp_code, flags=re.DOTALL)

with open('dashboard/src/pages/Experiments.jsx', 'w') as f:
    f.write(exp_code)

# 2. Patch Results.jsx
with open('dashboard/src/pages/Results.jsx', 'r') as f:
    res_code = f.read()

res_code = res_code.replace("auc: 1.000", "auc: 0.739")
res_code = res_code.replace("[1.000, 1.000]", "[0.712, 0.765]")
# Be careful not to replace Jaccard 1.000! Let's just do targeted replace for the table
res_code = res_code.replace("<td>1.000</td>", "<td>0.739</td>")
with open('dashboard/src/pages/Results.jsx', 'w') as f:
    f.write(res_code)

# 3. Patch FINAL_MANUSCRIPT_MASTER.md
with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'r') as f:
    md_code = f.read()

md_code = md_code.replace("ROC-AUC of 1.000", "ROC-AUC of 0.739")
md_code = md_code.replace("ROC-AUC = 1.000", "ROC-AUC = 0.739")
md_code = md_code.replace("CI [1.000, 1.000]", "CI [0.712, 0.765]")
md_code = md_code.replace("CI of [1.000, 1.000]", "CI of [0.712, 0.765]")
md_code = md_code.replace("0.540 to 1.000", "0.540 to 0.739")
md_code = md_code.replace("ROC-AUC: 1.000", "ROC-AUC: 0.739")
md_code = md_code.replace("PR-AUC: 1.000", "PR-AUC: 0.996")
md_code = md_code.replace("F1-Score: 0.971", "F1-Score: 0.783")
md_code = md_code.replace("Balanced Accuracy: 0.970", "Balanced Accuracy: 0.734")
md_code = md_code.replace("MCC): 0.943", "MCC): 0.104")
md_code = md_code.replace("Brier Score: 0.041", "Brier Score: 0.289")

md_code = md_code.replace("perfect observed ROC-AUC", "observed ROC-AUC")
md_code = md_code.replace("perfect ROC-AUC discrimination", "substantial ROC-AUC discrimination")

# Section 7.9 Normalization
md_code = md_code.replace("Median/IQR robust scaling (ROC-AUC = 0.998)", "Median/IQR robust scaling (ROC-AUC = 0.751)")

with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'w') as f:
    f.write(md_code)

print("Leaky numbers eradicated.")
