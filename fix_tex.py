import re

with open("reports/final_manuscript/manuscript_draft.tex", "r") as f:
    text = f.read()

# 1. Participant Coverage
if "31 subjects of Dataset B" in text:
    text = text.replace("31 subjects of Dataset B", "21 eligible subjects of Dataset B (from an initial target cohort of 35, where 14 lacked complete baseline evaluation windows)")

# 2. Results update (1.000 -> 0.759, etc)
text = text.replace("ROC-AUC of 1.000", "ROC-AUC of 0.759")
text = text.replace("Balanced Accuracy of 0.971", "Balanced Accuracy of 0.670")
text = text.replace("Sensitivity of 0.941", "Sensitivity of 0.661")
text = text.replace("Specificity of 1.000", "Specificity of 0.679")
text = text.replace("CI of [1.000, 1.000]", "CI of [0.629, 0.871]")
text = text.replace("0.9527", "0.999")

# 3. Limitations 1.000
text = text.replace("report an ROC-AUC of 1.000", "report an ROC-AUC of 0.759")
text = text.replace("perfect rank-separability", "observed rank-separability")

# Save as manuscript_draft_corrected.tex
with open("reports/final_manuscript/manuscript_draft_corrected.tex", "w") as f:
    f.write(text)

print("Saved corrected tex")
