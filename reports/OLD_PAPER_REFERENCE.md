# Previous Paper / Manuscript Reference

[USER: Please paste the full text of the old paper below this line.]

---Abstract
Background: Wearable physiological sensing is a promising way to assess stress objectively in school settings. Most prior work on the Wearable Exam Stress Dataset used features aggregated across the whole exam, which can hide how physiological responses change as an exam progresses. How stress shifts across different phases of an exam has not been studied closely.
Methods: This study builds a phase-aware stress classification framework using wearable signals recorded during real university exams. We preprocessed electrodermal activity (EDA), skin temperature (TEMP), heart rate (HR), blood volume pulse (BVP), and tri-axial accelerometry (ACC) with interpolation, z-score normalization, and Gaussian smoothing. Each recording was split into Beginning, Middle, and End phases, and we extracted statistical, spectral, and heart-rate-variability (HRV) features separately for each phase, giving a feature set that captures how physiology changes over time. We selected features with ANOVA ranking, balanced the classes with SMOTE, and trained an XGBoost classifier. We evaluated the model with leave-one-subject-out cross-validation and interpreted it with SHAP.
Results: The framework reached an AUC of 0.801. The confusion matrix showed 16 true negatives, 8 true positives, 2 false positives, and 4 false negatives. SHAP analysis showed that temperature-based features and accelerometer-derived motion patterns from the middle and end phases mattered most for classification.
Conclusion: These results show that adding temporal phase information improves physiological stress modeling and surfaces biomarkers tied to specific points in an exam. Stress during exams looks dynamic rather than constant, which supports building phase-aware machine learning models for wearable stress assessment.

1. Introduction
Psychological stress affects cognitive performance, emotional regulation, attention, memory, and decision-making. Academic exams are one of the most common natural stressors students face, and they give researchers a controlled setting to study how stress shows up physically. Stress responses include changes in autonomic nervous system activity, skin conductance, heart rate variability, peripheral temperature, and movement patterns.
Wearable sensing has made it possible to track these signals continuously in real-world settings. The Empatica E4 wristband, for example, can record electrodermal activity, skin temperature, heart rate, blood volume pulse, and accelerometer data at the same time, giving a multimodal picture of someone's physiological state. This has fueled interest in wearable stress detection systems that work without self-report questionnaires or lab equipment.
Even so, the existing literature has some gaps. Many stress detection studies rely on stress induced in a lab rather than stress that occurs naturally, in places like classrooms. And studies using the Wearable Exam Stress Dataset have mostly treated the whole exam as one block, extracting features across the full recording. That assumption misses the possibility that stress responses change as students move from initial anticipation into sustained problem-solving and then into time-pressure near the end.
Interpretability is another gap. Models can perform well without telling us much about which biomarkers drive their decisions, and in biomedical work that kind of explanation matters for scientific validity and for turning results into practical use.
To address these gaps, we propose a phase-segmented stress classification framework based on wearable signals. Instead of treating an exam as one observation period, we split each recording into Beginning, Middle, and End phases, which lets us look at how stress evolves over the course of an exam.
This work contributes:
A phase-aware physiological stress modeling framework that captures temporal dynamics across exam stages.
Statistical, spectral, and HRV biomarkers extracted separately from the Beginning, Middle, and End phases.
An XGBoost classification pipeline with feature selection and class imbalance correction.
Subject-independent cross-validation to reduce identity leakage and improve generalizability.
SHAP-based interpretation of model predictions.
Phase-specific biomarkers tied to exam stress.

