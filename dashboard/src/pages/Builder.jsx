import React from 'react';
import { LayoutTemplate, CheckCircle2, AlertTriangle } from 'lucide-react';

const Builder = () => {
  const structure = [
    { section: "Title, Abstract, Keywords", file: "reports/FINAL_MANUSCRIPT_STAGE_6.md", status: "found" },
    { section: "1. Introduction & 2. Related Work", file: "reports/FINAL_MANUSCRIPT_STAGE_2.md", status: "found" },
    { section: "3. Research Gap & 4. Contributions", file: "reports/FINAL_MANUSCRIPT_STAGE_2.md", status: "found" },
    { section: "5. Materials and Methods", file: "reports/FINAL_MANUSCRIPT_STAGE_3.md", status: "found" },
    { section: "6. Experimental Design & 7. Results", file: "reports/FINAL_MANUSCRIPT_STAGE_4.md", status: "found" },
    { section: "8. Discussion", file: "reports/FINAL_MANUSCRIPT_DISCUSSION.md", status: "found" },
    { section: "9. Conclusion", file: "reports/FINAL_MANUSCRIPT_STAGE_6.md", status: "found" },
    { section: "References", file: "reports/FINAL_MANUSCRIPT_MASTER.md", status: "found" }
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-2 text-slate-800 flex items-center gap-2">
        <LayoutTemplate className="text-indigo-500" /> Master Manuscript Builder
      </h2>
      <p className="text-slate-600 mb-8">This interface maps the logical structure of the manuscript to the authoritative source files.</p>
      
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-8">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 text-sm">
              <th className="p-4 font-medium">Manuscript Section</th>
              <th className="p-4 font-medium">Authoritative Source File</th>
              <th className="p-4 font-medium text-center">Status</th>
            </tr>
          </thead>
          <tbody>
            {structure.map((item, idx) => (
              <tr key={idx} className="border-b border-slate-100 last:border-0 hover:bg-slate-50">
                <td className="p-4 font-bold text-slate-700">{item.section}</td>
                <td className="p-4 font-mono text-sm text-slate-500">{item.file}</td>
                <td className="p-4 text-center">
                  {item.status === 'found' ? (
                    <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-800 gap-1">
                      <CheckCircle2 className="w-3 h-3" /> Found
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-bold bg-amber-100 text-amber-800 gap-1">
                      <AlertTriangle className="w-3 h-3" /> Missing
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-6 text-indigo-900">
        <h3 className="font-bold text-lg mb-2">Final Master File</h3>
        <p className="text-sm mb-4">The final compiled manuscript with resolved citations has already been assembled.</p>
        <div className="font-mono bg-white border border-indigo-200 px-4 py-3 rounded-lg text-sm text-indigo-700">
          reports/FINAL_MANUSCRIPT_MASTER.md
        </div>
      </div>
    </div>
  );
};

export default Builder;
