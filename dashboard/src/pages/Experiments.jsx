import React from 'react';
import { TestTube2, Activity, Target } from 'lucide-react';

const Experiments = () => {
  const exps = [
    {
      id: 1, title: 'Internal Source Validation',
      objective: 'Establish baseline absolute performance',
      input: 'WESAD (N=15) Absolute Features',
      eval: 'LOSO-CV', result: 'ROC-AUC = 0.964'
    },
    {
      id: 2, title: 'Accelerometer Domain-Shift Diagnostic',
      objective: 'Quantify motion protocol differences',
      input: 'WESAD vs Dataset B ACC_Z',
      eval: 'Distributional Distance', result: "Cohen's d ≈ -1.47"
    },
    {
      id: 3, title: 'External Absolute Transfer',
      objective: 'Evaluate zero-shot domain generalization',
      input: 'Dataset B (N=31) Absolute Features',
      eval: 'Frozen Pipeline Zero-Shot', result: 'ROC-AUC = 0.423'
    },
    {
      id: 4, title: 'Accelerometer Ablation',
      objective: 'Isolate modality-specific confound',
      input: 'Dataset B (N=31) No ACC Features',
      eval: 'Frozen Pipeline Zero-Shot', result: 'ROC-AUC = 0.540'
    },
    {
      id: 5, title: 'Baseline-Relative External Transfer',
      objective: 'Mitigate domain shift via relative representation',
      input: 'Dataset B (N=31) Subject-Baseline Z-Score',
      eval: 'Zero-Shot Stress-Label Transfer', result: 'ROC-AUC = 1.000'
    },
    {
      id: 6, title: 'Cross-Dataset SHAP Attribution Agreement',
      objective: 'Validate model decision structure stability',
      input: 'WESAD SHAP vs Dataset B SHAP',
      eval: 'Rank Correlation / Overlap', result: 'ρ = 0.9527, Jaccard = 1.000'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-slate-800 flex items-center gap-2">
        <TestTube2 className="text-purple-500" /> Experimental Configurations
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {exps.map(exp => (
          <div key={exp.id} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col h-full hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-bold rounded-md">EXP {exp.id}</span>
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
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">Authoritative Result</span>
              <div className="text-lg font-mono font-bold text-emerald-600 bg-emerald-50 px-3 py-2 rounded-lg inline-block">
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