2. Related Work / Literature Review
Wearable Stress Detection Using Physiological Signals
Wearable stress detection is now a major topic in affective computing and digital health. Signals such as electrodermal activity, photoplethysmography, heart rate, skin temperature, and ECG reliably reflect autonomic nervous system activation under stress, and several studies have used machine learning on wearable sensor data to classify stress successfully.
The WESAD dataset set an early benchmark for multimodal stress detection by combining physiological measurements recorded during lab-induced affective states. Later work showed that models built from EDA, heart rate, and movement features can tell stress apart from baseline conditions, which helped establish wearable sensing as a real alternative to self-report.
In education, wearable monitoring has drawn growing attention because exam stress is a naturally occurring source of cognitive and emotional strain. The Wearable Exam Stress Dataset gave researchers a real-world benchmark: physiological recordings from actual university exams. Early analyses found that these signals carry useful information about exam performance and stress outcomes.
Temporal and Phase-Based Analysis of Stress
Most wearable stress detection studies assume stress stays roughly constant over an observation period and extract features from the whole recording as a single block. That's convenient, but it can hide transient physiological changes that happen during a long stressful event.
Psychological theory suggests stress responses aren't static. During an exam, students typically feel anticipatory stress at the start, sustained cognitive load through the middle, and rising urgency near the end. Biomarkers should be expected to vary across these phases.
Some recent biomedical signal processing work has explored temporal segmentation, including sliding windows, event-centered segmentation, and state-transition modeling, but phase-based modeling remains mostly unexplored for exam stress detection specifically. The original Wearable Exam Stress Dataset paper flagged exam-phase analysis as a direction worth pursuing.
Tree-Based Machine Learning for Physiological Classification
Stress detection systems commonly use Support Vector Machines, Random Forests, k-Nearest Neighbors, and Multi-Layer Perceptrons. These can perform well, but gradient boosting methods tend to do better on structured tabular data.
XGBoost in particular has become a go-to algorithm for biomedical classification. It handles nonlinear relationships and feature interactions well, includes built-in regularization, and holds up under limited sample sizes — all useful properties for physiological datasets, which often have few subjects but many extracted features.
That description fits the Wearable Exam Stress Dataset closely: relatively few subjects, a large number of features. Gradient boosting is a natural fit here because it can pick up informative interactions without much manual feature engineering.
Explainable AI in Biomedical Research
As models get more complex, interpretability becomes more important in biomedical work. Predictions without physiological justification are hard to trust clinically and don't add much to scientific understanding.
SHAP (SHapley Additive exPlanations) has become a common way to interpret models. By assigning contribution values to individual features, it lets researchers see which physiological variables are driving classification outcomes.
In wearable stress research, this kind of explainability does two things. It checks whether a model is relying on biomarkers that make physiological sense, and it can surface new stress indicators worth investigating further. Pairing a strong-performing model with SHAP interpretation is a reasonable step toward stress detection systems that are actually useful clinically.

3. Dataset & Preprocessing
3.1 Wearable Exam Stress Dataset

We used the publicly available Wearable Exam Stress Dataset, which contains physiological recordings from undergraduate students during real university exams. The data came from Empatica E4 wristbands worn by ten students across three exams each: Midterm 1, Midterm 2, and a Final. Each student could contribute up to three sessions, for thirty examination recordings total.
![][image1]
The Empatica E4 recorded several signals at once:
Electrodermal Activity (EDA) at 4 Hz
Skin Temperature (TEMP) at 4 Hz
Heart Rate (HR) at 1 Hz
Blood Volume Pulse (BVP) at 64 Hz
Accelerometer X, Y, Z axes (ACC_X, ACC_Y, ACC_Z) at 32 Hz
We derived performance labels from exam scores, converting them into binary classes (higher- vs. lower-performing) using an 80% threshold, following prior work on this dataset.
The full processing pipeline is shown in Figure 5.
3.2 Signal Cleaning
Raw physiological recordings usually have missing samples, motion artifacts, and sensor noise. To keep things consistent across modalities, we applied the same cleaning steps to every signal.
First, we trimmed each recording down to the exam interval only, so physiological activity unrelated to the exam wouldn't get pulled into the analysis. This matches preprocessing used in earlier work on the same dataset.
Second, we filled in missing values with linear interpolation. Given two neighboring samples $(t_1,x_1)$ and $(t_2,x_2)$, we estimated missing values as:
$$x(t)=x_1+\frac{(t-t_1)}{(t_2-t_1)}(x_2-x_1)$$
This keeps temporal continuity while minimizing distortion of the underlying trend.
Third, we applied Gaussian smoothing with a three-minute window. The Gaussian kernel cuts down high-frequency noise and short-lived artifacts while keeping the slower changes tied to stress responses. This follows the preprocessing reported for the Wearable Exam Stress Dataset.
3.3 Normalization
Physiological signals vary a lot between people because of differences in baseline autonomic activity, metabolism, fitness, and environment. To cut down on these confounds, we ran z-score normalization separately for each signal.
For a signal $x$:
$$z=\frac{x-\mu}{\sigma}$$
where $\mu$ is the mean and $\sigma$ the standard deviation.
This puts every modality on a common scale centered at zero with unit variance, which makes comparisons between sensor channels more meaningful and helps the model train more stably. Earlier work on examination stress classification has used similar normalization.

