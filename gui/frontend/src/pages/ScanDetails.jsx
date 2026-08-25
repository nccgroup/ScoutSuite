import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  CheckCircle2, XCircle, Clock, StopCircle, 
  ExternalLink, ArrowLeft, RefreshCw, FileText, ShieldAlert
} from 'lucide-react';
import { scansApi, createScanWebSocket } from '../api';
import LogTerminal from '../components/LogTerminal';

export default function ScanDetails() {
  const { scanId } = useParams();
  const [scan, setScan] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState(false);

  const fetchScan = async () => {
    try {
      const data = await scansApi.get(scanId);
      setScan(data);
      const logHistory = await scansApi.getLogs(scanId);
      setLogs(logHistory);
    } catch (err) {
      console.error("Failed to load scan details:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScan();

    // Establish WebSocket for real-time output
    const ws = createScanWebSocket(
      scanId,
      (data) => {
        if (data.type === 'log') {
          setLogs((prev) => [...prev, data]);
        } else if (data.type === 'status') {
          setScan((prev) => ({
            ...prev,
            status: data.status,
            report_path: data.report_path || prev?.report_path,
            end_time: data.end_time || prev?.end_time,
            summary: data.summary || prev?.summary,
            is_running: false,
          }));
        }
      },
      (err) => console.log('WebSocket stream closed/error:', err)
    );

    return () => {
      ws.close();
    };
  }, [scanId]);

  const handleCancel = async () => {
    if (!confirm("Are you sure you want to stop this scan?")) return;
    try {
      setCancelling(true);
      await scansApi.cancel(scanId);
      fetchScan();
    } catch (err) {
      alert("Failed to cancel scan");
    } finally {
      setCancelling(false);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-4 h-4" /> Audit Completed
          </span>
        );
      case 'running':
      case 'queued':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">
            <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span> Live In Progress
          </span>
        );
      case 'cancelled':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-500/10 text-slate-400 border border-slate-500/30">
            <Clock className="w-4 h-4" /> Cancelled
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/30">
            <XCircle className="w-4 h-4" /> Failed / Error
          </span>
        );
    }
  };

  const deviceLoginLog = logs
    .map(l => (typeof l === 'string' ? l : l.message || ''))
    .find(m => m.includes('devicelogin') || m.includes('[ACTION REQUIRED]'));

  let deviceCode = null;
  if (deviceLoginLog) {
    const codeMatch = deviceLoginLog.match(/code:\s*([A-Z0-9]+)/i) || deviceLoginLog.match(/([A-Z0-9]{8,12})/);
    if (codeMatch) {
      deviceCode = codeMatch[1];
    }
  }

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6 flex flex-col h-[calc(100vh-4rem)]">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 shrink-0 bg-dark-card border border-dark-border p-5 rounded-2xl">
        <div className="flex items-center gap-4">
          <Link
            to="/"
            className="p-2 rounded-xl bg-dark-bg border border-dark-border text-slate-400 hover:text-white transition"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-bold text-white tracking-tight">Audit Session</h2>
              <span className="font-mono text-xs bg-dark-bg border border-dark-border px-2.5 py-1 rounded text-slate-300">
                {scanId?.substring(0, 8)}
              </span>
              {scan && getStatusBadge(scan.status)}
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Provider: <span className="font-semibold text-white uppercase">{scan?.provider}</span> • Started:{' '}
              {scan?.start_time ? new Date(scan.start_time).toLocaleTimeString() : '-'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {scan?.is_running && (
            <button
              onClick={handleCancel}
              disabled={cancelling}
              className="flex items-center gap-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-semibold px-4 py-2 rounded-xl transition cursor-pointer"
            >
              <StopCircle className="w-4 h-4" />
              <span>{cancelling ? 'Stopping...' : 'Cancel Scan'}</span>
            </button>
          )}

          {scan?.report_path && (
            <a
              href={scan.report_path}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 bg-brand-500 hover:bg-brand-600 text-slate-950 font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-brand-500/20 transition cursor-pointer"
            >
              <FileText className="w-4 h-4" />
              <span>Open HTML Report</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
      </div>

      {/* Interactive Azure Device Code Login Banner */}
      {deviceLoginLog && scan?.is_running && (
        <div className="bg-gradient-to-r from-blue-900/40 to-indigo-900/40 border border-blue-500/40 p-4 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs shrink-0 shadow-xl">
          <div className="flex items-center gap-3.5">
            <div className="bg-blue-500/20 p-2.5 rounded-xl text-blue-400 border border-blue-500/30">
              <KeyRound className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="font-bold text-white text-sm">Azure Device Login Required</div>
              <div className="text-slate-300 mt-0.5">
                Visit <a href="https://microsoft.com/devicelogin" target="_blank" rel="noreferrer" className="text-blue-400 font-semibold underline">microsoft.com/devicelogin</a> and enter code:
                {deviceCode && (
                  <span className="font-mono font-bold text-amber-300 bg-black/60 border border-amber-500/30 px-2 py-0.5 rounded ml-2 text-sm tracking-wider">
                    {deviceCode}
                  </span>
                )}
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2.5">
            {deviceCode && (
              <button
                type="button"
                onClick={() => navigator.clipboard.writeText(deviceCode)}
                className="bg-dark-bg hover:bg-dark-border text-white border border-dark-border px-3.5 py-2 rounded-xl font-semibold transition cursor-pointer"
              >
                Copy Code
              </button>
            )}
            <a
              href="https://microsoft.com/devicelogin"
              target="_blank"
              rel="noreferrer"
              className="bg-blue-500 hover:bg-blue-600 text-slate-950 font-bold px-4 py-2 rounded-xl flex items-center gap-1.5 transition shadow-lg shadow-blue-500/20 cursor-pointer"
            >
              <span>Open microsoft.com/devicelogin</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      )}

      {/* Findings banner if available */}
      {scan?.summary?.findings_count !== undefined && (
        <div className="bg-amber-500/10 border border-amber-500/20 p-4 rounded-xl flex items-center justify-between text-xs text-amber-300 shrink-0">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0" />
            <span>
              <strong>{scan.summary.findings_count} Security Rules Triggered</strong> across audited services.
            </span>
          </div>
          {scan.report_path && (
            <a href={scan.report_path} target="_blank" rel="noreferrer" className="underline font-semibold hover:text-white">
              Inspect Findings in Report →
            </a>
          )}
        </div>
      )}

      {/* Terminal View */}
      <div className="flex-1 min-h-0">
        <LogTerminal logs={logs} isRunning={scan?.is_running} />
      </div>
    </div>
  );
}
