import React, { useEffect, useState } from 'react';
import { Code2, FileCode2 } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const CodeViewer = () => {
  const [codeFiles, setCodeFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);
  const [content, setContent] = useState('');

  useEffect(() => {
    fetch('/api/inventory')
      .then(res => res.json())
      .then(data => setCodeFiles(data.code || []));
  }, []);

  const loadCode = (path) => {
    setActiveFile(path);
    setContent('Loading...');
    fetch(`/api/file?path=${encodeURIComponent(path)}`)
      .then(res => res.text())
      .then(text => setContent(text))
      .catch(err => setContent(`Error loading code: ${err.message}`));
  };

  const getLanguage = (path) => {
    if (!path) return 'text';
    const ext = path.split('.').pop().toLowerCase();
    const map = { 'py': 'python', 'js': 'javascript', 'ts': 'typescript', 'json': 'json', 'r': 'r' };
    return map[ext] || 'text';
  };

  return (
    <div className="flex h-full bg-slate-900 rounded-xl shadow-xl overflow-hidden border border-slate-700">
      <div className="w-72 border-r border-slate-700 flex flex-col bg-slate-900">
        <div className="p-4 border-b border-slate-800">
          <h2 className="text-lg font-bold text-slate-200 flex items-center gap-2">
            <Code2 className="text-amber-400" /> Source Code
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {codeFiles.map(path => (
            <button
              key={path}
              onClick={() => loadCode(path)}
              className={`w-full text-left px-3 py-2 rounded-md flex items-center space-x-2 transition-colors ${
                activeFile === path ? 'bg-slate-800 text-amber-400' : 'hover:bg-slate-800/50 text-slate-400'
              }`}
            >
              <FileCode2 className="w-4 h-4 flex-shrink-0" />
              <span className="text-sm font-mono truncate">{path.split('/').pop()}</span>
            </button>
          ))}
        </div>
      </div>
      <div className="flex-1 flex flex-col overflow-hidden bg-[#1e1e1e]">
        {activeFile ? (
          <>
            <div className="bg-slate-800 px-4 py-2 border-b border-slate-700 flex justify-between items-center">
              <span className="text-slate-300 font-mono text-sm">{activeFile}</span>
              <button 
                onClick={() => navigator.clipboard.writeText(content)}
                className="text-xs bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded transition-colors"
              >
                Copy Code
              </button>
            </div>
            <div className="flex-1 overflow-auto">
              <SyntaxHighlighter 
                language={getLanguage(activeFile)} 
                style={vscDarkPlus}
                customStyle={{ margin: 0, padding: '1rem', background: 'transparent', fontSize: '14px' }}
                showLineNumbers={true}
              >
                {content}
              </SyntaxHighlighter>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-600">
            <Code2 className="w-16 h-16 mb-4 opacity-20" />
            <p className="font-mono text-sm">Select a file to view code</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CodeViewer;
