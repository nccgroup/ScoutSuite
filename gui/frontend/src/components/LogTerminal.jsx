import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Copy, Check, ArrowDown, Search, Trash2 } from 'lucide-react';

export default function LogTerminal({ logs = [], isRunning = false, title = "Audit Live Terminal Output" }) {
  const [autoScroll, setAutoScroll] = useState(true);
  const [filterText, setFilterText] = useState('');
  const [copied, setCopied] = useState(false);
  const terminalEndRef = useRef(null);

  useEffect(() => {
    if (autoScroll && terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, autoScroll]);

  const filteredLogs = logs.filter(log => {
    if (!filterText) return true;
    const msg = typeof log === 'string' ? log : log.message || '';
    return msg.toLowerCase().includes(filterText.toLowerCase());
  });

  const handleCopy = () => {
    const rawText = logs.map(l => (typeof l === 'string' ? l : `[${l.timestamp || ''}] [${l.level || 'INFO'}] ${l.message}`)).join('\n');
    navigator.clipboard.writeText(rawText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getLogStyle = (level = 'INFO') => {
    switch (level.toUpperCase()) {
      case 'ERROR':
        return 'text-red-400 font-semibold';
      case 'WARNING':
      case 'WARN':
        return 'text-amber-400';
      case 'DEBUG':
        return 'text-purple-400';
      default:
        return 'text-emerald-400';
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0a0f1d] border border-dark-border rounded-xl overflow-hidden shadow-2xl font-mono">
      {/* Terminal Header */}
      <div className="bg-[#131b2e] border-b border-dark-border px-4 py-2.5 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-300 font-medium ml-2">
            <Terminal className="w-3.5 h-3.5 text-brand-500" />
            <span>{title}</span>
            {isRunning && (
              <span className="flex items-center gap-1 text-[11px] text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/30">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping"></span>
                Auditing...
              </span>
            )}
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Filter logs..."
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
              className="bg-dark-bg/80 border border-dark-border text-xs rounded-md pl-8 pr-2.5 py-1 text-slate-200 focus:outline-none focus:border-brand-500 w-36 sm:w-48 placeholder-slate-500"
            />
          </div>

          <button
            onClick={() => setAutoScroll(!autoScroll)}
            className={`p-1.5 rounded-md text-xs border transition ${
              autoScroll
                ? 'bg-brand-500/20 text-brand-500 border-brand-500/40'
                : 'text-slate-400 border-dark-border hover:bg-dark-card'
            }`}
            title={autoScroll ? "Auto-scroll Enabled" : "Auto-scroll Paused"}
          >
            <ArrowDown className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={handleCopy}
            className="p-1.5 rounded-md text-xs text-slate-400 border border-dark-border hover:bg-dark-card hover:text-slate-200 transition"
            title="Copy Logs"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Terminal Body */}
      <div className="flex-1 p-4 overflow-y-auto text-xs leading-relaxed space-y-1 text-slate-300 min-h-[300px]">
        {filteredLogs.length === 0 ? (
          <div className="text-slate-600 italic select-none">
            {isRunning ? "Awaiting ScoutSuite stdout stream..." : "No logs available for this session."}
          </div>
        ) : (
          filteredLogs.map((log, index) => {
            const isObj = typeof log === 'object';
            const timestamp = isObj && log.timestamp ? log.timestamp.split('T')[1]?.substring(0, 8) : null;
            const level = isObj ? log.level || 'INFO' : 'INFO';
            const msg = isObj ? log.message : log;

            return (
              <div key={index} className="flex items-start gap-2 hover:bg-white/[0.02] py-0.5 px-1 rounded">
                {timestamp && <span className="text-slate-600 select-none shrink-0">[{timestamp}]</span>}
                <span className={`shrink-0 select-none font-bold ${getLogStyle(level)}`}>
                  [{level}]
                </span>
                <span className="break-all whitespace-pre-wrap flex-1 text-slate-200">{msg}</span>
              </div>
            );
          })
        )}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
}
