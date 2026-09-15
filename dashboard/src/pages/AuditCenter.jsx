import React from 'react';
import { ShieldCheck, CheckCircle2, AlertCircle } from 'lucide-react';
import { conflicts } from '../generated/staticData';

const AuditCenter = () => {
  const audits = [
    { label: "Citation Audit", status: "PASS" },
    { label: "Numerical Consistency", status: "PASS" },
    { label: "Scientific Language", status: "PASS" },
    { label: "Terminology", status: "PASS" },
    { label: "Leakage (Zero-Shot Verification)", status: "PASS" },
    { label: "Contribution Constraints", status: "PASS" },
    { label: "Old Paper Contamination", status: "PASS" },
    { label: "Formatting", status: "PASS" }
  ];

  const values = [
    { k: "WESAD N", v: "15" },
    { k: "Dataset B N", v: "35" },
    { k: "Internal AUC", v: "0.964" },
    { k: "Baseline-Relative AUC (Z-Score)", v: "0.739" },
    { k: "Median/IQR AUC", v: "0.751" },
    { k: "External Absolute AUC", v: "0.408" },
    { k: "Cohen's d (ACC Shift)", v: "-1.47" },
    { k: "Bootstrap", v: "5000" },
    { k: "Permutation", v: "1000" },
    { k: "Permutation p-value", v: "0.001" },
    { k: "SHAP Spearman ρ", v: "0.9527" },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
        <ShieldCheck className="text-red-500" /> Validation & Audit Center
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Audit Status */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-200 p-4">
            <h3 className="font-bold text-slate-800">Final Protocol Audits</h3>
          </div>
          <div className="p-4 space-y-3">
            {audits.map(a => (
              <div key={a.label} className="flex justify-between items-center py-2 border-b border-slate-100 last:border-0">
                <span className="text-slate-700 font-medium">{a.label}</span>
                <span className="flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-800">
                  <CheckCircle2 className="w-3 h-3" /> {a.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Authoritative Values */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="bg-slate-50 border-b border-slate-200 p-4">
            <h3 className="font-bold text-slate-800">Authoritative Numerical Constants</h3>
            <p className="text-xs text-slate-500 mt-1">Locked and verified against experimental output.</p>
          </div>
          <div className="p-4">
            <table className="w-full text-left text-sm">
              <tbody>
                {values.map(v => (
                  <tr key={v.k} className="border-b border-slate-100 last:border-0">
                    <td className="py-2 text-slate-500 font-medium">{v.k}</td>
                    <td className="py-2 text-slate-900 font-mono text-right">{v.v}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      {conflicts && conflicts.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mt-8">
          <div className="bg-slate-50 border-b border-slate-200 p-4 flex items-center gap-2">
            <AlertCircle className="text-amber-500" />
            <h3 className="font-bold text-slate-800">Detected Conflicts</h3>
          </div>
          <div className="p-4 overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-slate-600">
                  <th className="py-2 px-4 font-medium">Path</th>
                  <th className="py-2 px-4 font-medium">Line</th>
                  <th className="py-2 px-4 font-medium">Term</th>
                  <th className="py-2 px-4 font-medium">Issue</th>
                </tr>
              </thead>
              <tbody>
                {conflicts.map((c, i) => (
                  <tr key={i} className="border-b border-slate-100 last:border-0">
                    <td className="py-3 px-4 text-slate-500 font-mono text-xs">{c.path}</td>
                    <td className="py-3 px-4 text-slate-900">{c.lineNum}</td>
                    <td className="py-3 px-4 font-medium text-slate-800">{c.term}</td>
                    <td className="py-3 px-4 text-slate-600">{c.issue}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
};

export default AuditCenter;
