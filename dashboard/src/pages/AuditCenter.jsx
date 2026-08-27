import React from 'react';
import { ShieldCheck, CheckCircle2 } from 'lucide-react';

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
    { k: "Dataset B N", v: "31" },
    { k: "Internal AUC", v: "0.964" },
    { k: "External Absolute AUC", v: "0.423" },
    { k: "ACC Ablation AUC", v: "0.540" },
    { k: "Baseline Relative AUC", v: "1.000" },
    { k: "Cohen's d", v: "≈ -1.47" },
    { k: "Bootstrap", v: "5000" },
    { k: "Bootstrap CI", v: "[1.000, 1.000]" },
    { k: "Permutation", v: "1000" },
    { k: "Permutation exceedances", v: "0" },
    { k: "SHAP ρ", v: "0.9527" },
    { k: "Top-20 Jaccard", v: "1.000" },
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
    </div>
  );
};

export default AuditCenter;
