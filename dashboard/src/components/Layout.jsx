import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { 
  Home, FileText, BookOpen, Bookmark, 
  TestTube, BarChart2, Image, Table2, 
  Code2, ShieldCheck, Search, LayoutTemplate, 
  CheckSquare, GraduationCap
} from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/manuscript', label: 'Manuscript', icon: FileText },
    { path: '/literature', label: 'Literature (PDFs)', icon: BookOpen },
    { path: '/citations', label: 'Citations', icon: Bookmark },
    { path: '/experiments', label: 'Experiments', icon: TestTube },
    { path: '/results', label: 'Results', icon: BarChart2 },
    { path: '/figures', label: 'Figures', icon: Image },
    { path: '/tables', label: 'Tables', icon: Table2 },
    { path: '/code', label: 'Code & Files', icon: Code2 },
    { path: '/audit', label: 'Audit Center', icon: ShieldCheck },
    { path: '/search', label: 'Global Search', icon: Search },
    { path: '/builder', label: 'Manuscript Builder', icon: LayoutTemplate },
    { path: '/vit-draft', label: 'VIT Paper Draft', icon: GraduationCap },
    { path: '/checklist', label: 'Pre-Submission', icon: CheckSquare },
  ];

  return (
    <div className="w-64 bg-slate-900 text-white min-h-screen flex flex-col">
      <div className="p-4 border-b border-slate-700">
        <h1 className="text-xl font-bold leading-tight">RESEARCH PROJECT</h1>
        <p className="text-xs text-slate-400 mt-1">Wearable Stress Detection</p>
      </div>
      <nav className="flex-1 overflow-y-auto p-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `flex items-center space-x-3 px-3 py-2 rounded-md transition-colors ${
                isActive ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <item.icon size={18} />
            <span className="text-sm font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

const Layout = () => {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8 relative">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
