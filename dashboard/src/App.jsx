import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Manuscript from './pages/Manuscript';
import Literature from './pages/Literature';
import Citations from './pages/Citations';
import Experiments from './pages/Experiments';
import Results from './pages/Results';
import Figures from './pages/Figures';
import Tables from './pages/Tables';
import CodeViewer from './pages/CodeViewer';
import AuditCenter from './pages/AuditCenter';
import Search from './pages/Search';
import Builder from './pages/Builder';
import Checklist from './pages/Checklist';
import VITPaperDraft from './pages/VITPaperDraft';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="manuscript" element={<Manuscript />} />
          <Route path="literature" element={<Literature />} />
          <Route path="citations" element={<Citations />} />
          <Route path="experiments" element={<Experiments />} />
          <Route path="results" element={<Results />} />
          <Route path="figures" element={<Figures />} />
          <Route path="tables" element={<Tables />} />
          <Route path="code" element={<CodeViewer />} />
          <Route path="audit" element={<AuditCenter />} />
          <Route path="search" element={<Search />} />
          <Route path="builder" element={<Builder />} />
          <Route path="checklist" element={<Checklist />} />
          <Route path="vit-draft" element={<VITPaperDraft />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
