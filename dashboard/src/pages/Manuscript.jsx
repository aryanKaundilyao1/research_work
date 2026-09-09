import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const Manuscript = () => {
  const [content, setContent] = useState('Loading manuscript...');

  useEffect(() => {
    // We fetch the compiled master manuscript
    fetch('/api/file?path=reports/FINAL_MANUSCRIPT_MASTER.md')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load master manuscript.');
        return res.text();
      })
      .then(text => setContent(text))
      .catch(err => setContent(`Error: ${err.message}. \n\nEnsure that 'reports/FINAL_MANUSCRIPT_MASTER.md' exists.`));
  }, []);

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-sm border border-slate-200 p-10 min-h-full">
      <article className="prose prose-slate max-w-none prose-headings:text-slate-800 prose-a:text-blue-600">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      </article>
    </div>
  );
};

export default Manuscript;
