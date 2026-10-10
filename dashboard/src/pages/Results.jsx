import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { BarChart2, ShieldCheck, CheckCircle2, Activity, TrendingUp } from 'lucide-react';

const Results = () => {
  const aucData = [
    { name: 'Internal WESAD LOSO-CV', auc: 0.964, color: '#3b82f6' }, 
    { name: 'External Absolute Transfer (with ACC)', auc: 0.492, color: '#ef4444' }, 
    { name: 'External ACC Ablation', auc: 0.540, color: '#f59e0b' }, 
    { name: 'External Baseline-Relative', auc: 0.772, color: '#10b981' }, 
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
        <BarChart2 className="text-blue-500" /> Results Dashboard
      </h2>

      {/* Main Bar Chart */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h3 className="text-lg font-bold text-slate-800 mb-2">Cross-Dataset Transfer Performance (ROC-AUC)</h3>
        <p className="text-sm text-slate-500 mb-6">Current rigorous target-label-free cross-dataset transfer.</p>
        <div className="h-80 w-full max-w-4xl mx-auto">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={aucData} margin={{ top: 20, right: 30, left: 20, bottom: 50 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis 
                dataKey="name" 
                axisLine={false} 
                tickLine={false} 
                tick={{fill: '#64748b', fontSize: 11}}
                interval={0}
                angle={-15}
                textAnchor="end"
              />
              <YAxis domain={[0, 1.0]} axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
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
            <ShieldCheck className="text-emerald-500 w-5 h-5" /> Statistical Robustness
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Bootstrap 95% CI</span>
              <span className="text-lg font-mono font-bold text-slate-700">[0.643, 0.880]</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Permutation p-value</span>
              <span className="text-lg font-mono font-bold text-slate-700">0/1000 ≥ observed</span>
            </div>
          </div>
        </div>

        {/* Feature Importance & Attribution */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-md font-bold text-slate-800 mb-4 flex items-center gap-2">
            <Activity className="text-blue-500 w-5 h-5" /> Feature Importance & Attribution
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">SHAP Spearman ρ</span>
              <span className="text-lg font-mono font-bold text-slate-700">0.980</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Top-5 Jaccard</span>
              <span className="text-lg font-mono font-bold text-slate-700">0.759</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Summary Results Table matching Table 7.1 */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mt-6">
          <div className="bg-slate-50 border-b border-slate-200 p-4 flex items-center gap-2">
            <TrendingUp className="text-purple-500 w-5 h-5" />
            <h3 className="font-bold text-slate-800">Summary Results Table</h3>
          </div>
          <div className="p-4 overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-slate-600">
                  <th className="py-3 px-4 font-bold">Experiment Setting</th>
                  <th className="py-3 px-4 font-bold">ROC-AUC</th>
                </tr>
              </thead>
              <tbody>
                {aucData.map((data, i) => (
                  <tr key={i} className="border-b border-slate-100 last:border-0">
                    <td className="py-3 px-4 text-slate-700 font-medium">{data.name}</td>
                    <td className="py-3 px-4 text-slate-900 font-mono font-bold">{data.auc.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
      </div>
    </div>
  );
};

export default Results;
