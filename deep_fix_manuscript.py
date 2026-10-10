import re

with open("reports/FINAL_MANUSCRIPT_MASTER.md", "r") as f:
    text = f.read()

# 1. Feature contradictions
# Remove 17 features contradiction if still there
text = re.sub(r'The text says TEMP contributes four features and ACC three; the table actually contains five TEMP and two ACC features.', 'TEMP contributes five features and ACC two features, consistently with Table 3.', text)
text = text.replace("ACF/PACF outside that list", "ACF/PACF included in the 39 features per scalar channel")
text = text.replace("17 features per modality", "39 features per scalar channel")
text = text.replace("68 overall", "234 overall")

# 2. Citation reference misidentifications
text = text.replace("Expert Systems with Applications 237, 121578", "")
text = text.replace("Otesteanu", "Tognotti")

# 3. 3-13 point accuracy difference vs AUROC
text = re.sub(r'26.1-point AUROC difference.*?3–13-point AUROC difference', '26.1-point AUROC difference with a cited 3-13-point accuracy difference', text)

# 4. Diminishing returns (already did increasing gains, let's verify)
text = text.replace("diminishing returns", "increasing gains")

# 5. Placeholders on page 1 and section 6.11
text = re.sub(r'First Author, Second Author, Department, University', 'KT', text)
text = re.sub(r'## 6.11[\s\S]*?(?=## 7)', '', text) # Remove empty section 6.11

# 6. Deployment numbers
text = text.replace('calibration parameters for 20 selected features', 'per-channel calibration method for all signals')

# Let's save and then we need to recompile the PDF or whatever is needed
with open("reports/FINAL_MANUSCRIPT_MASTER.md", "w") as f:
    f.write(text)

print("Deep fix applied.")
