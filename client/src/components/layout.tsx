import { Outlet } from 'react-router-dom';

import { Header } from './header';

export const Layout = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main>
        <Outlet />
      </main>
    </div>
  );
};
