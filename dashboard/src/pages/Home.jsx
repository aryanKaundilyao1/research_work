import React, { useEffect, useState } from 'react';
import { FileText, BookOpen, Image, Table2, Code2, ShieldCheck, FileQuestion } from 'lucide-react';

const Home = () => {
  const [inventory, setInventory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/inventory.json')
      .then(res => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then(data => {
        setInventory(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-slate-500">Loading project inventory...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  const stats = [
    { label: 'Manuscript Drafts', count: inventory.manuscript.length, icon: FileText, color: 'text-blue-500', bg: 'bg-blue-100' },
    { label: 'Literature & PDFs', count: inventory.pdf.length, icon: BookOpen, color: 'text-purple-500', bg: 'bg-purple-100' },
    { label: 'Figures & Images', count: inventory.figures.length, icon: Image, color: 'text-pink-500', bg: 'bg-pink-100' },
    { label: 'Tables & CSVs', count: inventory.tables.length, icon: Table2, color: 'text-emerald-500', bg: 'bg-emerald-100' },
    { label: 'Code & Scripts', count: inventory.code.length, icon: Code2, color: 'text-amber-500', bg: 'bg-amber-100' },
    { label: 'Audit Reports', count: inventory.audit.length, icon: ShieldCheck, color: 'text-red-500', bg: 'bg-red-100' },
    { label: 'Other Files', count: inventory.other.length, icon: FileQuestion, color: 'text-slate-500', bg: 'bg-slate-100' },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-slate-800">Research Project Dashboard</h2>
        <p className="text-slate-600 mt-2 text-lg">Wearable Physiological Stress Detection</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center space-x-4">
            <div className={`p-4 rounded-full ${stat.bg}`}>
              <stat.icon className={`w-8 h-8 ${stat.color}`} />
            </div>
            <div>
              <p className="text-3xl font-bold text-slate-800">{stat.count}</p>
              <p className="text-sm font-medium text-slate-500">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <h3 className="text-xl font-bold mb-4 text-slate-800">Project Status: <span className="text-emerald-600">READY FOR SUBMISSION</span></h3>
        
        <div className="space-y-4">
          <div className="flex items-center space-x-3 text-slate-400 line-through">
            <ShieldCheck className="w-5 h-5 text-emerald-500" /> <span>Stage 1: Pre-Audit</span>
          </div>
          <div className="flex items-center space-x-3 text-slate-400 line-through">
            <ShieldCheck className="w-5 h-5 text-emerald-500" /> <span>Stage 2: Introduction & Related Work</span>
          </div>
          <div className="flex items-center space-x-3 text-slate-400 line-through">
            <ShieldCheck className="w-5 h-5 text-emerald-500" /> <span>Stage 3: Methods</span>
          </div>
          <div className="flex items-center space-x-3 text-slate-400 line-through">
            <ShieldCheck className="w-5 h-5 text-emerald-500" /> <span>Stage 4: Results</span>
          </div>
          <div className="flex items-center space-x-3 text-slate-400 line-through">
            <ShieldCheck className="w-5 h-5 text-emerald-500" /> <span>Stage 5: Discussion</span>
          </div>
          <div className="flex items-center space-x-3 text-slate-400 line-through">
            <ShieldCheck className="w-5 h-5 text-emerald-500" /> <span>Stage 6: Abstract & Conclusion</span>
          </div>
          <div className="flex items-center space-x-3 font-medium text-slate-800">
            <ShieldCheck className="w-5 h-5 text-emerald-500" /> <span>Stage 7: Final Submission Readiness</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
