import React, { useEffect, useState } from 'react';
import { FileText, Search } from 'lucide-react';

const Literature = () => {
  const [pdfs, setPdfs] = useState([]);
  const [activePdf, setActivePdf] = useState(null);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch('/api/inventory.json')
      .then(res => res.json())
      .then(data => setPdfs(data.pdf || []));
  }, []);

  const filteredPdfs = pdfs.filter(p => p.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="flex h-full bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Sidebar List */}
      <div className="w-80 border-r border-slate-200 flex flex-col bg-slate-50">
        <div className="p-4 border-b border-slate-200">
          <h2 className="text-lg font-bold text-slate-800 mb-3">Literature Library</h2>
          <div className="relative">
            <Search className="absolute left-3 top-2.5 text-slate-400 w-4 h-4" />
            <input 
              type="text" 
              placeholder="Filter PDFs..." 
              className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {filteredPdfs.map(pdfPath => (
            <button
              key={pdfPath}
              onClick={() => setActivePdf(pdfPath)}
              className={`w-full text-left px-3 py-3 rounded-md flex items-start space-x-3 transition-colors ${
                activePdf === pdfPath ? 'bg-blue-100 text-blue-900' : 'hover:bg-slate-200 text-slate-700'
              }`}
            >
              <FileText className="w-5 h-5 flex-shrink-0 mt-0.5 text-red-500" />
              <span className="text-sm font-medium break-all">{pdfPath.split('/').pop()}</span>
            </button>
          ))}
          {filteredPdfs.length === 0 && (
            <p className="text-sm text-slate-500 text-center py-8">No PDFs found.</p>
          )}
        </div>
      </div>

      {/* PDF Viewer */}
      <div className="flex-1 bg-slate-200 flex flex-col relative">
        {activePdf ? (
          <iframe 
            src={`/raw/${activePdf}`}
            className="w-full h-full border-none"
            title="PDF Viewer"
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
            <BookOpen className="w-16 h-16 mb-4 opacity-50" />
            <p>Select a PDF from the list to view it</p>
          </div>
        )}
      </div>
    </div>
  );
};

import { BookOpen } from 'lucide-react';
export default Literature;
