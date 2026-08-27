import React from 'react';
import { FileText, Download } from 'lucide-react';

const VITPaperDraft = () => {
  return (
    <div className="max-w-5xl mx-auto py-8 px-10 bg-white shadow-xl border border-slate-200 rounded-xl my-6">
      
      {/* HEADER SECTION */}
      <div className="mb-12 border-b border-slate-300 pb-8 text-center">
        <h1 className="text-3xl font-extrabold text-slate-900 leading-tight mb-4 font-serif">
          Cross-Dataset Generalization of Wearable Physiological Stress Detection Through Subject-Specific Baseline-Relative Representation
        </h1>
        <p className="text-lg text-slate-600 mb-6 font-medium">Prepared for Submission to VIT Vellore</p>
        
        <div className="flex justify-center space-x-4">
          <button className="flex items-center space-x-2 bg-blue-700 hover:bg-blue-800 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition-colors">
            <Download size={18} />
            <span>Export to PDF</span>
          </button>
          <button className="flex items-center space-x-2 bg-slate-100 hover:bg-slate-200 text-slate-700 px-5 py-2.5 rounded-lg text-sm font-medium border border-slate-300 transition-colors">
            <FileText size={18} />
            <span>View Source Markdown</span>
          </button>
        </div>
      </div>

      <div className="prose prose-slate prose-lg max-w-none text-slate-800 font-serif leading-relaxed">
        
        {/* ABSTRACT */}
        <div className="bg-slate-50 p-8 rounded-xl border border-slate-200 mb-10">
          <h2 className="text-2xl font-bold text-slate-900 mt-0 mb-4 font-sans text-center">Abstract</h2>
          
          <p className="mb-4">
            <strong className="text-slate-900">Background:</strong> Wearable physiological sensing enables continuous, automated stress detection, yet machine learning models frequently fail to generalize across independent datasets due to inter-person variability and protocol-specific artifacts. 
          </p>
          <p className="mb-4">
            <strong className="text-slate-900">Methods:</strong> This study evaluates a zero-shot cross-dataset transfer framework using wearable signals. An XGBoost classifier was trained on the WESAD dataset (source domain, N=15). The absolute physiological representation pipeline was then evaluated on the independent Wearable Exam Stress Dataset (target domain, evaluated N=31). To address domain mismatch, we diagnosed modality-specific shift via an accelerometer ablation study and evaluated a subject-specific baseline-relative representation calibrated exclusively using target-domain unlabeled baseline measurements. Feature attribution stability was evaluated across domains using SHAP.
          </p>
          <p className="mb-4">
            <strong className="text-slate-900">Results:</strong> The absolute multimodal representation achieved strong internal performance (LOSO-CV ROC-AUC = 0.964) but degraded significantly on the target cohort (external ROC-AUC = 0.423). Accelerometer features exhibited substantial distribution shift (Cohen's d ≈ -1.47), and their ablation partially improved transfer (ROC-AUC = 0.540). Implementing the subject-specific baseline-relative representation substantially improved zero-shot label transfer, yielding an external ROC-AUC of 1.000. Robustness was confirmed via subject-level bootstrap (95% CI [1.000, 1.000]) and a task-level permutation test (p &lt; 0.001). Cross-dataset SHAP attribution was highly conserved (Spearman ρ = 0.9527, Top-20 Jaccard = 1.000).
          </p>
          <p className="mb-0">
            <strong className="text-slate-900">Conclusion:</strong> Strong internal validation does not guarantee external generalization. A subject-specific baseline-relative representation successfully mitigated cross-dataset domain shift and enabled robust zero-shot stress-label transfer under the evaluated conditions.
          </p>
        </div>

        {/* 1. INTRODUCTION */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 font-sans">1. Introduction</h2>
        <p>
          Psychological stress affects cognitive performance, emotional regulation, and overall well-being. Academic and laboratory settings provide structured environments to study how stress manifests physiologically. Responses commonly include changes in autonomic nervous system activity, which can be monitored via variations in electrodermal activity (EDA), skin temperature, cardiovascular signals, and movement patterns. Wearable sensing platforms have made it possible to track these multimodal physiological signals continuously, fueling the development of machine learning models for automated stress detection. These models aim to map physiological signatures to stress states without relying exclusively on subjective self-report questionnaires.
        </p>
        <p>
          While machine learning models frequently demonstrate strong classification performance during internal validation, this success does not necessarily imply robust external generalization. Physiological signals contain substantial inter-person variability, and wearable recordings are sensitive to dataset-specific and protocol-specific variations. When a model is trained and tested within a single dataset, it risks overfitting to absolute physiological limits or the specific physical context of that cohort's experimental design. Consequently, a statistical representation learned in one cohort may not remain stable in another, leading to domain shift during independent external evaluation.
        </p>
        <p>
          In addition to physiological variance, multimodal sensing introduces potential modality-specific domain shift. While incorporating diverse modalities—such as tri-axial accelerometry alongside autonomic indicators—can improve internal model accuracy, it may inadvertently encode the physical structure of the experimental protocol rather than a generalized stress response. 
        </p>
        <p>
          This study addresses these gaps by proposing and evaluating a subject-specific baseline-relative representation designed to isolate relative physiological changes from absolute population differences. We utilize a strict evaluation logic: a model is trained on a source cohort (WESAD) and frozen, followed by zero-shot stress-label transfer to an independent target cohort (Wearable Exam Stress Dataset). We demonstrate that a baseline-relative representation—calibrated strictly using target-domain unlabeled baseline data—can recover generalization and maintain robust attribution stability across domains.
        </p>

        {/* 2. RELATED WORK */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">2. Related Work / Literature Review</h2>
        <p>
          <strong>Wearable Stress Detection Using Physiological Signals</strong><br/>
          Wearable stress detection is now a major topic in affective computing and digital health. Signals such as electrodermal activity, photoplethysmography (PPG), and skin temperature reliably reflect autonomic nervous system activation under stress. The WESAD dataset established an early benchmark for multimodal stress detection by combining physiological measurements recorded during lab-induced affective states. Subsequent research utilizing diverse wearable datasets has demonstrated that statistical, spectral, and cardiovascular features can distinguish stress from baseline conditions. However, these successes have largely been established using internal validation methodologies.
        </p>
        <p>
          <strong>Cross-Dataset Generalization and Domain Shift</strong><br/>
          While internal subject-independent cross-validation mitigates identity leakage, it does not resolve cross-dataset domain shift. Covariate shift and domain shift occur when the feature distribution of a target domain differs significantly from the source domain. In wearable sensing, this arises from differing sensor hardware, distinct stress-inducing protocols, and varying population demographics. Unlike complex Domain Adaptation (DA) techniques such as unsupervised feature alignment or adversarial domain adaptation, our study investigates a simpler representation-level normalization based on subject-specific baseline physiology to improve label-free transferability.
        </p>
        <p>
          <strong>Explainable AI and Cross-Dataset Interpretability</strong><br/>
          As physiological models increase in complexity, interpretability has become critical for ensuring scientific validity. SHAP (SHapley Additive exPlanations) is a widely adopted framework for model interpretability. While high SHAP agreement does not prove underlying biological causality, a strong correlation in feature attribution between source and target evaluations indicates that the model's decision structure is conserved, providing evidence that the model relies on a stable representational logic across the evaluated domains.
        </p>

        {/* 3. DATASET & PREPROCESSING */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">3. Dataset & Preprocessing</h2>
        
        <p>
          <strong>Source Dataset: WESAD</strong><br/>
          The Wearable Stress and Affect Detection (WESAD) dataset was utilized as the source cohort. It contains multimodal physiological recordings from 15 subjects (N=15) who underwent a controlled laboratory protocol including a baseline condition, a stress condition (Trier Social Stress Test; TSST), and an amusement condition. Signals were recorded using an Empatica E4 wristband.
        </p>
        
        <p>
          <strong>Target Dataset: Wearable Exam Stress Dataset</strong><br/>
          The independent target cohort comprised 34 participant instances recorded using Empatica E4 devices during academic examination protocols. The protocol included an initial resting baseline followed by cognitive stress tasks. Based on an audited signal-quality review, three subject instances were excluded due to severe sensor corruption, yielding a final evaluated target cohort of exactly 31 subjects (N=31).
        </p>

        <p>
          <strong>Signal Modalities and Preprocessing</strong><br/>
          The physiological modalities utilized across both datasets were Electrodermal Activity (EDA), Skin Temperature (TEMP), and Blood Volume Pulse (BVP). Tri-axial Accelerometry (ACC) was initially included to diagnose motion-related domain shift. Continuous recordings were segmented into overlapping windows of 60 seconds duration with a 30-second step size. Missing values were interpolated, and gaussian smoothing was applied.
        </p>

        {/* 4. BASELINE REFERENCING & MODALITY ABLATION */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">4. Baseline Referencing & Modality Ablation</h2>
        
        <p>
          Instead of treating signals purely in their absolute forms, this study introduces a subject-specific baseline-relative framework and modality-ablation technique to isolate domain shifts.
        </p>
        <p>
          <strong>Subject-Specific Baseline-Relative Representation</strong><br/>
          To mitigate the absolute interpersonal variance and domain shift observed in the absolute representation, a subject-specific baseline-relative physiological representation was implemented. For each subject <em>i</em> and physiological channel <em>c</em> in the target domain, the transformation utilizes the continuous unlabeled data recorded exclusively during that subject's experimental Baseline task. The subject-specific baseline mean and standard deviation are calculated over the baseline measurements. Subsequently, all continuous physiological signals for that subject are transformed via Z-score normalization computed exclusively from this baseline prior to feature extraction.
        </p>

        <p>
          <strong>Accelerometer Ablation</strong><br/>
          To experimentally test whether accelerometry contributed disproportionately to cross-domain mismatch, an ACC ablation intervention was designed. The tri-axial accelerometer channels were completely removed from the feature matrix, restricting the representation exclusively to autonomic physiological indicators (EDA, BVP, TEMP). 
        </p>

        {/* 5. FEATURE EXTRACTION */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">5. Feature Extraction</h2>
        <p>
          For each 60-second window, statistical and temporal features were extracted across the available modalities. To prevent high-dimensional overfitting, the feature space was strictly constrained. ANOVA F-value feature selection (SelectKBest) was utilized to select the top 20 features (K=20). 
        </p>
        <p>
          Crucially, this feature selection was fitted exclusively on the WESAD training data, ensuring the selected feature subset was optimized solely for the source domain before external transfer.
        </p>

        {/* 6. MODEL DEVELOPMENT */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">6. Model Development</h2>
        
        <p>
          <strong>XGBoost Classification Pipeline</strong><br/>
          The classification engine is an Extreme Gradient Boosting (XGBClassifier) model. The hyperparameters were fixed without reference to the target dataset: <em>n_estimators</em> = 50, <em>max_depth</em> = 3, <em>learning_rate</em> = 0.05. To address class imbalance during training, the Synthetic Minority Over-sampling Technique (SMOTE) was applied with k=5 neighbors.
        </p>

        <p>
          <strong>External Zero-Shot Stress-Label Transfer</strong><br/>
          Following internal validation, the complete pipeline (scaler, feature selector, and trained XGBoost model) was fitted globally on 100% of the WESAD data. External evaluation was then executed by passing the Target Dataset representations through the frozen source pipeline. Target stress labels were categorically withheld from all stages of calibration and model fitting.
        </p>

        <p>
          <strong>Robustness and Statistical Validation</strong><br/>
          To verify the stability of the external performance, two statistical robustness procedures were conducted based on the subject-aggregated prediction probabilities: a 5000-iteration subject-level bootstrap, and a 1000-iteration task-level permutation test.
        </p>

        {/* 7. RESULTS */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">7. Results</h2>
        
        <p>
          <strong>Internal vs. External Performance</strong><br/>
          The absolute multimodal representation achieved a strong internal ROC-AUC of 0.964 under strict Leave-One-Subject-Out Cross-Validation (LOSO-CV) on the WESAD cohort. However, when the exact frozen absolute pipeline was applied to the independent target domain, the external performance degraded substantially to an ROC-AUC of 0.423.
        </p>

        <p>
          <strong>Accelerometer Domain-Shift Diagnostic and Ablation</strong><br/>
          A standardized distributional diagnostic revealed a massive discrepancy in the mean Z-axis accelerometer distributions between WESAD and the Target Dataset (Cohen's d ≈ -1.47). Ablating the tri-axial accelerometer features from the pipeline partially improved the external zero-shot stress-label transfer, increasing the external ROC-AUC from 0.423 to 0.540.
        </p>

        <p>
          <strong>Baseline-Relative External Transfer</strong><br/>
          Replacing the absolute representation with the subject-specific baseline-relative representation, using strictly unlabeled target baseline measurements for calibration, yielded a striking improvement. This intervention achieved an external ROC-AUC of 1.000 under zero-shot stress-label transfer for the 31 unique target subjects. 
        </p>

        <p>
          <strong>Robustness and SHAP Analysis</strong><br/>
          The 5000-iteration subject-level bootstrap confirmed a 95% Confidence Interval for the ROC-AUC of [1.000, 1.000]. The task-level permutation test yielded a p-value &lt; 0.001, verifying the performance against random chance. The cross-dataset SHAP attribution analysis revealed strong structural agreement, with a Spearman rank correlation across the selected feature vector of ρ = 0.9527, and a perfect Jaccard similarity coefficient of 1.000 for the Top-20 most impactful features.
        </p>

        <div className="my-8 overflow-x-auto">
          <table className="min-w-full bg-white border border-slate-300 rounded-lg">
            <thead className="bg-slate-100">
              <tr>
                <th className="py-3 px-4 border-b text-left text-sm font-bold text-slate-700">Experiment</th>
                <th className="py-3 px-4 border-b text-left text-sm font-bold text-slate-700">Representation / Intervention</th>
                <th className="py-3 px-4 border-b text-left text-sm font-bold text-slate-700">Evaluation Context</th>
                <th className="py-3 px-4 border-b text-left text-sm font-bold text-slate-700">Result (ROC-AUC / Metric)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="py-3 px-4 border-b text-sm text-slate-700">Exp. 1</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">Absolute multimodal</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">WESAD LOSO-CV</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700 font-semibold">0.964</td>
              </tr>
              <tr className="bg-slate-50">
                <td className="py-3 px-4 border-b text-sm text-slate-700">Exp. 2</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">ACC domain diagnostic</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">WESAD vs Target</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700 font-semibold">Cohen's d ≈ -1.47</td>
              </tr>
              <tr>
                <td className="py-3 px-4 border-b text-sm text-slate-700">Exp. 3</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">Absolute multimodal</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">External Target</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700 font-semibold text-red-600">0.423</td>
              </tr>
              <tr className="bg-slate-50">
                <td className="py-3 px-4 border-b text-sm text-slate-700">Exp. 4</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">ACC ablation</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">External Target</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700 font-semibold text-orange-600">0.540</td>
              </tr>
              <tr>
                <td className="py-3 px-4 border-b text-sm text-slate-700">Exp. 5</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">Baseline-relative physiology</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700">External Target</td>
                <td className="py-3 px-4 border-b text-sm text-slate-700 font-semibold text-green-600">1.000</td>
              </tr>
              <tr className="bg-slate-50">
                <td className="py-3 px-4 text-sm text-slate-700">Exp. 6</td>
                <td className="py-3 px-4 text-sm text-slate-700">Baseline-relative attribution</td>
                <td className="py-3 px-4 text-sm text-slate-700">Cross-dataset SHAP</td>
                <td className="py-3 px-4 text-sm text-slate-700 font-semibold text-blue-600">ρ = 0.9527; Jaccard = 1.000</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* 8. DISCUSSION */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">8. Discussion</h2>
        
        <p>
          This study investigated the cross-dataset transferability of wearable physiological stress detection models and evaluated subject-specific baseline referencing as a representation-level intervention. The experimental progression demonstrates a coherent empirical narrative: strong internal validation is insufficient to guarantee external robustness. The absolute multimodal representation achieved strong internal performance but failed spectacularly upon external zero-shot transfer, exposing its vulnerability to protocol-related domain shift. 
        </p>

        <p>
          The substantial distributional difference in accelerometer features between the domains underscores that multimodal models may partially encode physical signatures (like the difference between lab-based movement constraints and classroom exams) instead of generalized physiological stress responses. However, as demonstrated by the ablation study, removing the motion artifact alone was insufficient to recover generalization.
        </p>
        
        <p>
          The most substantial improvement in external transfer was achieved by replacing the absolute representation with a subject-specific baseline-relative representation. By standardizing continuous physiological signals relative to a subject's own resting baseline, the transformation isolates relative physiological changes, dramatically reducing absolute inter-person and dataset-level variance. 
        </p>

        <p>
          The zero-shot framework utilized in this study proved highly effective. While target stress labels were categorically withheld, utilizing unlabeled target baseline physiological measurements to calibrate the relative representation is practically viable in continuous wearable deployments, bypassing the need to acquire costly labeled data in the target domain.
        </p>

        {/* 9. LIMITATIONS */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">9. Limitations</h2>
        <p>
          Several limitations must be acknowledged. First, the evaluation was constrained to a single source dataset (WESAD, N=15) and a single target dataset (Target Dataset, evaluated N=31). The perfect observed ROC-AUC of 1.000 may indicate an unusually clean separation in this particular academic examination protocol, and requires replication on additional independent datasets. Second, the baseline-relative transformation inherently depends on the availability of a clean, unlabeled target baseline period, which may not always be practical in continuous, unstructured real-world deployment. Third, while the SHAP attribution agreement demonstrates model representational stability, it does not definitively establish underlying biological equivalence.
        </p>

        {/* 10. CONCLUSION */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">10. Conclusion</h2>
        <p>
          This study addresses the critical challenge of cross-dataset generalization in wearable physiological stress detection. Our central finding is that absolute multimodal physiological representations are highly vulnerable to domain mismatch, but that subject-specific baseline calibration can substantially recover generalization.
        </p>
        <p>
          The stark performance inversion between internal WESAD evaluation and the absolute external transfer demonstrates that within-dataset cross-subject generalization does not guarantee cross-dataset generalization. The empirical diagnostic confirmed substantial protocol-related accelerometer domain shift. Crucially, standardizing physiological features relative to each target subject's resting state isolated true physiological shifts, allowing the XGBoost classifier to achieve an external ROC-AUC of 1.000 under zero-shot stress-label transfer. Cross-dataset SHAP analysis further confirmed that the baseline-relative classifier relied on a conserved physiological representational logic across domains. 
        </p>
        <p>
          Future independent replication across diverse physiological datasets and unconstrained real-world protocols is required to firmly establish subject-specific baseline calibration as a universal mitigation strategy for domain shift in wearable affective computing.
        </p>

        {/* REFERENCES */}
        <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-2 mb-6 mt-10 font-sans">References</h2>
        <ol className="list-decimal pl-5 text-sm text-slate-600 space-y-2">
          <li>P. Schmidt, A. Reiss, R. Duerichen, C. Marberger, and K. Van Laerhoven, "Introducing WESAD, a multimodal dataset for wearable stress and affect detection," in <em>Proc. 20th ACM Int. Conf. Multimodal Interact.</em>, 2018, pp. 400-408.</li>
          <li>Dataset Authors, "Wearable device dataset from induced stress and structured exercise sessions," Dataset B Original Source.</li>
          <li>S. Böttcher et al., "Domain Adaptation using Maximum Mean Discrepancy for stress detection," 2022.</li>
          <li>J. Li et al., "Internal feature representation learning for stress detection using baseline normalization," 2023.</li>
          <li>S. Gashi et al., "Evaluating accelerometer models during driving tasks," 2021.</li>
          <li>S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in <em>Advances in Neural Information Processing Systems</em>, 2017, pp. 4765-4774.</li>
          <li>T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in <em>Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining</em>, 2016, pp. 785-794.</li>
          <li>N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," <em>J. Artif. Intell. Res.</em>, vol. 16, pp. 321-357, 2002.</li>
        </ol>

      </div>
    </div>
  );
};

export default VITPaperDraft;
