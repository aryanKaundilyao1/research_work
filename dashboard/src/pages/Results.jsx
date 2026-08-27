import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { BarChart2, ShieldCheck, CheckCircle2 } from 'lucide-react';

const Results = () => {
  const aucData = [
    { name: 'Internal (Absolute)', auc: 0.964, color: '#3b82f6' }, // blue
    { name: 'External (Absolute)', auc: 0.423, color: '#ef4444' }, // red
    { name: 'External (ACC Ablation)', auc: 0.540, color: '#f59e0b' }, // amber
    { name: 'External (Relative)', auc: 1.000, color: '#10b981' }, // emerald
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
        <BarChart2 className="text-blue-500" /> Results Dashboard
      </h2>

      {/* Main Bar Chart */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h3 className="text-lg font-bold text-slate-800 mb-6">Cross-Dataset Transfer Performance (ROC-AUC)</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={aucData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
              <YAxis domain={[0, 1.1]} axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
              <Tooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
              <Bar dataKey="auc" radius={[4, 4, 0, 0]} maxBarSize={80}>
                {aucData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Statistical Robustness */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-md font-bold text-slate-800 mb-4 flex items-center gap-2">
            <ShieldCheck className="text-emerald-500 w-5 h-5" /> Robustness Analyses
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Subject-Level Bootstrap (5000 iter)</span>
              <span className="text-lg font-mono font-bold text-slate-700">95% CI: [1.000, 1.000]</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Task-Level Permutation (1000 iter)</span>
              <span className="text-lg font-mono font-bold text-slate-700">Exceedances: 0 / 1000</span>
            </div>
          </div>
        </div>

        {/* Other Diagnostics */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-md font-bold text-slate-800 mb-4 flex items-center gap-2">
            <CheckCircle2 className="text-blue-500 w-5 h-5" /> Explanatory Diagnostics
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">ACC Domain Shift (Cohen's d)</span>
              <span className="text-lg font-mono font-bold text-slate-700">≈ -1.47</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">SHAP Attribution Agreement</span>
              <span className="text-lg font-mono font-bold text-slate-700">ρ = 0.9527, Jaccard = 1.000</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