4. Phase Segmentation


A central piece of this work is splitting each exam recording into three phases instead of treating the exam as one continuous block. The segmentation strategy is shown in Figure 2.
Let $T$ be the total exam duration. We split each exam as follows:
Beginning Phase: first 25% of the recording
Middle Phase: middle 50% of the recording
End Phase: final 25% of the recording
This split balances temporal resolution against feature stability while keeping the phases physiologically meaningful.
![][image2] Figure 2. Phase segmentation strategy. Each exam recording was divided into Beginning (25%), Middle (50%), and End (25%) phases before feature extraction.
4.1 Beginning Phase
The Beginning Phase covers the first quarter of the exam, when anticipatory stress tends to show up right after the exam starts. Students often feel uncertainty and heightened sympathetic activation as they adjust to the demands of the exam.
Physiologically, this can show up as elevated heart rate, increased electrodermal activity, and temperature shifts tied to the onset of acute stress.
4.2 Middle Phase
The Middle Phase covers the central 50% of the exam — the longest and most cognitively demanding stretch, when students are concentrating, solving problems, retrieving memory, and managing their workload.
Anticipatory effects have mostly faded by this point, and the urgency of finishing hasn't kicked in yet, so the Middle Phase may give the most stable picture of sustained cognitive stress.
4.3 End Phase
The End Phase covers the final quarter, when deadlines, unanswered questions, and time pressure start to weigh on students. Urgency and emotional arousal tend to rise as the exam nears its end.
Because of that, biomarkers from this phase can look different from earlier ones, and Section 7's SHAP analysis backs this up by showing how important End Phase features turn out to be.

5. Feature Extraction
We extracted features separately for each signal within each phase. Pulling features from the Beginning, Middle, and End segments individually keeps temporal information that would otherwise get lost if we aggregated across the whole exam.
For each signal $s$ and phase $p$, we computed a feature vector $F_{s,p}$, then concatenated features across all signals and phases into one high-dimensional representation of physiological behavior over the exam.
The final feature set combines statistical descriptors, spectral characteristics, and HRV biomarkers, which goes beyond what prior studies on this dataset typically used — mostly aggregated, exam-level statistics.

