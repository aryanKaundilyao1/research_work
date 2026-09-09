import React, { useEffect, useState } from 'react';
import { Table2, FileText } from 'lucide-react';

const Tables = () => {
  const [tables, setTables] = useState([]);
  const [activeTable, setActiveTable] = useState(null);
  const [content, setContent] = useState('Select a table to view contents.');

  useEffect(() => {
    fetch('/api/inventory')
      .then(res => res.json())
      .then(data => setTables(data.tables || []));
  }, []);

  const loadTable = (path) => {
    setActiveTable(path);
    setContent('Loading...');
    fetch(`/api/file?path=${encodeURIComponent(path)}`)
      .then(res => res.text())
      .then(text => setContent(text))
      .catch(err => setContent(`Error loading table: ${err.message}`));
  };

  return (
    <div className="flex h-full bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="w-80 border-r border-slate-200 flex flex-col bg-slate-50">
        <div className="p-4 border-b border-slate-200">
          <h2 className="text-lg font-bold text-slate-800 flex items-center gap-2">
            <Table2 className="text-emerald-500" /> Table Library
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {tables.map(tablePath => (
            <button
              key={tablePath}
              onClick={() => loadTable(tablePath)}
              className={`w-full text-left px-3 py-3 rounded-md flex items-start space-x-3 transition-colors ${
                activeTable === tablePath ? 'bg-emerald-100 text-emerald-900' : 'hover:bg-slate-200 text-slate-700'
              }`}
            >
              <FileText className="w-5 h-5 flex-shrink-0 mt-0.5 text-emerald-500" />
              <div className="overflow-hidden">
                <span className="text-sm font-medium block truncate">{tablePath.split('/').pop()}</span>
                <span className="text-xs text-slate-500 block truncate">{tablePath}</span>
              </div>
            </button>
          ))}
          {tables.length === 0 && (
            <p className="text-sm text-slate-500 text-center py-8">No tables/CSVs found.</p>
          )}
        </div>
      </div>
      <div className="flex-1 bg-slate-50 flex flex-col p-4 overflow-hidden">
        {activeTable ? (
          <div className="flex-1 bg-white border border-slate-200 rounded-lg overflow-auto p-4">
            <pre className="text-xs font-mono text-slate-800 whitespace-pre-wrap">{content}</pre>
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
            <Table2 className="w-16 h-16 mb-4 opacity-50" />
            <p>Select a table to view its raw data</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Tables;
