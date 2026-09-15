import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { manuscriptContent } from '../generated/staticData';

const Manuscript = () => {
  return (
    <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-sm border border-slate-200 p-10 min-h-full">
      <article className="prose prose-slate max-w-none prose-headings:text-slate-800 prose-a:text-blue-600">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {manuscriptContent}
        </ReactMarkdown>
      </article>
    </div>
  );
};

export default Manuscript;