5.1 Statistical Features
Statistical features summarize the shape and distribution of a signal over time. These descriptors have repeatedly shown up as useful for stress classification because they capture central tendency, variability, asymmetry, and sudden fluctuations tied to autonomic activation.
For each signal-phase combination, we extracted:
Mean
Standard deviation
Root mean square (RMS)
Median
Minimum
Maximum
First quartile (Q1)
Third quartile (Q3)
Skewness
Kurtosis
Peak value
Crest factor
Impulse factor
Clearance factor
Shape factor
Positive count
Negative count
A few of these higher-order statistics carry real physiological meaning. Skewness picks up on asymmetry in the distribution and can point to transient events. Kurtosis flags outliers or extreme responses. Crest factor and impulse factor capture sudden deviations from baseline, which can reflect acute stress reactions.
We also computed Autocorrelation Function at lag 1 (ACF1) and Partial Autocorrelation Function at lag 1 (PACF1) to capture short-term temporal dependencies within each signal.
5.2 Spectral Features
Stress-related responses often show up as changes in frequency content, not just time-domain statistics, so spectral analysis adds something time-domain features miss.
We estimated power spectral density (PSD) with Welch's method, which reduces variance by averaging modified periodograms across overlapping windows — a common approach in biomedical signal processing.
For each signal-phase segment, we interpolated PSD values into twenty spectral bins, capturing the frequency-dependent energy distribution without tying the features to specific frequency locations.
Spectral descriptors are particularly useful for catching rhythmic patterns and oscillatory responses tied to autonomic regulation.
5.3 HRV Features
We computed heart-rate variability (HRV) from inter-beat interval (IBI) data recorded by the wearable.
HRV is a well-established marker of autonomic balance and gets used often in stress assessment. Reduced HRV usually points to sympathetic dominance and higher psychological stress.
We extracted the following HRV biomarkers when there was enough IBI data available:
Time-Domain HRV Features
Mean NN interval
SDNN (Standard Deviation of NN intervals)
RMSSD (Root Mean Square of Successive Differences)
SDNN reflects overall heart-rate variability, while RMSSD mostly tracks parasympathetic activity.
Frequency-Domain HRV Features
We ran frequency-domain HRV analysis through power spectral estimation, extracting:
Low-Frequency Power (LF)
High-Frequency Power (HF)
LF/HF Ratio
We included the LF/HF ratio because it's commonly read as an indicator of sympathovagal balance.
We computed all HRV features separately for each exam phase, which lets us look at how autonomic regulation changes over the course of an exam.

6. Model Development
The goal here was to classify exam outcomes from multimodal physiological biomarkers while keeping subject-specific information from leaking into the model.
Figure 5 shows the full pipeline. After feature extraction, the steps were:
ANOVA-based feature selection
Synthetic Minority Oversampling Technique (SMOTE)
XGBoost classification
Leave-One-Subject-Out cross-validation
SHAP-based interpretation
6.1 XGBoost Framework

We chose Extreme Gradient Boosting (XGBoost) as the main classifier because it performs well on high-dimensional tabular data and can model nonlinear interactions between physiological variables.
XGBoost builds an ensemble of decision trees one at a time, with each new tree trying to correct the errors left by the previous ones.
For a dataset with $N$ observations and $M$ features, the prediction is:
$$\hat{y}i=\sum{k=1}^{K}f_k(x_i)$$
where $f_k$ is the $k^{th}$ decision tree.
A few properties make XGBoost a good fit for wearable physiological data:
Handles nonlinear relationships well
Models feature interactions automatically
Includes regularization to limit overfitting
Works well in high-dimensional feature spaces
Has built-in feature importance analysis
Because the dataset has relatively few subjects but a lot of candidate features, gradient boosting gives a better bias-variance tradeoff here than many conventional classifiers.
Earlier studies on the Wearable Exam Stress Dataset mostly used kNN, SVM, Random Forest, and MLP architectures. We extend that line of work with an XGBoost-based framework built specifically for phase-aware physiological modeling.
6.2 Cross Validation Strategy
Subject leakage is a real concern in physiological machine learning. If recordings from the same person show up in both training and test sets, the model can end up learning that person's physiological signature instead of general stress patterns.
We used Leave-One-Subject-Out Cross Validation (LOSO-CV) to avoid this.
For each fold:
We held out one student's exams entirely as the test set.
We trained on all the remaining students.
We ran feature selection and SMOTE only within the training partition.
We evaluated the trained model on the held-out subject.
We repeated this until every participant had served as the test subject exactly once.
LOSO-CV gives a realistic sense of how well the model generalizes, since it has to predict outcomes for people it never saw during training.
6.3 Hyperparameter Optimization
We tuned hyperparameters within the training data during cross-validation. The search space included:
Parameter
Search Range
n_estimators
50–500
max_depth
2–8
learning_rate
0.01–0.30
subsample
0.5–1.0
colsample_bytree
0.5–1.0
min_child_weight
1–10
gamma
0–5

