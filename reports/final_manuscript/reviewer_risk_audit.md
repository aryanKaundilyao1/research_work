# Reviewer Risk Audit & Pre-emptive Rebuttals

## Reviewer A: Biomedical Signal-Processing Expert
**Profile:** Cares deeply about signal quality, baseline assumptions, and physiological plausibility. Skeptical of "black box" ML.
- **Primary Risk:** "A 60-second baseline is not a true physiological baseline, which clinically requires 5-10 minutes of complete rest. Furthermore, your normalization assumes linearity in physiological responses, which isn't true for EDA."
- **Pre-emptive Mitigation:** Section 4.7 strictly defines our use of the term "baseline" as an *experimental reference* rather than a *clinical resting state*. We include the Baseline Duration Sensitivity audit (Phase 5) to demonstrate empirically that even a 30-second relative reference successfully shifts the distribution enough to rescue transferability for this model. We make no claims about biological causality.

## Reviewer B: Machine Learning & Generalization Expert
**Profile:** Looks for data leakage, overfit models, improper cross-validation, and inflated metrics due to overlapping windows.
- **Primary Risk:** "You achieved an AUC of 1.000. This is an obvious case of data leakage or window-level evaluation artifact. It's impossible."
- **Pre-emptive Mitigation:** Section 4.13 (Leakage Prevention) is explicitly designed to preempt this. We detail the strict zero-shot target inference. We explicitly declare in Section 5.5 and the Discussion that the 1.000 AUC is *not* a claim of a perfect universal model, but rather a reflection of the clean probability separation within the finite 31-subject Dataset B cohort. We emphasize that we aggregated predictions to the *subject level* to compute confidence intervals, proving the separation is robust to subject resampling (Phase 3).

## Reviewer C: Highly Skeptical Journal Reviewer (General Audience)
**Profile:** Dislikes "incremental ML tweaks" and demands to know the broader significance without allowing authors to overclaim.
- **Primary Risk:** "Baseline normalization is a standard preprocessing step that has been used in psychology for decades. This is not a novel methodological paper."
- **Pre-emptive Mitigation:** In the Introduction and Discussion, we explicitly concede that baseline normalization is an established technique. The novelty is our systematic, diagnostic proof of *why* wearable models fail cross-dataset (ACC domain shift) and the demonstration (via cross-dataset SHAP agreement) that relative physiological deviation allows an ML model to transfer *strictly zero-shot* without complex Domain Adaptation. The contribution is the validation of the transferability of the representation, not the invention of the normalization equation.
