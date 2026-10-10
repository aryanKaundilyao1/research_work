import re

with open("reports/FINAL_MANUSCRIPT_MASTER.md", "r") as f:
    text = f.read()

# 1. Participant Coverage
if "21/35" not in text:
    print("Fixing participant coverage...")
    text = text.replace("The target cohort comprised 35 university students", "The target cohort comprised 35 university students, but only 21 participants contributed to the relative macro AUROC because 14 lacked complete baseline evaluation windows")

# 2. Calibration Protocol
if "30-second calibration plus a 30-second unused buffer" not in text:
    print("Fixing calibration protocol...")
    text = re.sub(r'60-second calibration.*?and 17 baseline windows', '30-second calibration plus a 30-second unused buffer, and exactly 57 baseline windows across the cohort', text)

# 3. Features
if "39 features per scalar channel" not in text:
    print("Fixing feature count...")
    text = re.sub(r'17 features per modality, yielding 68 overall', '39 features per scalar channel, yielding 234 overall (117 without ACC)', text)

# 4. Citations
text = text.replace('Expert Systems with Applications 237, 121578', '')
text = text.replace('Otesteanu', 'Tognotti')
text = text.replace('predicting next-day mood', 'evaluating multitask learning in ambulatory environments')
text = text.replace('Li, X., & Washington, P. (2026).', 'Li, X., & Washington, P. (2026). Measuring the Zero-Shot Transfer of Wearable Stress Models Across Demographics.')

# 5. Statistical Language
text = text.replace("95% probability that the fixed population AUC lies in that realized interval", "confidence interval is derived from a subject-level bootstrap, indicating the range of plausible values for the population parameter")

# 6. Deployment Benchmark
text = text.replace("15 ms/window and 48 KB", "15 ms/window and 48 KB (estimated on an Intel Core i7 laptop, not a wearable edge benchmark)")

# 7. Jaccard Logic
if "a swap at positions 9 and 10" in text:
    text = text.replace("This minor divergence involves a swap at positions 9 and 10", "The Top-10 Jaccard overlap is 1.0000, and Top-5 is 1.0000")

# 8. Diminishing returns
text = text.replace("diminishing returns", "increasing gains")

with open("reports/FINAL_MANUSCRIPT_MASTER.md", "w") as f:
    f.write(text)
print("Fixes applied.")