We picked the final configuration based on validation AUC.
We ran ANOVA ranking for feature selection before training and kept only the highest-ranked features. We then applied SMOTE to address class imbalance, so both classes were represented in roughly equal numbers during training.

7. Results
7.1 Classification Performance
The phase-aware XGBoost framework reached an AUC of 0.801, showing it can meaningfully tell higher-performing exam outcomes apart from lower-performing ones.

Figure 1 shows the ROC curve.
Figure 3 shows the confusion matrix:

 Figure 3. Confusion matrix of the XGBoost classifier: true negatives (TN = 16), false positives (FP = 2), false negatives (FN = 4), true positives (TP = 8).
True Negatives (TN) = 16
False Positives (FP) = 2
False Negatives (FN) = 4
True Positives (TP) = 8
From these values:
Accuracy
$$Accuracy=\frac{TP+TN}{TP+TN+FP+FN}=\frac{8+16}{30}=0.800$$
Accuracy = 80.0%
Precision
$$Precision=\frac{TP}{TP+FP}=\frac{8}{10}=0.800$$
Precision = 80.0%
Recall (Sensitivity)
$$Recall=\frac{TP}{TP+FN}=\frac{8}{12}=0.667$$
Recall = 66.7%
Specificity
$$Specificity=\frac{TN}{TN+FP}=\frac{16}{18}=0.889$$
Specificity = 88.9%
F1-Score
$$F1=\frac{2PR}{P+R}=0.727$$
F1-Score = 72.7%

The model was better at catching negative-class exams than positive-class ones — specificity comes out higher than recall. That tracks with the confusion matrix in Figure 3, where only two exams got false-positive flags but four positive cases got missed.
Given the small dataset, an AUC of 0.801 holds up well against prior studies on this same dataset, which reported ROC-AUC values around 0.80–0.81 using more conventional machine learning approaches.

(incomplete)
7.2 SHAP Analysis
We interpreted the model with SHAP values; Figure 4 shows the resulting feature importance distribution.


The five most influential features were:
middle_TEMP_q1
end_ACC_X_skewness
middle_TEMP_shape_factor
end_TEMP_rms
end_ACC_X_pacf1
middle_TEMP_q1
The first quartile of skin temperature during the Middle Phase reflects the lower end of the temperature distribution during sustained exam engagement.
A lower lower-quartile temperature might point to peripheral vasoconstriction tied to sympathetic activation. A relatively higher one might instead point to better physiological regulation and less stress burden.
That this feature ranks so high suggests stable thermoregulation during prolonged cognitive workload carries real information about exam outcomes.
end_ACC_X_skewness
Skewness of accelerometer activity during the End Phase captures asymmetry in movement patterns.
Positive skewness points to occasional bursts of movement against an otherwise stable baseline — possibly fidgeting, posture shifts, or restlessness as stress and time pressure build near the end of the exam.
This suggests stress-related movement becomes more informative specifically in the final stretch of the exam.
middle_TEMP_shape_factor
Shape factor captures the relationship between RMS magnitude and average absolute temperature.
It reflects overall signal shape rather than absolute temperature level. Higher shape-factor values might point to more variable, less stable temperature during sustained cognitive effort.
Its importance suggests that how temperature moves matters more than where it sits.
end_TEMP_rms
RMS temperature reflects the overall magnitude of thermal activity during the End Phase.
Stress-driven changes in peripheral circulation can shift skin temperature distributions. Higher RMS values might point to sustained autonomic activation, lower values to more stable regulation.
This feature's importance points again to thermoregulatory biomarkers mattering during the later stretch of an exam.
end_ACC_X_pacf1
PACF1 measures the direct dependence between consecutive accelerometer readings.
Higher PACF values point to persistent movement patterns, lower values to more irregular activity.
This suggests that not just how much someone moves, but how that movement is structured over time, contributes to stress classification.


