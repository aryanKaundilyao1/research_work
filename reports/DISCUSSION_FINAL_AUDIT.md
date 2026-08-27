# Discussion Final Audit

## 1. Numerical consistency
**PASS**. All numerical values match the authoritative audited list exactly: WESAD N=15, Dataset B evaluated N=31, LOSO-CV ROC-AUC=0.964, External absolute ROC-AUC=0.423, Cohen's d≈-1.47, ACC ablation ROC-AUC=0.540, Relative external ROC-AUC=1.000, Bootstrap iterations=5000, 95% CI=[1.000, 1.000], Permutation iterations=1000, Spearman ρ=0.9527, Jaccard=1.000. No new or unverified numbers were introduced.

## 2. Claim support
**PASS**. Every claim stems directly from the empirical results. The improvement from 0.423 to 0.540 supports the claim that ACC is only a partial confound. The improvement to 1.000 supports the claim that baseline-relative referencing mitigates the shift. The discussion explicitly frames these findings under the evaluated cohorts.

## 3. Causal-language audit
**PASS**. The discussion strictly avoids claims of biological causality or clinical validity. It explicitly states that "we do not claim that movement is inherently non-physiological" and that SHAP "does not establish biological equivalence, prove identical underlying physiological causality, or provide evidence of clinical validity." 

## 4. Zero-shot terminology audit
**PASS**. The term "zero-shot stress-label transfer" is used consistently. Section 8.5 provides a dedicated explanation clarifying that target stress labels were withheld while target baseline physiological measurements were utilized.

## 5. Limitation completeness
**PASS**. Section 8.10 accurately and rigorously lists the required limitations: small sample sizes (N=15, N=31), single source/target dataset constraint, the requirement of a target baseline period, the lack of complete causal decomposition for motion artifacts, the lack of biological equivalence from SHAP, and the non-universal nature of the perfect ROC-AUC.

## 6. Citation placeholder audit
**PASS**. The comparison with existing literature (Section 8.8) correctly identifies where citations are needed (e.g., multimodal physiological representations, Domain Adaptation techniques, and baseline normalization history). No citations were fabricated.

## 7. Novelty-claim discipline
**PASS**. The text avoids claiming "the first study" or similar hype. It frames the intervention as a simpler representation-level approach compared to complex Domain Adaptation, without claiming to be the first to invent baseline referencing. 

## Sentences needing revision
None identified. The text successfully balances scientific rigor, formal tone, and strict adherence to the empirical evidence without crossing into unsupported causal language.

## STAGE 5 (DISCUSSION) STATUS
STAGE 5 IS COMPLETE AND READY FOR THE FINAL CONCLUSION AND ABSTRACT (STAGE 6).

## What remains for STAGE 6
- Abstract (needs revision to align perfectly with the finalized empirical narrative, especially the baseline-relative terminology and specific domain-shift diagnostic).
- Conclusion (a brief final synthesis of the paper).
- References compilation (assembling the actual citations for the placeholders).
- Final figure and table compilation.
