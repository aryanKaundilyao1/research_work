import React, { useState } from 'react';
import { 
  TestTube2, CheckCircle2, TrendingUp, TrendingDown, 
  Activity, BarChart2, Brain, Shield, 
  ChevronDown, ChevronUp, FileText, Image as ImageIcon,
  FileBarChart
} from 'lucide-react';

const experiments = [
  {
    id: "EXP-01",
    title: "Internal Source Validation (WESAD LOSO-CV)",
    status: "COMPLETED",
    borderColor: "border-emerald-500",
    icon: <Activity className="w-5 h-5 text-emerald-500" />,
    objective: "Establish the baseline internal accuracy of the absolute multimodal physiological representation within the source domain (WESAD, N=15). This experiment verifies that the chosen feature extraction, selection, and classification pipeline successfully captures meaningful physiological separation between baseline resting and stress states before attempting cross-dataset transfer.",
    methodology: "Leave-One-Subject-Out Cross-Validation (LOSO-CV) on WESAD. In each of 15 folds, one subject is held out as test. Global standard scaling, ANOVA F-value feature selection (K=20), and SMOTE class balancing are strictly nested within each training fold. XGBoost classifier (n_estimators=50, max_depth=3, learning_rate=0.05, subsample=0.8, reg_alpha=1.0).",
    inputData: "WESAD multimodal physiological data — EDA, BVP, TEMP, ACC — from 15 subjects (N=15), comprising 9,034,272 sensor observations across 877 quality-controlled 60-second windows with 30-second overlap.",
    results: [
      { label: "ROC-AUC", value: "0.964" },
      { label: "Balanced Accuracy", value: "0.933" },
      { label: "F1 Score", value: "0.933" }
    ],
    interpretation: "Strong internal performance confirmed the pipeline can separate baseline from stress within WESAD. However, this does NOT guarantee cross-dataset transferability.",
    figures: [
      "reports/experiment_1/outputs/roc_curve.png",
      "reports/experiment_1/outputs/pr_curve.png",
      "reports/experiment_1/outputs/confusion_matrix.png",
      "reports/experiment_1/outputs/per_subject_performance.png"
    ],
    dataFiles: [
      "reports/experiment_1/outputs/experiment_1_fold_results.csv",
      "reports/experiment_1/results/experiment_1_subject_results.csv"
    ]
  },
  {
    id: "EXP-02",
    title: "Domain-Shift Diagnostic (Accelerometer)",
    status: "COMPLETED",
    borderColor: "border-amber-500",
    icon: <TrendingDown className="w-5 h-5 text-amber-500" />,
    objective: "Quantify the distributional shift in accelerometer features between source (WESAD) and target (Dataset B) domains to diagnose modality-specific contributions to domain mismatch.",
    methodology: "Compute Cohen's d effect size between the mean Z-axis accelerometer feature distributions of WESAD and Dataset B. Large |d| values (>0.8) indicate substantial domain shift.",
    inputData: "Accelerometer features extracted from both WESAD (N=15) and Dataset B (evaluated N=31) under identical windowing parameters (60s windows, 30s step).",
    results: [
      { label: "Cohen's d", value: "−1.47" }
    ],
    interpretation: "The large effect size confirms substantial accelerometer distribution shift consistent with protocol-related movement differences. Laboratory TSST elicits different physical behaviors than classroom examinations. The model partially encoded dataset-specific physical signatures rather than generalizable stress physiology.",
    figures: [],
    dataFiles: [
      "reports/experiment_3/results/feature_distribution_shift.csv"
    ]
  },
  {
    id: "EXP-03",
    title: "External Absolute Transfer",
    status: "COMPLETED",
    borderColor: "border-red-500",
    icon: <TrendingDown className="w-5 h-5 text-red-500" />,
    objective: "Evaluate whether the frozen WESAD-trained model can generalize to an independent target dataset (Dataset B) using the absolute multimodal representation, without any target-domain adaptation.",
    methodology: "Complete WESAD pipeline (global standard scaler, ANOVA K=20, SMOTE, XGBoost) fitted on 100% of WESAD data and mathematically frozen. Applied directly to Dataset B's absolute multimodal features. No target labels used.",
    inputData: "Dataset B multimodal data (EDA, BVP, TEMP, ACC) from 31 evaluated subjects (N=31), comprising 9,514,291 sensor observations across 1,591 quality-controlled windows.",
    results: [
      { label: "ROC-AUC", value: "0.423" },
      { label: "Balanced Accuracy", value: "0.441" }
    ],
    interpretation: "Dramatic performance inversion (0.964 → 0.423) conclusively demonstrates that strong internal validation does NOT guarantee cross-dataset generalization. The absolute representation suffered severe domain mismatch, performing WORSE than random chance.",
    figures: [
      "reports/experiment_3/outputs/external_roc_curve.png",
      "reports/experiment_3/outputs/external_pr_curve.png",
      "reports/experiment_3/outputs/external_confusion_matrix.png",
      "reports/experiment_3/outputs/external_per_subject_performance.png"
    ],
    dataFiles: [
      "reports/experiment_3/results/experiment3_external_results.csv",
      "reports/experiment_3/results/experiment3_subject_results.csv"
    ]
  },
  {
    id: "EXP-04",
    title: "Accelerometer Ablation",
    status: "COMPLETED",
    borderColor: "border-amber-500",
    icon: <BarChart2 className="w-5 h-5 text-amber-500" />,
    objective: "Test whether removing the protocol-sensitive accelerometer modality improves cross-dataset transfer, isolating the contribution of motion artifacts.",
    methodology: "Identical to Experiment 3, but with ALL tri-axial accelerometer features removed. Representation restricted to autonomic indicators (EDA, BVP, TEMP). Pipeline refitted on WESAD without ACC and frozen.",
    inputData: "Dataset B physiological data (EDA, BVP, TEMP only) — ACC ablated.",
    results: [
      { label: "ROC-AUC", value: "0.540" },
      { label: "Balanced Accuracy", value: "0.514" }
    ],
    interpretation: "Removing accelerometry partially improved transfer (0.423 → 0.540), confirming motion artifacts contribute to domain mismatch. However, performance still barely above chance — absolute autonomic features also suffer cross-dataset shift. Modality ablation alone is insufficient.",
    figures: [
      "reports/experiment_2/outputs/ablation_roc_curve.png",
      "reports/experiment_2/outputs/ablation_pr_curve.png",
      "reports/experiment_2/outputs/ablation_subject_comparison.png"
    ],
    dataFiles: [
      "reports/experiment_4/results/experiment4_external_results.csv",
      "reports/experiment_4/results/experiment4_vs_experiment3.csv"
    ]
  },
  {
    id: "EXP-05",
    title: "Baseline-Relative External Transfer",
    status: "COMPLETED",
    borderColor: "border-emerald-500",
    icon: <TrendingUp className="w-5 h-5 text-emerald-500" />,
    objective: "Evaluate whether subject-specific baseline-relative features recover cross-dataset generalization via zero-shot stress-label transfer.",
    methodology: "For each target subject, continuous physiological signals (EDA, BVP, TEMP) standardized relative to that individual's unlabeled resting baseline using Z-score: z(t) = (x(t) − μ_base) / σ_base. Target stress labels strictly withheld. Frozen WESAD pipeline applied.",
    inputData: "Dataset B baseline-relative physiological data (EDA, BVP, TEMP) for 31 evaluated subjects, calibrated using each subject's unlabeled resting measurements.",
    results: [
      { label: "ROC-AUC", value: "1.000" },
      { label: "Balanced Accuracy", value: "0.970" },
      { label: "Sensitivity", value: "0.941" },
      { label: "Specificity", value: "1.000" }
    ],
    interpretation: "Perfect ROC-AUC discrimination recovered from catastrophic failure. Isolating relative physiological changes from absolute interpersonal/dataset-level variance substantially mitigates cross-dataset domain mismatch. This constitutes label-free zero-shot transfer.",
    figures: [
      "reports/experiment_5/outputs/experiment5_subject_performance.png",
      "reports/experiment_5/outputs/experiment5_task_probabilities.png",
      "reports/experiment_5/outputs/baseline_relative_signal_comparison.png",
      "figures/final_submission/Figure_3_Macro_AUROC_Comparison.png"
    ],
    dataFiles: [
      "reports/experiment_5/results/experiment5_external_results.csv",
      "reports/experiment_5/results/experiment5_subject_results.csv",
      "reports/experiment_5/results/experiment5_vs_exp3_exp4.csv"
    ]
  },
  {
    id: "EXP-06",
    title: "Cross-Dataset SHAP Attribution",
    status: "COMPLETED",
    borderColor: "border-emerald-500",
    icon: <Brain className="w-5 h-5 text-emerald-500" />,
    objective: "Determine whether the baseline-relative model relies on consistent feature attribution structure across source and target domains.",
    methodology: "SHAP values extracted for both WESAD and Dataset B evaluations. Mean absolute SHAP values generated global feature importance rankings. Agreement quantified via Spearman rank correlation (ρ) and Top-20 Jaccard similarity.",
    inputData: "Baseline-relative model predictions on WESAD and Dataset B.",
    results: [
      { label: "Spearman ρ", value: "0.9527" },
      { label: "Top-20 Jaccard", value: "1.000" }
    ],
    interpretation: "Near-perfect rank correlation and perfect Top-20 overlap indicate the model's decision structure is highly conserved across domains. The model relies on the same relative physiological features in both datasets.",
    figures: [
      "reports/experiment_6/outputs/feature_level_agreement.png",
      "reports/experiment_6/outputs/shap_beeswarm_wesad.png",
      "reports/experiment_6/outputs/shap_beeswarm_datasetB.png",
      "reports/experiment_6/outputs/modality_shap_comparison.png",
      "figures/final_submission/Figure_10_SHAP_Rank_Comparison.png"
    ],
    dataFiles: [
      "reports/experiment_6/results/shap_feature_ranking.csv",
      "reports/experiment_6/results/feature_level_agreement.csv"
    ]
  }
];