7.3 Phase-wise Biomarker Analysis
The SHAP results show a clear phase-dependent pattern. Among the five most influential features:
Two came from the Middle Phase.
Three came from the End Phase.
None came from the Beginning Phase.
That gives empirical support to the phase segmentation framework from Section 4.
Middle-phase temperature biomarkers seem to capture sustained cognitive workload and physiological adaptation during active problem-solving. End Phase biomarkers, by contrast, lean on both thermoregulatory and movement-related indicators, which suggests that approaching deadlines and finishing the exam bring on distinct physiological responses.
The absence of high-ranking Beginning Phase features might mean anticipatory stress varies more from person to person and so carries less consistent predictive value.
Overall, the SHAP analysis suggests exam stress changes over the course of an exam, and the strongest physiological signals show up later rather than earlier.
7.4 Permutation Test
To check whether model performance was better than chance, we ran a permutation test.
We shuffled class labels randomly while keeping the feature structure intact, then repeated the full training and validation pipeline across multiple permutations to build a null performance distribution.
We compared the observed AUC of 0.801 against this distribution.
Permutation Test Result:
Observed AUC = 0.801
Permutation p-value = 0.020
The permutation test gave p = 0.020, which suggests the observed performance was unlikely to come from random label assignments — evidence that the classifier picked up on real physiological patterns rather than noise.
7.5 LOEO Generalization Analysis
To check robustness further, we ran a Leave-One-Exam-Out (LOEO) evaluation.
Here, we excluded one complete exam session during training and tested on it instead. This checks whether the model generalizes across exam instances, not just across subjects.
LOEO Results:
Accuracy = [pending]
Precision = [pending]
Recall = [pending]
F1-Score = [pending]
AUC = [pending]
These results are still being finalized and should add more evidence about how stable the model is across different exam contexts.

8. Discussion
This study asked whether phase-aware physiological representations can improve stress classification on wearable exam data. The results suggest there is meaningful predictive information in multimodal physiological signals, and that temporal segmentation adds something beyond the usual whole-exam aggregation.
Temperature-derived biomarkers stand out as one of the main findings here. Earlier work on the Wearable Exam Stress Dataset already flagged skin temperature as one of the more informative modalities for predicting exam outcomes. Our results build on that by showing temperature features from specific phases of the exam carry more weight than the rest.
The SHAP analysis also shows that physiological signals get more informative during the Middle and End phases — which lines up with psychological theories of stress evolving over time rather than staying flat. Sustained cognitive workload probably dominates the Middle Phase, while deadline pressure takes over more in the End Phase.
Movement-related biomarkers turned out to matter too. Accelerometer-derived features ranked among the strongest predictors in the SHAP results, which matches earlier reports of these features showing up often in feature-selection analyses. We add a physiologically grounded explanation here, linking irregular movement to exam stress specifically.
An AUC of 0.801 is a solid result given how strict the validation protocol is. LOSO validation forces the model to generalize to people it's never seen, unlike approaches that might quietly benefit from subject leakage. That makes this performance a more realistic estimate of how the model would do in practice.
Methodologically, combining phase segmentation, ANOVA feature selection, SMOTE balancing, XGBoost classification, and SHAP interpretation gives a fairly complete framework for wearable stress analysis — one that produces both predictions and explanations, which matters for biomedical and educational applications.

9. Limitations
A few limitations are worth keeping in mind.
First, the dataset only includes ten participants and thirty exam sessions. LOSO validation helps, but a sample this small still limits statistical power and generalizability.
Second, every recording came from one academic setting — university exams. Physiological stress responses here might not transfer cleanly to workplace stress, social stress, or clinical anxiety.
Third, we used SMOTE to handle class imbalance. Synthetic oversampling helps with training stability, but the generated samples may not fully reflect physiological variability in real populations.
Fourth, even with HRV features included, the wearable gives lower-fidelity cardiovascular data than clinical-grade ECG, so some HRV estimates carry measurement uncertainty.
Fifth, the 25%-50%-25% phase split improved interpretability, but it's only one possible way to divide an exam temporally. Other segmentation schemes might surface different patterns.
Finally, the permutation testing and LOEO analyses are still being finalized. They should clarify the statistical robustness and generalizability of this framework further.

