import React from 'react';
import { TestTube2 } from 'lucide-react';

const Experiments = () => {
  const exps = [
    {
      id: 'E1', title: 'Dataset Utilization',
      objective: 'Define data volume and primary unit of inference',
      input: 'WESAD (N=15) & Target (N=35)',
      eval: 'Summary Statistics', result: '~18.55M samples across 50 subjects'
    },
    {
      id: 'E2', title: 'Internal Source Validation',
      objective: 'Establish baseline absolute performance',
      input: 'WESAD Absolute Features',
      eval: 'LOSO-CV', result: 'ROC-AUC = 0.964'
    },
    {
      id: 'E3', title: 'Corrected Absolute Transfer',
      objective: 'Evaluate strict zero-shot absolute generalizability',
      input: 'Dataset B Absolute Features',
      eval: 'Zero-Shot Strict Evaluation', result: 'Pending Final Script'
    },
    {
      id: 'E4', title: 'Calibration-Exclusive Baseline Transfer',
      objective: 'Mitigate domain shift with label-free relative baseline (Leak-Free)',
      input: 'Dataset B (N=35) Strict 60s Z-Score',
      eval: 'Subject-Level Verification', result: 'ROC-AUC = 0.745'
    },
    {
      id: 'E5', title: 'Calibration-Duration Sensitivity',
      objective: 'Evaluate effect of baseline context size',
      input: 'Dataset B (30s, 60s, 120s, 300s)',
      eval: 'Subject-Level AUROC/Brier', result: 'Pending Final Script'
    },
    {
      id: 'E6', title: 'Normalization Comparison',
      objective: 'Benchmark 8 different global and subject-wise norms',
      input: 'Dataset B',
      eval: 'ROC-AUC & Precision-Recall', result: 'Pending Final Script'
    },
    {
      id: 'E7', title: 'Domain Shift',
      objective: 'Quantify cross-dataset modality distributions',
      input: 'All modalities (ACC, EDA, BVP, TEMP)',
      eval: "Cohen's d, KS, Wasserstein, MMD", result: 'Pending Final Script'
    },
    {
      id: 'E8', title: 'Modality Ablation',
      objective: 'Isolate modality contributions and confounders',
      input: 'Dataset B (9 combinations)',
      eval: 'Subject-Level Validation', result: 'Pending Final Script'
    },
    {
      id: 'E9', title: 'Classifier Robustness',
      objective: 'Test representation superiority across ML models',
      input: 'LR, SVM, RF, XGBoost',
      eval: 'Zero-shot performance', result: 'Pending Final Script'
    },
    {
      id: 'E10', title: 'Feature-Selection Sensitivity',
      objective: 'Test K={5,10,15,20,30,50,All}',
      input: 'WESAD CV Optimization',
      eval: 'Stability and Performance', result: 'Pending Final Script'
    },
    {
      id: 'E11', title: 'Subject-Level Evaluation',
      objective: 'Analyze inter-subject variability',
      input: 'Dataset B (N=35)',
      eval: 'Individual AUROC Distribution', result: 'Pending Final Script'
    },
    {
      id: 'E12', title: 'Task/Stressor Analysis',
      objective: 'Verify performance across specific stressors',
      input: 'Stroop, TMCT, Real/Opposite Opinion, Subtract',
      eval: 'Prediction means & 95% CI', result: 'Pending Final Script'
    },
    {
      id: 'E13', title: 'Protocol V1/V2 Analysis',
      objective: 'Investigate protocol order effect',
      input: 'Dataset B (V1 vs V2 Cohort)',
      eval: 'Cohort-level Metrics', result: 'Pending Final Script'
    },
    {
      id: 'E14', title: 'Bootstrap',
      objective: 'Derive non-parametric 95% confidence intervals',
      input: '5000 Iterations (Subject-level Resampling)',
      eval: 'Percentile CI', result: 'Pending Final Script'
    },
    {
      id: 'E15', title: 'Permutation',
      objective: 'Assess null distribution significance',
      input: '1000 Iterations',
      eval: 'Exact p-value', result: 'Pending Final Script'
    },
    {
      id: 'E16', title: 'SHAP Stability',
      objective: 'Compare attribution across domains robustly',
      input: 'Spearman rho, Kendall tau',
      eval: 'Correlation', result: 'Pending Final Script'
    },
    {
      id: 'E17', title: 'Deployment',
      objective: 'Assess computational cost',
      input: 'Feature Extraction & Prediction',
      eval: 'Latency & Memory', result: 'Pending Final Script'
    },
    {
      id: 'E18', title: 'Additional Dataset Feasibility',
      objective: 'Assess replication viability',
      input: 'SWELL-KW, ForDigitStress',
      eval: 'Harmonization Score', result: 'Pending Final Script'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-slate-800 flex items-center gap-2">
        <TestTube2 className="text-purple-500" /> Experimental Suite (Rebuild)
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {exps.map(exp => (
          <div key={exp.id} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col h-full hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-bold rounded-md">{exp.id}</span>
            </div>
            <h3 className="text-lg font-bold text-slate-800 mb-2 leading-tight">{exp.title}</h3>
            
            <div className="flex-1 space-y-3 mt-2">
              <div>
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Objective</span>
                <p className="text-sm text-slate-700">{exp.objective}</p>
              </div>
              <div>
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Input Data</span>
                <p className="text-sm text-slate-700">{exp.input}</p>
              </div>
              <div>
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Evaluation</span>
                <p className="text-sm text-slate-700">{exp.eval}</p>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">Result</span>
              <div className="text-sm font-mono font-bold text-emerald-600 bg-emerald-50 px-3 py-2 rounded-lg inline-block break-words max-w-full">
                {exp.result}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Experiments;
