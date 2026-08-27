import React, { useState } from 'react';
import { Search as SearchIcon, FileText, Code2, Loader2 } from 'lucide-react';

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsSearching(true);
    setSearched(true);
    try {
      const q = query.toLowerCase();
      const res = await fetch('/api/search_index.json');
      const allFiles = await res.json();
      
      const matched = [];
      allFiles.forEach(file => {
        if (file.content.toLowerCase().includes(q)) {
          const lines = file.content.split('\n');
          const matches = [];
          for (let i = 0; i < lines.length; i++) {
            if (lines[i].toLowerCase().includes(q)) {
              matches.push({
                lineNum: i + 1,
                content: lines[i].trim()
              });
              if (matches.length > 3) break;
            }
          }
          matched.push({
            path: file.path,
            matches
          });
        }
      });
      setResults(matched);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  const getFileIcon = (path) => {
    const ext = path.split('.').pop().toLowerCase();
    return ['md', 'txt', 'csv'].includes(ext) ? <FileText className="w-5 h-5 text-blue-500" /> : <Code2 className="w-5 h-5 text-amber-500" />;
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-slate-800 flex items-center gap-2">
        <SearchIcon className="text-blue-600" /> Global Project Search
      </h2>

      <form onSubmit={handleSearch} className="mb-8">
        <div className="relative flex items-center">
          <input
            type="text"
            className="w-full pl-12 pr-4 py-4 rounded-xl border border-slate-300 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg bg-white"
            placeholder="Search manuscripts, code, and audits..."
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
          <SearchIcon className="absolute left-4 text-slate-400 w-6 h-6" />
          <button 
            type="submit" 
            disabled={isSearching}
            className="absolute right-3 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            {isSearching ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Search'}
          </button>
        </div>
      </form>

      <div className="space-y-4">
        {!isSearching && searched && results.length === 0 && (
          <div className="text-center py-12 bg-white rounded-xl border border-slate-200">
            <p className="text-slate-500">No results found for "{query}"</p>
          </div>
        )}

        {results.map((res, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="bg-slate-50 px-4 py-3 border-b border-slate-200 flex items-center gap-2">
              {getFileIcon(res.path)}
              <span className="font-mono text-sm text-slate-700 font-medium">{res.path}</span>
            </div>
            <div className="p-4 bg-slate-900 text-slate-300 font-mono text-sm overflow-x-auto">
              {res.matches.map((m, i) => (
                <div key={i} className="flex gap-4 mb-2 last:mb-0 hover:bg-slate-800 px-2 py-1 rounded">
                  <span className="text-slate-500 select-none w-8 text-right flex-shrink-0">{m.lineNum}</span>
                  <span className="whitespace-pre">{m.content}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Search;