10. Conclusion
This study presented a phase-aware wearable stress classification framework built on multimodal physiological signals recorded during real university exams.
Instead of aggregating physiological information across an entire exam, we modeled temporal stress dynamics explicitly through Beginning, Middle, and End phases. We extracted statistical, spectral, and HRV biomarkers from each phase and trained an XGBoost classifier within a subject-independent validation setup.
The approach reached an AUC of 0.801, with accuracy at 80.0%, precision at 80.0%, recall at 66.7%, specificity at 88.9%, and an F1-score of 72.7%. SHAP analysis showed temperature and accelerometer-derived biomarkers from the Middle and End phases mattered most for classification.
These findings point toward exam stress as a dynamic physiological process rather than a stationary state. Temporal segmentation surfaced phase-specific biomarkers that whole-exam analysis would likely have missed.
Future work should test these findings on larger cohorts, look into adaptive phase segmentation strategies, bring in more advanced HRV and EDA decomposition methods, and explore multimodal deep-learning architectures without losing interpretability. Phase-aware physiological modeling could eventually feed into wearable systems that track stress trajectories and support personalized interventions in school and workplace settings.

References
[1] M. R. Amin, D. S. Wickramasuriya, and R. T. Faghih, "A Wearable Exam Stress Dataset for Predicting Grades Using Physiological Signals," in Proc. 2022 IEEE Healthcare Innovations and Point of Care Technologies (HI-POCT), pp. 30–36, 2022. doi: 10.1109/HI-POCT54491.2022.9744065
[2] M. R. Amin, D. S. Wickramasuriya, and R. T. Faghih, "Wearable Exam Stress Dataset," PhysioNet, 2022. [Online]. Available: https://physionet.org/content/wearable-exam-stress/1.0.0/
[3] V. Abromavičius, A. Serackis, A. Katkevičius, M. Kazlauskas, and T. Sledevič, "Prediction of Exam Scores Using a Multi-Sensor Approach for Wearable Exam Stress Dataset with Uniform Preprocessing," Technology and Health Care, vol. 31, no. 6, pp. 2499–2511, 2023. doi: 10.3233/THC-235015
[4] W. Kang, S. Kim, E. Yoo, and S. Kim, "Predicting Students' Exam Scores Using Physiological Signals," arXiv:2301.12051, 2023. [Online]. Available: https://arxiv.org/abs/2301.12051
[5] T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining, pp. 785–794, 2016. doi: 10.1145/2939672.2939785
[6] S. M. Lundberg and S.-I. Lee, "A Unified Approach to Interpreting Model Predictions," in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017.
[7] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic Minority Over-sampling Technique," Journal of Artificial Intelligence Research, vol. 16, pp. 321–357, 2002. doi: 10.1613/jair.953
[8] P. D. Welch, "The Use of Fast Fourier Transform for the Estimation of Power Spectra: A Method Based on Time Averaging Over Short, Modified Periodograms," IEEE Transactions on Audio and Electroacoustics, vol. 15, no. 2, pp. 70–73, 1967. doi: 10.1109/TAU.1967.1161901
[9] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.
[10] C. R. Harris et al., "Array Programming with NumPy," Nature, vol. 585, pp. 357–362, 2020.
[11] P. Schmidt, A. Reiss, R. Duerichen, C. Marberger, and K. Van Laerhoven, "Introducing WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection," in Proc. 20th ACM Int. Conf. Multimodal Interaction (ICMI), pp. 400–408, 2018. [Online]. Available: https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection

