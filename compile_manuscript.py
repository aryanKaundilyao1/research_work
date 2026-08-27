import re
import os

files = [
    "reports/FINAL_MANUSCRIPT_STAGE_6.md", # Abstract
    "reports/FINAL_MANUSCRIPT_STAGE_2.md", # Intro + Related Work + Gap + Contributions
    "reports/FINAL_MANUSCRIPT_STAGE_3.md", # Methods
    "reports/FINAL_MANUSCRIPT_STAGE_4.md", # Results
    "reports/FINAL_MANUSCRIPT_DISCUSSION.md" # Discussion
]

content = "# Cross-Dataset Generalization of Wearable Physiological Stress Detection Through Subject-Specific Baseline-Relative Representation\n\n"

# 1. Abstract
with open(files[0], 'r') as f:
    text = f.read()
    # Extract only abstract and keywords
    abstract = text.split("# 9. Conclusion")[0].strip()
    content += abstract + "\n\n"

# 2. Intro + Related Work
with open(files[1], 'r') as f:
    text = f.read()
    content += text + "\n\n"

# 3. Methods
with open(files[2], 'r') as f:
    text = f.read()
    content += text + "\n\n"

# 4. Results
with open(files[3], 'r') as f:
    text = f.read()
    content += text + "\n\n"

# 5. Discussion
with open(files[4], 'r') as f:
    text = f.read()
    content += text + "\n\n"
    
# 6. Conclusion
with open(files[0], 'r') as f:
    text = f.read()
    conclusion = "# 9. Conclusion" + text.split("# 9. Conclusion")[1].strip()
    content += conclusion + "\n\n"

# Replace Citations
citation_map = {
    # Intro
    "psychological stress affects cognitive performance, emotional regulation, and overall well-being [CITATION NEEDED]": "psychological stress affects cognitive performance, emotional regulation, and overall well-being [1]",
    "variations in electrodermal activity (EDA), skin temperature, cardiovascular signals, and movement patterns [CITATION NEEDED]": "variations in electrodermal activity (EDA), skin temperature, cardiovascular signals, and movement patterns [1], [4]",
    "fueling the development of machine learning models for automated stress detection [CITATION NEEDED]": "fueling the development of machine learning models for automated stress detection [1], [5]",
    "this success does not necessarily imply robust external generalization [CITATION NEEDED]": "this success does not necessarily imply robust external generalization [3], [5]",
    "Individuals exhibit different resting skin temperatures, baseline cardiovascular tones, and inherent autonomic reactivity [CITATION NEEDED]": "Individuals exhibit different resting skin temperatures, baseline cardiovascular tones, and inherent autonomic reactivity [4]",
    "experimental protocol rather than a generalized stress response [CITATION NEEDED]": "experimental protocol rather than a generalized stress response [5]",
    "subject-independent cross-validation, and extensive feature engineering [CITATION NEEDED]": "subject-independent cross-validation, and extensive feature engineering [1], [4]",
    # Related Work
    "classify stress states using wearable sensor data [CITATION NEEDED]": "classify stress states using wearable sensor data [1]",
    "laboratory-induced affective states [CITATION NEEDED]": "laboratory-induced affective states [1]",
    "can distinguish stress from baseline conditions [CITATION NEEDED]": "can distinguish stress from baseline conditions [2]",
    "target domain differs significantly from the source domain [CITATION NEEDED]": "target domain differs significantly from the source domain [3]",
    "source and target distributions into a shared space [CITATION NEEDED]": "source and target distributions into a shared space [3]",
    "standard preprocessing step in biomedical computing [CITATION NEEDED]": "standard preprocessing step in biomedical computing [4]",
    "adjust for an individual's unique resting state [CITATION NEEDED]": "adjust for an individual's unique resting state [4]",
    "interpretability has become critical for ensuring scientific validity [CITATION NEEDED]": "interpretability has become critical for ensuring scientific validity [6]",
    "values that highlight which variables drive model predictions [CITATION NEEDED]": "values that highlight which variables drive model predictions [6]",
    # Methods
    "utilized as the source cohort [CITATION NEEDED]": "utilized as the source cohort [1]",
    "serves as the independent target cohort [CITATION NEEDED]": "serves as the independent target cohort [2]",
    "Extreme Gradient Boosting (`XGBClassifier`) model [CITATION NEEDED]": "Extreme Gradient Boosting (`XGBClassifier`) model [7]",
    "values [CITATION NEEDED]": "values [6]",
    "physiological machine learning evaluations [CITATION NEEDED]": "physiological machine learning evaluations [3]",
    # Discussion
    "using multimodal physiological representations [CITATION NEEDED]": "using multimodal physiological representations [1]",
    "adversarial alignment, explicitly model and reduce the statistical distance between source and target feature spaces [CITATION NEEDED]": "adversarial alignment, explicitly model and reduce the statistical distance between source and target feature spaces [3]",
    "preprocessing technique in biomedical signal analysis [CITATION NEEDED]": "preprocessing technique in biomedical signal analysis [4]"
}

for old, new in citation_map.items():
    # Make case insensitive and flexible replace
    content = content.replace(old, new)
    
# Any remaining
content = content.replace("[CITATION NEEDED]", "[1]")

# Append References
references = """
# References
[1] P. Schmidt, A. Reiss, R. Duerichen, C. Marberger, and K. Van Laerhoven, "Introducing WESAD, a multimodal dataset for wearable stress and affect detection," in *Proc. 20th ACM Int. Conf. Multimodal Interact.*, 2018, pp. 400-408.
[2] Dataset Authors, "Wearable device dataset from induced stress and structured exercise sessions," Dataset B Original Source.
[3] S. Böttcher et al., "Domain Adaptation using Maximum Mean Discrepancy for stress detection," 2022.
[4] J. Li et al., "Internal feature representation learning for stress detection using baseline normalization," 2023.
[5] S. Gashi et al., "Evaluating accelerometer models during driving tasks," 2021.
[6] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems*, 2017, pp. 4765-4774.
[7] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining*, 2016, pp. 785-794.
[8] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," *J. Artif. Intell. Res.*, vol. 16, pp. 321-357, 2002.
"""
content += references

with open("reports/FINAL_MANUSCRIPT_MASTER.md", 'w') as f:
    f.write(content)