const robustnessChecks = [
  {
    id: "ROB-01",
    title: "Subject-Level Bootstrap",
    status: "COMPLETED",
    borderColor: "border-emerald-500",
    methodology: "5000-iteration subject-level bootstrap resampling on baseline-relative predictions from 31 target subjects.",
    results: "95% CI [1.000, 1.000]",
    interpretation: "Confirming separation is robust to subject-level variance.",
    figures: ["reports/final_hardening/subject_margin_plot.png"],
    dataFiles: ["reports/final_hardening/bootstrap_results.csv"]
  },
  {
    id: "ROB-02",
    title: "Task-Level Permutation",
    status: "COMPLETED",
    borderColor: "border-emerald-500",
    methodology: "1000-iteration permutation test — randomly shuffled subject-level condition labels against fixed model predictions.",
    results: "0/1000 permutations ≥ observed AUC (p < 0.001)",
    interpretation: "Statistically significant validation of task separation.",
    figures: ["reports/final_hardening/permutation_null_distribution.png"],
    dataFiles: []
  }
];

const ExperimentCard = ({ exp }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden mb-6 border-l-4 ${exp.borderColor}`}>
      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center gap-3">
            {exp.icon}
            <div>
              <span className="inline-block px-2 py-1 bg-slate-100 text-slate-600 text-xs font-mono font-semibold rounded mb-1">
                {exp.id}
              </span>
              <h3 className="text-xl font-bold text-slate-800">{exp.title}</h3>
            </div>
          </div>
          <span className="flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 text-sm font-semibold rounded-full border border-emerald-200">
            <CheckCircle2 className="w-4 h-4" />
            {exp.status}
          </span>
        </div>

        <div className="mb-6">
          <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Objective</h4>
          <p className="text-slate-700 leading-relaxed">{exp.objective}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-slate-50 p-4 rounded-lg border border-slate-100">
            <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Key Results</h4>
            <div className="flex flex-wrap gap-6">
              {exp.results.map((res, i) => (
                <div key={i}>
                  <div className="text-sm text-slate-500 mb-1">{res.label}</div>
                  <div className="text-2xl font-bold text-slate-800">{res.value}</div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Interpretation</h4>
            <p className="text-slate-700 text-sm leading-relaxed">{exp.interpretation}</p>
          </div>
        </div>

        <button 
          onClick={() => setExpanded(!expanded)}
          className="flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors"
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          {expanded ? "Hide Methodology & Files" : "View Methodology & Files"}
        </button>

        {expanded && (
          <div className="mt-6 pt-6 border-t border-slate-100 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="mb-4">
                <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Methodology</h4>
                <p className="text-sm text-slate-700 leading-relaxed">{exp.methodology}</p>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Input Data</h4>
                <p className="text-sm text-slate-700 leading-relaxed">{exp.inputData}</p>
              </div>
            </div>
            
            <div>
              {exp.figures && exp.figures.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <ImageIcon className="w-4 h-4" /> Figures
                  </h4>
                  <ul className="space-y-2">
                    {exp.figures.map((fig, i) => (
                      <li key={i} className="text-sm text-slate-600 flex items-start gap-2 bg-slate-50 p-2 rounded border border-slate-100 break-all">
                        <ImageIcon className="w-4 h-4 mt-0.5 text-slate-400 flex-shrink-0" />
                        {fig}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {exp.dataFiles && exp.dataFiles.length > 0 && (
                <div>
                  <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <FileText className="w-4 h-4" /> Data Files
                  </h4>
                  <ul className="space-y-2">
                    {exp.dataFiles.map((file, i) => (
                      <li key={i} className="text-sm text-slate-600 flex items-start gap-2 bg-slate-50 p-2 rounded border border-slate-100 break-all">
                        <FileBarChart className="w-4 h-4 mt-0.5 text-slate-400 flex-shrink-0" />
                        {file}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const RobustnessCard = ({ rob }) => {
  return (
    <div className={`bg-white rounded-lg shadow-sm border border-slate-200 p-5 mb-4 border-l-4 ${rob.borderColor}`}>
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-emerald-500" />
          <span className="inline-block px-2 py-0.5 bg-slate-100 text-slate-600 text-xs font-mono font-semibold rounded">
            {rob.id}
          </span>
          <h3 className="text-lg font-bold text-slate-800">{rob.title}</h3>
        </div>
        <span className="flex items-center gap-1 px-2 py-0.5 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-full border border-emerald-200">
          <CheckCircle2 className="w-3 h-3" />
          {rob.status}
        </span>
      </div>
      <div className="text-sm text-slate-700 mb-3 leading-relaxed">
        <strong>Methodology:</strong> {rob.methodology}
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-50 p-3 rounded">
          <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-1">Results</div>
          <div className="font-bold text-slate-800">{rob.results}</div>
        </div>
        <div className="bg-slate-50 p-3 rounded">
          <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-1">Interpretation</div>
          <div className="text-sm text-slate-700">{rob.interpretation}</div>
        </div>
      </div>
    </div>
  );
};

export default function Experiments() {
  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3 mb-2">
            <TestTube2 className="w-8 h-8 text-blue-600" />
            Experimental Pipeline Results
          </h1>
          <p className="text-slate-600 text-lg">
            Comprehensive validation of multimodal physiological representations across source and target domains.
          </p>
        </div>

        {/* Summary Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
            <TestTube2 className="w-6 h-6 text-blue-500 mb-2" />
            <div className="text-3xl font-bold text-slate-800">6</div>
            <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mt-1">Canonical Experiments</div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
            <Activity className="w-6 h-6 text-rose-500 mb-2" />
            <div className="text-3xl font-bold text-slate-800">50</div>
            <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mt-1">Total Participants</div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
            <BarChart2 className="w-6 h-6 text-indigo-500 mb-2" />
            <div className="text-3xl font-bold text-slate-800">~18.55M</div>
            <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mt-1">Sensor Observations</div>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
            <Shield className="w-6 h-6 text-emerald-500 mb-2" />
            <div className="text-3xl font-bold text-slate-800">8</div>
            <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mt-1">Robustness Checks</div>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-slate-800 mb-6 border-b border-slate-200 pb-2">Canonical Experiments</h2>
          {experiments.map(exp => (
            <ExperimentCard key={exp.id} exp={exp} />
          ))}
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold text-slate-800 mb-6 border-b border-slate-200 pb-2">Robustness & Validation</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {robustnessChecks.map(rob => (
              <RobustnessCard key={rob.id} rob={rob} />
            ))}
          </div>
        </div>

        {/* Results Summary Table (Table 7.1 Equivalent) */}
        <div className="mb-12 bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h2 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
            <FileBarChart className="w-5 h-5 text-slate-500" />
            Table 7.1: Summary of Cross-Dataset Generalization Results
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-600 text-sm uppercase tracking-wider border-b-2 border-slate-200">
                  <th className="py-3 px-4 font-semibold">Experiment</th>
                  <th className="py-3 px-4 font-semibold">Modality</th>
                  <th className="py-3 px-4 font-semibold">Representation</th>
                  <th className="py-3 px-4 font-semibold">Target Domain</th>
                  <th className="py-3 px-4 font-semibold text-right">ROC-AUC</th>
                  <th className="py-3 px-4 font-semibold text-right">Bal. Acc</th>
                </tr>
              </thead>
              <tbody className="text-sm text-slate-700">
                <tr className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="py-3 px-4 font-medium">Exp 1: Internal Validate</td>
                  <td className="py-3 px-4">EDA, BVP, TEMP, ACC</td>
                  <td className="py-3 px-4">Absolute</td>
                  <td className="py-3 px-4">WESAD (CV)</td>
                  <td className="py-3 px-4 text-right font-mono font-bold text-emerald-600">0.964</td>
                  <td className="py-3 px-4 text-right font-mono font-bold text-emerald-600">0.933</td>
                </tr>
                <tr className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="py-3 px-4 font-medium">Exp 3: External Absolute</td>
                  <td className="py-3 px-4">EDA, BVP, TEMP, ACC</td>
                  <td className="py-3 px-4">Absolute</td>
                  <td className="py-3 px-4">Dataset B</td>
                  <td className="py-3 px-4 text-right font-mono font-bold text-red-600">0.423</td>
                  <td className="py-3 px-4 text-right font-mono font-bold text-red-600">0.441</td>
                </tr>
                <tr className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="py-3 px-4 font-medium">Exp 4: ACC Ablation</td>
                  <td className="py-3 px-4">EDA, BVP, TEMP</td>
                  <td className="py-3 px-4">Absolute</td>
                  <td className="py-3 px-4">Dataset B</td>
                  <td className="py-3 px-4 text-right font-mono text-amber-600">0.540</td>
                  <td className="py-3 px-4 text-right font-mono text-amber-600">0.514</td>
                </tr>
                <tr className="hover:bg-slate-50 bg-emerald-50/30">
                  <td className="py-3 px-4 font-medium">Exp 5: Baseline-Relative</td>
                  <td className="py-3 px-4">EDA, BVP, TEMP</td>
                  <td className="py-3 px-4">Relative</td>
                  <td className="py-3 px-4">Dataset B</td>
                  <td className="py-3 px-4 text-right font-mono font-bold text-emerald-600">1.000</td>
                  <td className="py-3 px-4 text-right font-mono font-bold text-emerald-600">0.970</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
      </div>
    </div>
  );
}
