from docx import Document
import re
import shutil

# First, make a copy to work on
shutil.copy("/Users/aryankaundilya/Downloads/stress_paper_FINAL_v3 (1).docx", "/Users/aryankaundilya/Downloads/stress_paper_FINAL_v4.docx")

doc = Document("/Users/aryankaundilya/Downloads/stress_paper_FINAL_v4.docx")

replacements = {
    # Participant Coverage
    "31 subjects of Dataset B": "21 eligible subjects of Dataset B (from an initial target cohort of 35, where 14 lacked complete baseline evaluation windows)",
    "target cohort comprised 35 university students": "target cohort comprised 35 university students, but only 21 participants contributed to the relative macro AUROC because 14 lacked complete baseline evaluation windows",
    
    # Numbers
    "ROC-AUC of 1.000": "ROC-AUC of 0.759",
    "ROC-AUC = 1.000": "ROC-AUC = 0.759",
    "Balanced Accuracy of 0.971": "Balanced Accuracy of 0.670",
    "Sensitivity of 0.941": "Sensitivity of 0.661",
    "Specificity of 1.000": "Specificity of 0.679",
    "CI of [1.000, 1.000]": "CI of [0.629, 0.871]",
    "ρ = 0.9527": "ρ = 0.999",
    "0.9527": "0.999",
    "ROC-AUC of 0.772": "ROC-AUC of 0.759",
    "ROC-AUC = 0.772": "ROC-AUC = 0.759",
    
    # Limitations 1.000
    "report an ROC-AUC of 1.000": "report an ROC-AUC of 0.759",
    "perfect rank-separability": "observed rank-separability",
    
    # Calibration Protocol
    "60-second calibration": "30-second calibration plus a 30-second unused buffer",
    "17 baseline windows": "57 baseline windows across the cohort",
    
    # Features
    "17 features per modality": "39 features per scalar channel",
    "68 overall": "234 overall (117 without ACC)",
    "TEMP contributes four features and ACC three": "TEMP contributes five features and ACC two features, consistently with Table 3",
    "ACF/PACF outside that list": "ACF/PACF included in the 39 features per scalar channel",
    
    # Citations
    "Expert Systems with Applications 237, 121578": "",
    "Otesteanu": "Tognotti",
    "predicting next-day mood": "evaluating multitask learning in ambulatory environments",
    
    # Statistical Language
    "95% probability that the fixed population AUC lies in that realized interval": "confidence interval is derived from a subject-level bootstrap, indicating the range of plausible values for the population parameter",
    
    # Deployment Benchmark
    "15 ms/window and 48 KB": "15 ms/window and 48 KB (estimated on an Intel Core i7 laptop, not a wearable edge benchmark)",
    "calibration parameters for 20 selected features": "per-channel calibration method for all signals",
    
    # Jaccard Logic
    "a swap at positions 9 and 10": "Top-10 Jaccard overlap is 1.0000",
    "Top-5 is 1.000": "Top-5 is 1.0000",
    
    # Diminishing returns
    "diminishing returns": "increasing gains",
    
    # Placeholders on page 1 and section 6.11
    "First Author, Second Author, Department, University": "KT"
}

def replace_in_paragraph(paragraph):
    for old, new in replacements.items():
        if old in paragraph.text:
            # Simple text replacement - loses formatting if spanning runs, 
            # but usually fine for simple replacements if done at the paragraph level
            # We'll do a run-level replacement if possible, or just overwrite paragraph text
            # To be safe and preserve most formatting, we'll replace the text in the first run 
            # and clear the others if it spans, OR just replace paragraph.text.
            # However paragraph.text clears all formatting!
            # Let's try replacing in runs.
            for run in paragraph.runs:
                if old in run.text:
                    run.text = run.text.replace(old, new)
            
            # If not in a single run, fallback to full paragraph text replacement (loses inline formatting)
            if old in paragraph.text:
                paragraph.text = paragraph.text.replace(old, new)

for p in doc.paragraphs:
    replace_in_paragraph(p)
    
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                replace_in_paragraph(p)

doc.save("/Users/aryankaundilya/Downloads/stress_paper_FINAL_v4.docx")
print("DOCX updated")
