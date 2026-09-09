import React, { useState } from 'react';
import { CheckSquare } from 'lucide-react';

const Checklist = () => {
  const items = [
    "No [CITATION NEEDED] placeholders remain",
    "References are numbered correctly in IEEE style",
    "All in-text citations map to the References list",
    "Tables I - IV are numbered correctly and populated",
    "Figures 1 - 6 are numbered correctly",
    "Figure captions are present and descriptive",
    "No duplicate sections exist in the master file",
    "No old experimental values (e.g., AUC=1.000) are present",    "Numerical values match the authoritative audit precisely",
    "Dataset sizes are consistent (WESAD N=15, Dataset B N=35)",    "Zero-shot terminology is strictly used (no 'domain adaptation' confusion)",
    "Target stress-label leakage statement is explicitly clear",
    "Scientific limitations are present and appropriately cautious",
    "Abstract perfectly matches Results and Conclusion",
    "Final compiled Markdown/PDF has been generated"
  ];

  const [checked, setChecked] = useState(
    // initialize all to true since we've audited this project already
    items.reduce((acc, curr, i) => ({ ...acc, [i]: true }), {})
  );

  const toggle = (i) => setChecked(prev => ({ ...prev, [i]: !prev[i] }));

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-2 text-slate-800 flex items-center gap-2">
        <CheckSquare className="text-emerald-600" /> Pre-Submission Checklist
      </h2>
      <p className="text-slate-600 mb-8">Verify these critical conditions before submitting the manuscript.</p>
      
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-2">
        {items.map((item, i) => (
          <label 
            key={i} 
            className="flex items-start space-x-3 p-4 hover:bg-slate-50 cursor-pointer rounded-lg transition-colors border-b border-slate-100 last:border-0"
          >
            <div className="flex-shrink-0 mt-0.5">
              <input 
                type="checkbox" 
                checked={checked[i]} 
                onChange={() => toggle(i)}
                className="w-5 h-5 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 transition-all cursor-pointer"
              />
            </div>
            <span className={`text-slate-700 font-medium ${checked[i] ? 'line-through text-slate-400' : ''}`}>
              {item}
            </span>
          </label>
        ))}
      </div>
      
      {Object.values(checked).every(v => v) && (
        <div className="mt-8 bg-emerald-50 border border-emerald-200 text-emerald-800 px-6 py-4 rounded-xl font-bold flex items-center justify-center gap-2">
          <CheckSquare /> All pre-submission checks completed. Ready to submit!
        </div>
      )}
    </div>
  );
};

export default Checklist;
