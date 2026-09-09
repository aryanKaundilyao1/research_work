import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { BarChart2, ShieldCheck, CheckCircle2, ArchiveX } from 'lucide-react';

const Results = () => {
  const aucData = [
    { name: 'External (Absolute) FINAL CANONICAL', auc: 0.492, color: '#ef4444' }, 
    { name: 'External (Baseline-relative) FINAL CANONICAL', auc: 0.781, color: '#10b981' }, 
  ];

  const archivedData = [
    { name: 'External (Absolute V1)', auc: 0.423, color: '#ef4444' }, 
    { name: 'External (ACC Ablation)', auc: 0.540, color: '#f59e0b' }, 
    { name: 'External (Leaked Relative)', auc: 1.000, color: '#10b981' }, 
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
        <BarChart2 className="text-blue-500" /> Results Dashboard
      </h2>

      {/* Main Bar Chart */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h3 className="text-lg font-bold text-slate-800 mb-2">Cross-Dataset Transfer Performance (ROC-AUC)</h3>
        <p className="text-sm text-slate-500 mb-6">Current rigorous target-label-free cross-dataset transfer, strictly separated from 30s calibration.</p>
        <div className="h-80 w-full max-w-2xl mx-auto">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={aucData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} />
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
            <ShieldCheck className="text-emerald-500 w-5 h-5" /> Subject-Level Evaluation Metrics
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Baseline-Relative AUROC</span>
              <span className="text-lg font-mono font-bold text-slate-700">0.781</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Median/IQR AUROC</span>
              <span className="text-lg font-mono font-bold text-slate-700">0.840 (IQR 0.32)</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="block text-xs font-bold text-slate-400 uppercase">Participant-Balanced Acc</span>
              <span className="text-lg font-mono font-bold text-slate-700">0.669</span>
            </div>
          </div>
        </div>

        {/* Other Diagnostics */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-md font-bold text-slate-800 mb-4 flex items-center gap-2">
            <CheckCircle2 className="text-blue-500 w-5 h-5" /> Target N = 35 Independent Cohort
          </h3>
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100 text-sm text-slate-700">
              The 0.781 AUROC is established with exact participant mapping, excluding f07, resolving S02 duplication, and applying a strict 30s calibration + 30s buffer boundary to completely eliminate temporal leakage. Result represents the eligible 21 subjects.
            </div>
          </div>
        </div>
      </div>

      {/* Archived Results */}
      <div className="bg-red-50 rounded-xl shadow-sm border border-red-200 p-8 mt-12 opacity-80">
        <h3 className="text-lg font-bold text-red-800 mb-2 flex items-center gap-2">
          <ArchiveX className="w-5 h-5" /> Archived Results / Previous Evaluation
        </h3>
        <p className="text-sm text-red-700 mb-6">
          <strong>WARNING:</strong> The results below are obsolete. The 1.000 result was invalidated because evaluation overlapping windows extended back into the calibration period, causing temporal label leakage. The absolute results (0.423 and 0.540) were also evaluated under mismatched logic.
        </p>
        <div className="h-48 w-full max-w-2xl mx-auto">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={archivedData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#fca5a5" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#991b1b', fontSize: 11}} />
              <YAxis domain={[0, 1.0]} axisLine={false} tickLine={false} tick={{fill: '#991b1b'}} />
              <Tooltip cursor={{fill: '#fee2e2'}} />
              <Bar dataKey="auc" radius={[4, 4, 0, 0]} maxBarSize={60}>
                {archivedData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} opacity={0.6} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
};

export default Results;
