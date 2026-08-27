import React from 'react';
import { Bookmark, FileText } from 'lucide-react';

const Citations = () => {
  const citations = [
    { id: 1, title: 'WESAD paper', source: 'Original Dataset', verified: true },
    { id: 2, title: 'Dataset B paper', source: 'Original Dataset', verified: true },
    { id: 3, title: 'Domain shift / domain adaptation paper', source: 'Methodology', verified: true },
    { id: 4, title: 'Baseline normalization paper', source: 'Methodology', verified: true },
    { id: 5, title: 'Protocol/motion paper', source: 'Domain Knowledge', verified: true },
    { id: 6, title: 'SHAP (Lundberg & Lee, 2017)', source: 'Original Algorithm', verified: true },
    { id: 7, title: 'XGBoost (Chen & Guestrin, 2016)', source: 'Original Algorithm', verified: true },
    { id: 8, title: 'SMOTE (Chawla et al., 2002)', source: 'Original Algorithm', verified: true },
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-slate-800 flex items-center gap-2">
        <Bookmark className="text-blue-500" /> Citation Management
      </h2>
      
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 text-sm">
              <th className="p-4 font-medium w-16 text-center">Ref</th>
              <th className="p-4 font-medium">Mapped Source / Topic</th>
              <th className="p-4 font-medium">Category</th>
              <th className="p-4 font-medium text-center">Status</th>
            </tr>
          </thead>
          <tbody>
            {citations.map(cit => (
              <tr key={cit.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center font-bold text-slate-400">[{cit.id}]</td>
                <td className="p-4 flex items-center gap-2 font-medium text-slate-800">
                  <FileText className="w-4 h-4 text-slate-400" /> {cit.title}
                </td>
                <td className="p-4 text-sm text-slate-500">{cit.source}</td>
                <td className="p-4 text-center">
                  {cit.verified ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                      Verified
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                      Needs verification
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Citations;
