import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlayCircle, CheckCircle2, XCircle, Clock, ShieldAlert,
  Cloud, ArrowUpRight, RefreshCw, Trash2, ExternalLink
} from 'lucide-react';
import { dashboardApi, scansApi } from '../api';

const providerLogos = {
  aws: { name: 'Amazon Web Services', color: 'text-amber-400 bg-amber-400/10 border-amber-400/30' },
  azure: { name: 'Microsoft Azure', color: 'text-blue-400 bg-blue-400/10 border-blue-400/30' },
  gcp: { name: 'Google Cloud Platform', color: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/30' },
  kubernetes: { name: 'Kubernetes', color: 'text-indigo-400 bg-indigo-400/10 border-indigo-400/30' },
  aliyun: { name: 'Alibaba Cloud', color: 'text-orange-400 bg-orange-400/10 border-orange-400/30' },
  do: { name: 'DigitalOcean', color: 'text-sky-400 bg-sky-400/10 border-sky-400/30' },
  oci: { name: 'Oracle Cloud', color: 'text-red-400 bg-red-400/10 border-red-400/30' },
};

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsData, scansData] = await Promise.all([
        dashboardApi.getStats(),
        scansApi.list()
      ]);
      setStats(statsData);
      setScans(scansData);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDelete = async (id, e) => {
    e.preventDefault();
    if (confirm("Are you sure you want to delete this scan record and its reports?")) {
      await scansApi.delete(id);
      fetchData();
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5" /> Completed
          </span>
        );
      case 'running':
      case 'queued':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping"></span> In Progress
          </span>
        );
      case 'cancelled':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-500/10 text-slate-400 border border-slate-500/30">
            <Clock className="w-3.5 h-3.5" /> Cancelled
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/30">
            <XCircle className="w-3.5 h-3.5" /> Failed
          </span>
        );
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-gradient-to-r from-dark-card to-dark-bg border border-dark-border p-6 rounded-2xl">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Security Auditing Dashboard</h2>
          <p className="text-sm text-slate-400 mt-1">
            Orchestrate multi-cloud posture assessments and inspect real-time audit logs.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="p-2.5 rounded-xl border border-dark-border text-slate-400 hover:text-white hover:bg-dark-card transition"
            title="Refresh"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <Link
            to="/new-scan"
            className="flex items-center gap-2 bg-brand-500 hover:bg-brand-600 text-slate-950 font-semibold px-4 py-2.5 rounded-xl shadow-lg shadow-brand-500/20 transition"
          >
            <PlayCircle className="w-5 h-5" />
            <span>Launch New Scan</span>
          </Link>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-dark-card border border-dark-border p-5 rounded-2xl shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Total Audits</span>
            <Cloud className="w-4 h-4 text-brand-500" />
          </div>
          <div className="text-3xl font-bold text-white mt-2">
            {stats?.total_scans ?? 0}
          </div>
          <div className="text-xs text-slate-500 mt-1">Across all cloud environments</div>
        </div>

        <div className="bg-dark-card border border-dark-border p-5 rounded-2xl shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Completed</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">
            {stats?.status_counts?.completed ?? 0}
          </div>
          <div className="text-xs text-slate-500 mt-1">Reports generated and archived</div>
        </div>

        <div className="bg-dark-card border border-dark-border p-5 rounded-2xl shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Active / Running</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-bold text-amber-400 mt-2">
            {(stats?.status_counts?.running || 0) + (stats?.status_counts?.queued || 0)}
          </div>
          <div className="text-xs text-slate-500 mt-1">Streaming live stdout</div>
        </div>

        <div className="bg-dark-card border border-dark-border p-5 rounded-2xl shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
            <span>Failed / Errors</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-3xl font-bold text-red-400 mt-2">
            {stats?.status_counts?.failed ?? 0}
          </div>
          <div className="text-xs text-slate-500 mt-1">Authentication or API faults</div>
        </div>
      </div>

      {/* Recent Scans Table */}
      <div className="bg-dark-card border border-dark-border rounded-2xl overflow-hidden shadow-xl">
        <div className="p-5 border-b border-dark-border flex items-center justify-between">
          <h3 className="text-base font-semibold text-white">Recent Cloud Audits</h3>
          <Link to="/reports" className="text-xs text-brand-500 hover:underline flex items-center gap-1 font-medium">
            View All Reports <ArrowUpRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-dark-bg/60 text-xs uppercase text-slate-400 font-semibold border-b border-dark-border">
              <tr>
                <th className="px-6 py-3.5">Provider</th>
                <th className="px-6 py-3.5">Started At</th>
                <th className="px-6 py-3.5">Status</th>
                <th className="px-6 py-3.5">Findings</th>
                <th className="px-6 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border/60">
              {scans.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-10 text-center text-slate-500 italic">
                    No scans have been initiated yet. Click "Launch New Scan" to begin.
                  </td>
                </tr>
              ) : (
                scans.slice(0, 8).map((scan) => {
                  const provInfo = providerLogos[scan.provider] || { name: scan.provider.toUpperCase(), color: 'text-slate-300 bg-slate-500/10 border-slate-500/30' };
                  return (
                    <tr key={scan.id} className="hover:bg-dark-bg/30 transition">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <span className={`px-2.5 py-1 rounded-lg text-xs font-bold uppercase tracking-wider border ${provInfo.color}`}>
                            {scan.provider}
                          </span>
                          <span className="font-medium text-white">{provInfo.name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-xs text-slate-400">
                        {scan.start_time ? new Date(scan.start_time).toLocaleString() : '-'}
                      </td>
                      <td className="px-6 py-4">
                        {getStatusBadge(scan.status)}
                      </td>
                      <td className="px-6 py-4 text-xs font-medium">
                        {scan.summary?.findings_count !== undefined ? (
                          <span className="text-amber-400 bg-amber-400/10 px-2 py-0.5 rounded border border-amber-400/20">
                            {scan.summary.findings_count} Rules Triggered
                          </span>
                        ) : (
                          <span className="text-slate-500">-</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Link
                            to={`/scans/${scan.id}`}
                            className="text-xs bg-dark-bg hover:bg-dark-border text-slate-300 hover:text-white px-3 py-1.5 rounded-lg border border-dark-border transition"
                          >
                            Logs
                          </Link>
                          {scan.report_path && (
                            <a
                              href={scan.report_path}
                              target="_blank"
                              rel="noreferrer"
                              className="text-xs bg-brand-500/10 hover:bg-brand-500/20 text-brand-500 font-medium px-3 py-1.5 rounded-lg border border-brand-500/30 flex items-center gap-1 transition"
                            >
                              Report <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                          <button
                            onClick={(e) => handleDelete(scan.id, e)}
                            className="p-1.5 text-slate-500 hover:text-red-400 rounded-lg hover:bg-red-500/10 transition"
                            title="Delete Scan"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
