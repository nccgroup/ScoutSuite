import React from 'react';
import { Shield, LogOut, User, Terminal } from 'lucide-react';
import { authApi } from '../api';

export default function Navbar() {
  const username = localStorage.getItem('scout_user') || 'Admin';

  const handleLogout = () => {
    authApi.logout();
  };

  return (
    <header className="h-16 border-b border-dark-border bg-dark-card/80 backdrop-blur sticky top-0 z-40 px-6 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="bg-brand-500/20 p-2 rounded-lg text-brand-500 border border-brand-500/30 flex items-center justify-center">
          <Shield className="w-6 h-6" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-lg text-white tracking-wide">ScoutSuite</h1>
            <span className="text-xs bg-brand-500/20 text-brand-500 font-medium px-2 py-0.5 rounded border border-brand-500/30">
              GUI Console
            </span>
          </div>
          <p className="text-xs text-dark-muted">Multi-Cloud Security Auditing Engine</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 bg-dark-bg/60 border border-dark-border px-3 py-1.5 rounded-lg text-sm">
          <User className="w-4 h-4 text-brand-500" />
          <span className="text-slate-200 font-medium">{username}</span>
        </div>

        <button
          onClick={handleLogout}
          className="flex items-center gap-2 px-3 py-1.5 text-sm text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg border border-transparent hover:border-red-500/20 transition"
          title="Sign Out"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </header>
  );
}
