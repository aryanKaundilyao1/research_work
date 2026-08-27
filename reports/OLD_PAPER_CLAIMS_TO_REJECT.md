# Old Paper Claims to Reject and Replace

The previous manuscript contained several framings and claims that conflict with the new scientific narrative. These must be strictly avoided in the new manuscript.

## 1. The Focus on Phase Segmentation
- **Old Claim:** "How stress shifts across different phases of an exam has not been studied closely. This study builds a phase-aware stress classification framework..."
- **Why to Reject:** Our new study explicitly moves away from internal feature engineering. The entire contribution is about cross-dataset generalization.
- **Replacement Framing:** "Machine learning models for physiological stress detection often demonstrate strong internal validation performance, but this can substantially overestimate cross-cohort generalizability."

## 2. Dataset Specificity as the Main Problem
- **Old Claim:** "Many stress detection studies rely on stress induced in a lab rather than stress that occurs naturally, in places like classrooms."
- **Why to Reject:** Our new paper uses both a lab dataset (WESAD) and a classroom dataset (Dataset B) to prove a transfer failure. The problem is domain shift, not just the setting.
- **Replacement Framing:** "Differences in absolute physiological limits and laboratory-specific physical protocols create severe domain mismatch during independent external evaluation."

## 3. Treating 0.801 AUC as the Ultimate Finding
- **Old Claim:** "The framework reached an AUC of 0.801. The permutation test gave p = 0.020, which suggests the observed performance was unlikely to come from random label assignments..."
- **Why to Reject:** 0.801 was an internal Dataset B result. Our external baseline-relative result is 1.000. We must not confuse the two.
- **Replacement Framing:** "Transitioning to the subject-specific baseline-relative physiological representation substantially recovered generalization in the evaluated external cohort (ROC-AUC = 1.000)."

## 4. Unqualified Use of Accelerometer Features
- **Old Claim:** "SHAP analysis showed that temperature-based features and accelerometer-derived motion patterns from the middle and end phases mattered most for classification."
- **Why to Reject:** We discovered that ACC is a massive domain-shift confound ($d \approx -1.47$) that captures the *experimental protocol*, not physiological stress. It actively harmed cross-dataset transfer.
- **Replacement Framing:** "Diagnostic analysis identified the accelerometer as a massive domain-shift confound reflecting protocol differences (Cohen's $d \approx -1.47$), and its ablation partially improved transfer."

## 5. Vague Claims about "Biomarkers"
- **Old Claim:** "These results show that adding temporal phase information... surfaces biomarkers tied to specific points in an exam."
- **Why to Reject:** We are doing model attribution, not establishing biological causality or clinical biomarkers.
- **Replacement Framing:** "Cross-dataset SHapley Additive exPlanations (SHAP) feature attribution was highly conserved, indicating the model relied on a stable physiological representation across cohorts."

## 6. Dataset Characteristics (Dataset B)
- **Old Claim:** "We used the publicly available Wearable Exam Stress Dataset... 10 students across 3 exams each, for 30 recordings total."
- **Why to Reject:** This directly conflicts with our audited evaluation of $N=31$ separate subject instances (34 original minus S02, f07, f14).
- **Replacement Framing:** "The target cohort, Dataset B, originally comprised 34 participant instances. After applying signal quality exclusions (S02, f07, f14), exactly 31 subject instances were evaluated."
