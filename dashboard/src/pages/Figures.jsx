import React, { useEffect, useState } from 'react';
import { Image as ImageIcon } from 'lucide-react';

const Figures = () => {
  const [figures, setFigures] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    fetch('/api/inventory.json')
      .then(res => res.json())
      .then(data => setFigures(data.figures || []));
  }, []);

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-slate-800 flex items-center gap-2">
        <ImageIcon className="text-pink-500" /> Figure Library
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {figures.map(figPath => (
          <div 
            key={figPath} 
            className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden cursor-pointer hover:ring-2 ring-pink-400 transition-all"
            onClick={() => setSelectedImage(figPath)}
          >
            <div className="h-48 bg-slate-100 flex items-center justify-center p-2">
              <img src={`/raw/${figPath}`} alt="Figure thumbnail" className="max-h-full max-w-full object-contain" />
            </div>
            <div className="p-3 border-t border-slate-100">
              <p className="text-sm font-medium text-slate-700 truncate" title={figPath.split('/').pop()}>
                {figPath.split('/').pop()}
              </p>
              <p className="text-xs text-slate-400 truncate" title={figPath}>{figPath}</p>
            </div>
          </div>
        ))}
        {figures.length === 0 && (
          <div className="col-span-full py-12 text-center text-slate-500">
            No figures found in the project directory.
          </div>
        )}
      </div>

      {selectedImage && (
        <div className="fixed inset-0 bg-slate-900/80 z-50 flex items-center justify-center p-8" onClick={() => setSelectedImage(null)}>
          <div className="bg-white rounded-xl shadow-xl overflow-hidden max-w-5xl max-h-full flex flex-col" onClick={e => e.stopPropagation()}>
            <div className="p-4 border-b flex justify-between items-center bg-slate-50">
              <h3 className="font-bold text-slate-800">{selectedImage.split('/').pop()}</h3>
              <button onClick={() => setSelectedImage(null)} className="text-slate-500 hover:text-slate-800 font-bold px-2 py-1 bg-slate-200 rounded">Close</button>
            </div>
            <div className="flex-1 overflow-auto p-4 flex justify-center bg-slate-100">
              <img src={`/raw/${selectedImage}`} alt="Full Figure" className="max-w-full object-contain" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Figures;
