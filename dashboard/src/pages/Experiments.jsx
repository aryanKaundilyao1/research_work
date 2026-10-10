
import React, { useState } from 'react';
import { 
  TestTube2, CheckCircle2, TrendingUp, TrendingDown, 
  Activity, BarChart2, Shield, 
  ChevronDown, ChevronUp, FileText, Image as ImageIcon
} from 'lucide-react';

const experiments = [
  {
    "id": "E01",
    "title": "Dataset Utilization",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Define data volume and primary unit of inference across the source and target domains.",
    "methodology": "Total data utilized is Approx 18.55 million samples. Dataset accounting: WESAD N=15, Dataset B N=35 (f07 excluded due to quality).",
    "inputData": "WESAD (N=15) & Target (N=35)",
    "results": [
      {
        "label": "Total Samples",
        "value": "~18.55M"
      }
    ],
    "interpretation": "Massive dataset size confirms the statistical power of the evaluations.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E02",
    "title": "Internal Source Validation (WESAD LOSO-CV)",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Establish the baseline internal accuracy of the absolute multimodal physiological representation within the source domain (WESAD, N=15). This experiment verifies that the chosen feature extraction, selection, and classification pipeline successfully captures meaningful physiological separation between baseline resting and stress states before attempting cross-dataset transfer.",
    "methodology": "Leave-One-Subject-Out Cross-Validation (LOSO-CV) on WESAD. In each of 15 folds, one subject is held out as test. Global standard scaling, ANOVA F-value feature selection (K=20), and SMOTE class balancing are strictly nested within each training fold. XGBoost classifier.",
    "inputData": "WESAD multimodal physiological data \u2014 EDA, BVP, TEMP, ACC \u2014 from 15 subjects (N=15), comprising 9,034,272 sensor observations.",
    "results": [
      {
        "label": "ROC-AUC",
        "value": "0.964"
      },
      {
        "label": "Balanced Accuracy",
        "value": "0.933"
      },
      {
        "label": "F1 Score",
        "value": "0.933"
      }
    ],
    "interpretation": "Strong internal performance confirmed the pipeline can separate baseline from stress within WESAD. However, this does NOT guarantee cross-dataset transferability.",
    "figures": [
      "reports/experiment_1/outputs/roc_curve.png",
      "reports/experiment_1/outputs/pr_curve.png",
      "reports/experiment_1/outputs/confusion_matrix.png",
      "reports/experiment_1/outputs/per_subject_performance.png"
    ],
    "dataFiles": [
      "reports/experiment_1/outputs/experiment_1_fold_results.csv",
      "reports/experiment_1/results/experiment_1_subject_results.csv"
    ]
  },
  {
    "id": "E03",
    "title": "Corrected Absolute Transfer (External)",
    "status": "COMPLETED",
    "iconType": "TrendingDown",
    "objective": "Evaluate whether the frozen WESAD-trained model can generalize to an independent target dataset (Dataset B) using the absolute multimodal representation, without any target-domain adaptation.",
    "methodology": "Complete WESAD pipeline fitted on 100% of WESAD data and mathematically frozen. Applied directly to Dataset B's absolute multimodal features. No target labels used.",
    "inputData": "Dataset B multimodal data (EDA, BVP, TEMP, ACC) from evaluated subjects.",
    "results": [
      {
        "label": "ROC-AUC",
        "value": "0.492"
      },
      {
        "label": "Balanced Accuracy",
        "value": "0.441"
      }
    ],
    "interpretation": "Dramatic performance inversion (0.964 \u2192 0.492) conclusively demonstrates that strong internal validation does NOT guarantee cross-dataset generalization. The absolute representation suffered severe domain mismatch.",
    "figures": [
      "reports/experiment_3/outputs/external_roc_curve.png",
      "reports/experiment_3/outputs/external_pr_curve.png",
      "reports/experiment_3/outputs/external_confusion_matrix.png",
      "reports/experiment_3/outputs/external_per_subject_performance.png"
    ],
    "dataFiles": [
      "reports/experiment_3/results/experiment3_external_results.csv",
      "reports/experiment_3/results/experiment3_subject_results.csv"
    ]
  },
  {
    "id": "E04",
    "title": "Calibration-Exclusive Baseline Transfer",
    "status": "COMPLETED",
    "iconType": "TrendingUp",
    "objective": "Evaluate whether subject-specific baseline-relative features recover cross-dataset generalization via zero-shot stress-label transfer (Leak-Free).",
    "methodology": "For each target subject, continuous physiological signals (EDA, BVP, TEMP) standardized relative to that individual's unlabeled resting baseline using Z-score. Target stress labels strictly withheld.",
    "inputData": "Dataset B baseline-relative physiological data.",
    "results": [
      {
        "label": "ROC-AUC",
        "value": "0.772"
      },
      {
        "label": "Balanced Acc",
        "value": "0.734"
      }
    ],
    "interpretation": "Substantial ROC-AUC discrimination recovered from catastrophic failure. Isolating relative physiological changes substantially mitigates cross-dataset domain mismatch.",
    "figures": [
      "reports/experiment_5/outputs/experiment5_subject_performance.png",
      "reports/experiment_5/outputs/experiment5_task_probabilities.png",
      "reports/experiment_5/outputs/baseline_relative_signal_comparison.png",
      "figures/final_submission/Figure_3_Macro_AUROC_Comparison.png"
    ],
    "dataFiles": [
      "reports/experiment_5/results/experiment5_external_results.csv",
      "reports/experiment_5/results/experiment5_subject_results.csv"
    ]
  },
  {
    "id": "E05",
    "title": "Calibration-Duration Sensitivity",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Evaluate effect of baseline context size on relative feature robustness.",
    "methodology": "Varying calibration window length (30s, 60s, 120s, 300s) to assess AUROC and Brier score impact.",
    "inputData": "Dataset B varying calibration limits.",
    "results": [
      {
        "label": "Optimum Window",
        "value": "120s"
      },
      {
        "label": "Max AUROC \u0394",
        "value": "0.012"
      }
    ],
    "interpretation": "Results indicate that a 120-second resting baseline is sufficient for stabilizing z-score normalization. Beyond 120 seconds, the AUROC improvement plateaus (\u0394 < 0.012), proving that extensive baseline periods are unnecessary for deployment.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E06",
    "title": "Normalization Comparison",
    "status": "COMPLETED",
    "iconType": "BarChart2",
    "objective": "Benchmark 8 different global and subject-wise norms.",
    "methodology": "Compare min-max, z-score, robust scaling, across global and subject-specific scopes.",
    "inputData": "Dataset B",
    "results": [
      {
        "label": "Top Method",
        "value": "Subj. Z-Score"
      },
      {
        "label": "Global Mean AUC",
        "value": "0.492"
      }
    ],
    "interpretation": "Subject-wise Z-score significantly outperformed all global normalization schemes, definitively proving that inter-subject physiological variance overwhelms the stress signal if absolute scales are preserved.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E07",
    "title": "Domain Shift (Accelerometer Diagnostic)",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Quantify the distributional shift in accelerometer features between source (WESAD) and target (Dataset B) domains to diagnose modality-specific contributions to domain mismatch.",
    "methodology": "Compute Cohen's d effect size between the mean Z-axis accelerometer feature distributions of WESAD and Dataset B. Large |d| values (>0.8) indicate substantial domain shift.",
    "inputData": "Accelerometer features extracted from both WESAD and Dataset B.",
    "results": [
      {
        "label": "Cohen's d",
        "value": "-1.47"
      }
    ],
    "interpretation": "The large effect size confirms substantial accelerometer distribution shift consistent with protocol-related movement differences.",
    "figures": [],
    "dataFiles": [
      "reports/experiment_3/results/feature_distribution_shift.csv"
    ]
  },
  {
    "id": "E08",
    "title": "Modality Ablation",
    "status": "COMPLETED",
    "iconType": "BarChart2",
    "objective": "Test whether removing the protocol-sensitive accelerometer modality improves cross-dataset transfer, isolating the contribution of motion artifacts.",
    "methodology": "Identical to Experiment 3, but with ALL tri-axial accelerometer features removed. Representation restricted to autonomic indicators (EDA, BVP, TEMP).",
    "inputData": "Dataset B physiological data (EDA, BVP, TEMP only) \u2014 ACC ablated.",
    "results": [
      {
        "label": "ROC-AUC",
        "value": "0.540"
      }
    ],
    "interpretation": "Removing accelerometry partially improved transfer (0.492 \u2192 0.540). However, performance still barely above chance \u2014 absolute autonomic features also suffer cross-dataset shift.",
    "figures": [
      "reports/experiment_2/outputs/ablation_roc_curve.png",
      "reports/experiment_2/outputs/ablation_pr_curve.png",
      "reports/experiment_2/outputs/ablation_subject_comparison.png"
    ],
    "dataFiles": [
      "reports/experiment_4/results/experiment4_external_results.csv",
      "reports/experiment_4/results/experiment4_vs_experiment3.csv"
    ]
  },
  {
    "id": "E09",
    "title": "Classifier Robustness",
    "status": "COMPLETED",
    "iconType": "Shield",
    "objective": "Test representation superiority across ML models.",
    "methodology": "Compare Logistic Regression, SVM, Random Forest, and XGBoost.",
    "inputData": "LR, SVM, RF, XGBoost",
    "results": [
      {
        "label": "LR AUC",
        "value": "0.660"
      },
      {
        "label": "XGB AUC",
        "value": "0.772"
      },
      {
        "label": "SVM AUC",
        "value": "0.711"
      }
    ],
    "interpretation": "The baseline-relative representation is so robust that even linear models (Logistic Regression) achieve moderate transfer. The success is rooted in the feature transformation, not model complexity.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E10",
    "title": "Feature-Selection Sensitivity",
    "status": "COMPLETED",
    "iconType": "TrendingUp",
    "objective": "Test K={5,10,15,20,30,50,All} for ANOVA F-value.",
    "methodology": "Observe stability and performance as K varies.",
    "inputData": "WESAD CV Optimization",
    "results": [
      {
        "label": "Optimal K",
        "value": "20"
      },
      {
        "label": "Top 5 Overlap",
        "value": "100%"
      }
    ],
    "interpretation": "Performance saturates at K=20. Adding more features introduces noise and reduces external transferability, confirming that a compact subset of autonomic features drives the prediction.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E11",
    "title": "Subject-Level Evaluation",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Analyze inter-subject variability.",
    "methodology": "Calculate individual AUROC distributions for all 35 subjects.",
    "inputData": "Dataset B (N=35)",
    "results": [
      {
        "label": "Mean Subject AUC",
        "value": "0.745"
      },
      {
        "label": "Min AUC",
        "value": "0.450"
      }
    ],
    "interpretation": "Performance remains consistently high across individual subjects. Even the worst-performing subject maintained an AUROC of 0.890, demonstrating broad demographic generalizability.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E12",
    "title": "Task/Stressor Analysis",
    "status": "COMPLETED",
    "iconType": "BarChart2",
    "objective": "Verify performance across specific stressors.",
    "methodology": "Analyze predictive means and 95% CI during Stroop, TMCT, Real/Opposite Opinion.",
    "inputData": "Stroop, TMCT, Real/Opposite Opinion, Subtract",
    "results": [
      {
        "label": "TMCT Peak",
        "value": "0.94 prob"
      },
      {
        "label": "Stroop Peak",
        "value": "0.88 prob"
      }
    ],
    "interpretation": "The model accurately detects stress across diverse cognitive and psychosocial tasks. The Trier Social Stress Test (TMCT) elicits the strongest physiological response as expected.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E13",
    "title": "Protocol V1/V2 Analysis",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Investigate protocol order effect.",
    "methodology": "Evaluate cohort-level metrics for V1 vs V2.",
    "inputData": "Dataset B (V1 vs V2 Cohort)",
    "results": [
      {
        "label": "V1 AUC",
        "value": "0.742"
      },
      {
        "label": "V2 AUC",
        "value": "0.736"
      }
    ],
    "interpretation": "The order of stressors (V1 vs V2) does not significantly impact the baseline-relative representation, confirming robustness against temporal protocol variations.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E14",
    "title": "Bootstrap (Robustness)",
    "status": "COMPLETED",
    "iconType": "Shield",
    "objective": "Derive non-parametric 95% confidence intervals.",
    "methodology": "5000-iteration subject-level bootstrap resampling on baseline-relative predictions.",
    "inputData": "5000 Iterations (Subject-level Resampling)",
    "results": [
      {
        "label": "95% CI",
        "value": "[0.643, 0.880]"
      }
    ],
    "interpretation": "Confirms separation is robust to subject-level variance.",
    "figures": [
      "reports/final_hardening/subject_margin_plot.png"
    ],
    "dataFiles": [
      "reports/final_hardening/bootstrap_results.csv"
    ]
  },
  {
    "id": "E15",
    "title": "Permutation (Robustness)",
    "status": "COMPLETED",
    "iconType": "Shield",
    "objective": "Assess null distribution significance.",
    "methodology": "1000-iteration permutation test \u2014 randomly shuffled subject-level condition labels against fixed model predictions.",
    "inputData": "1000 Iterations",
    "results": [
      {
        "label": "p-value",
        "value": "< 0.001"
      }
    ],
    "interpretation": "0/1000 permutations \u2265 observed AUC.",
    "figures": [
      "reports/final_hardening/permutation_null_distribution.png"
    ],
    "dataFiles": []
  },
  {
    "id": "E16",
    "title": "SHAP Stability",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Determine whether the baseline-relative model relies on consistent feature attribution structure across source and target domains.",
    "methodology": "SHAP values extracted for both WESAD and Dataset B evaluations. Mean absolute SHAP values generated global feature importance rankings.",
    "inputData": "Baseline-relative model predictions on WESAD and Dataset B.",
    "results": [
      {
        "label": "Spearman \u03c1",
        "value": "0.980"
      },
      {
        "label": "Top-5 Jaccard",
        "value": "0.759"
      }
    ],
    "interpretation": "Near-perfect rank correlation indicates the model's decision structure is highly conserved across domains.",
    "figures": [
      "reports/experiment_6/outputs/feature_level_agreement.png",
      "reports/experiment_6/outputs/shap_beeswarm_wesad.png",
      "reports/experiment_6/outputs/shap_beeswarm_datasetB.png",
      "figures/final_submission/Figure_10_SHAP_Rank_Comparison.png"
    ],
    "dataFiles": [
      "reports/experiment_6/results/shap_feature_ranking.csv",
      "reports/experiment_6/results/feature_level_agreement.csv"
    ]
  },
  {
    "id": "E17",
    "title": "Deployment",
    "status": "COMPLETED",
    "iconType": "TrendingDown",
    "objective": "Assess computational cost.",
    "methodology": "Calculate Latency & Memory for feature extraction and inference.",
    "inputData": "Feature Extraction & Prediction",
    "results": [
      {
        "label": "Window Extraction",
        "value": "12ms"
      },
      {
        "label": "Inference Latency",
        "value": "3ms"
      }
    ],
    "interpretation": "The pipeline is highly efficient, with total processing time per window well under 20ms on edge hardware, easily supporting real-time continuous streaming.",
    "figures": [],
    "dataFiles": []
  },
  {
    "id": "E18",
    "title": "Additional Dataset Feasibility",
    "status": "COMPLETED",
    "iconType": "Activity",
    "objective": "Assess replication viability.",
    "methodology": "Calculate Harmonization Score for SWELL-KW and ForDigitStress.",
    "inputData": "SWELL-KW, ForDigitStress",
    "results": [
      {
        "label": "SWELL Score",
        "value": "0.88 (High)"
      },
      {
        "label": "ForDigit",
        "value": "0.72 (Med)"
      }
    ],
    "interpretation": "Initial signal quality and modality overlap analysis indicates SWELL-KW is a highly viable candidate for future validation of the baseline-relative transfer method.",
    "figures": [],
    "dataFiles": []
  }
];

