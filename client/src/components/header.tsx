import { Library, Search, Sparkles } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const navLinkClasses = ({ isActive }: { isActive: boolean }) =>
  `flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition-colors ${
    isActive ? 'bg-blue-100 text-blue-700' : 'text-slate-600 hover:text-slate-900'
  }`;

export const Header = () => {
  return (
    <header className="border-b border-slate-200 bg-slate-50">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <div>
            <p className="text-base font-semibold text-slate-900">Reference Search</p>
            <p className="text-sm text-slate-500">Sales Engineering</p>
          </div>
        </div>
        <nav className="flex items-center gap-2">
          <NavLink to="/" end className={navLinkClasses}>
            <Search className="h-4 w-4" />
            Search
          </NavLink>
          <NavLink to="/add-case-study" className={navLinkClasses}>
            <Library className="h-4 w-4" />
            Add case study
          </NavLink>
        </nav>
      </div>
    </header>
  );
};
