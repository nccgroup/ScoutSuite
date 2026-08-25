import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, PlayCircle, KeyRound, FileText, History, Settings } from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'New Scan', href: '/new-scan', icon: PlayCircle },
  { name: 'Credentials', href: '/credentials', icon: KeyRound },
  { name: 'Reports & History', href: '/reports', icon: FileText },
];

export default function Sidebar() {
  return (
    <aside className="w-64 border-r border-dark-border bg-dark-bg/95 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="p-4 space-y-1">
        <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
          Navigation
        </div>
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                isActive
                  ? 'bg-brand-500/15 text-brand-500 border border-brand-500/30'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-dark-card/60'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </div>

      <div className="p-4 border-t border-dark-border text-xs text-slate-500 space-y-2">
        <div className="flex justify-between items-center">
          <span>Engine Status</span>
          <span className="inline-flex items-center gap-1.5 text-emerald-400 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            WSL Ready
          </span>
        </div>
        <div className="text-[11px] text-slate-600">
          ScoutSuite Multi-Cloud Security Audit
        </div>
      </div>
    </aside>
  );
}
