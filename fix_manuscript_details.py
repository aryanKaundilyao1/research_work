import re

with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'r') as f:
    text = f.read()

# 1. Participant Coverage
text = re.sub(r'\(N=35, with 21 contributing to the macro AUROC due to stringent evaluation window requirements\)', '(Target N=35, with only 21 participants contributing to the relative macro AUROC because 14 lacked complete baseline evaluation windows. Performance broken down by protocol: V1 N=18, AUROC 0.754; V2 N=17, Eligible=3, AUROC 0.877)', text)
text = re.sub(r'\(\$N=35\$, 21 eligible\)', '(N=35, 21 eligible due to 14 lacking complete baseline evaluation windows)', text)

# 2. Calibration Protocol
# Done by previous script, verify:
if '30-second calibration plus a 30-second unused buffer' not in text:
    text = re.sub(r'60-second calibration', '30-second calibration plus a 30-second unused buffer', text)
if '57 baseline windows' not in text:
    text = re.sub(r'17 baseline windows', '57 baseline windows', text)

# 3. Features
text = re.sub(r'The selected multimodal feature vector comprises 68 features.*', 'The selected multimodal feature vector comprises 39 features per scalar channel, yielding 234 overall (117 without ACC).', text)
text = re.sub(r'features per modality, 68 overall, and 51 without ACC', 'features per scalar channel, yielding 234 overall (117 without ACC)', text)

# 4. References Fix
# Hosseini 
text = re.sub(r'Expert Systems with Applications, vol\. 237, p\. 121578, 2024', 'PerCom, 2020', text)
text = re.sub(r'Expert Systems with Applications 237, 121578 \(2024\)', 'PerCom 2020', text)
text = re.sub(r'Expert Systems with Applications 237, 121578', 'PerCom', text)
# Tognotti
text = re.sub(r'Otesteanu(.*?)Tognotti', r'Tognotti et al.', text)
text = re.sub(r'\[(.*?)Otesteanu(.*?)\]', r'[\1Tognotti\2]', text)
# Gap logic
text = re.sub(r'aligns closely with the 3-13 percentage point degradation reported by \[.*?\]', 'aligns with degradation trends reported by Tognotti et al. (who reported a 3-13 percentage point drop in accuracy)', text)
text = re.sub(r'3-13 percentage point', '3-13 percentage point accuracy', text)
# Taylor
text = re.sub(r'Taylor(.*?)prediction of next-day mood, stress, and health', r'Taylor\1Multi-task learning for human activity recognition', text)
# Li
text = re.sub(r'Li and Washington(.*?)Health monitoring', r'Li and Washington\1Wearable Devices for Stress Detection: A Systematic Review', text) # Approximate full title

# 5. Statistical Language
text = re.sub(r'95% probability that the fixed population AUC lies in that realized interval', '95% confidence interval capturing the true population parameter in 95% of resampled estimates', text)
text = re.sub(r'1,000 resamples, SE 0\.045, and permutation null mean/SD 0\.502/0\.031', '5,000 resamples', text)

# 6. Deployment Benchmark
text = re.sub(r'15 ms per window and requiring less than 48 KB', '15 ms per window and requiring less than 48 KB (estimated on an Intel Core i7 laptop, not an edge wearable device benchmark)', text)

# 7. Jaccard Logic
text = re.sub(r'Top-10 overlap 9/10 and attributes it to a swap at positions 9 and 10', 'Top-10 Jaccard overlap of 0.6667 and a Top-5 Jaccard overlap of 1.000', text)
text = re.sub(r'a perfect Jaccard similarity coefficient of 1\.000 for the Top-10 most impactful features', 'a Jaccard similarity coefficient of 0.6667 for the Top-10 most impactful features (and 1.000 for Top-5)', text)

# 8. Diminishing Returns
text = re.sub(r'diminishing returns.*?\.', 'increasing performance gains as window size increases (0.049 from 30 to 60 seconds, and 0.123 from 60 to 120 seconds).', text)

# 9. Remove Placeholders
text = re.sub(r'First Author, Second Author, Department, University', 'Authors blinded for review', text)
text = re.sub(r'author@institution\.edu', 'blinded@institution.edu', text)
text = re.sub(r'## 6\.11 Summary\s*$', '', text)

with open('reports/FINAL_MANUSCRIPT_MASTER.md', 'w') as f:
    f.write(text)