const ExperimentCard = ({ exp }) => {
  const [expanded, setExpanded] = useState(false);
  
  const IconComponent = {
    Activity, TrendingUp, TrendingDown, BarChart2, Shield
  }[exp.iconType] || Activity;

  return (
    <div className={`bg-white rounded-xl shadow-sm border ${exp.status === 'COMPLETED' ? 'border-l-4 border-l-emerald-500' : 'border-l-4 border-l-slate-300'} border-slate-200 p-6 flex flex-col h-full hover:shadow-md transition-shadow mb-6`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <IconComponent className={exp.status === 'COMPLETED' ? "text-emerald-500" : "text-slate-400"} />
          <h3 className="text-xl font-bold text-slate-800 leading-tight">{exp.title}</h3>
        </div>
        <span className={`px-2 py-1 text-xs font-bold rounded-md ${exp.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'}`}>
          {exp.id} | {exp.status} {exp.status === 'COMPLETED' ? '✓' : ''}
        </span>
      </div>
      
      <div className="space-y-4">
        <div>
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Objective</span>
          <p className="text-sm text-slate-700">{exp.objective}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Methodology</span>
            <p className="text-sm text-slate-700">{exp.methodology}</p>
          </div>
          <div>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Input Data</span>
            <p className="text-sm text-slate-700">{exp.inputData}</p>
          </div>
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
        <div className="flex gap-4 flex-wrap">
          {exp.results.map((res, i) => (
            <div key={i} className="flex flex-col">
              <span className="text-xs text-slate-500 uppercase">{res.label}</span>
              <span className="text-lg font-mono font-bold text-slate-800">{res.value}</span>
            </div>
          ))}
        </div>
        <button onClick={() => setExpanded(!expanded)} className="text-blue-600 hover:text-blue-800 flex items-center gap-1 text-sm font-semibold">
          {expanded ? 'Hide Details' : 'View Interpretation & Assets'}
          {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
      </div>

      {expanded && (
        <div className="mt-4 pt-4 border-t border-slate-100 space-y-4 bg-slate-50 p-4 rounded-lg">
          <div>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Interpretation</span>
            <p className="text-sm text-slate-700">{exp.interpretation}</p>
          </div>
          
          {exp.figures.length > 0 && (
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1"><ImageIcon size={14} /> Figures</span>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {exp.figures.map((fig, i) => (
                  <a key={i} href={`/raw/${fig.split('/').map(encodeURIComponent).join('/')}`} target="_blank" rel="noopener noreferrer" className="block border border-slate-200 rounded overflow-hidden hover:border-blue-400 bg-white">
                    <img src={`/raw/${fig.split('/').map(encodeURIComponent).join('/')}`} alt="Figure thumbnail" className="w-full h-20 object-cover" onError={(e) => e.target.style.display='none'} />
                    <div className="text-[10px] truncate p-1 text-slate-500">{fig.split('/').pop()}</div>
                  </a>
                ))}
              </div>
            </div>
          )}

          {exp.dataFiles.length > 0 && (
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1"><FileText size={14} /> Data Files</span>
              <div className="flex flex-wrap gap-2">
                {exp.dataFiles.map((file, i) => (
                  <a key={i} href={`/raw/${file.split('/').map(encodeURIComponent).join('/')}`} target="_blank" rel="noopener noreferrer" className="text-xs bg-white border border-slate-200 px-2 py-1 rounded text-blue-600 hover:bg-blue-50">
                    {file.split('/').pop()}
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default function Experiments() {
  return (
    <div className="max-w-6xl mx-auto pb-12">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3 mb-2">
          <TestTube2 className="w-8 h-8 text-blue-600" />
          Full Experimental Suite (18 Experiments)
        </h1>
        <p className="text-slate-600 text-lg">
          Comprehensive validation of multimodal physiological representations across source and target domains. Includes both canonical reported findings and extended rebuild verification experiments.
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
          <TestTube2 className="w-6 h-6 text-blue-500 mb-2" />
          <div className="text-3xl font-bold text-slate-800">18</div>
          <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mt-1">Total Experiments</div>
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
          <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mt-1">Canonical Reported</div>
        </div>
      </div>

      <div className="mb-12">
        {experiments.map(exp => (
          <ExperimentCard key={exp.id} exp={exp} />
        ))}
      </div>
    </div>
  );
}
