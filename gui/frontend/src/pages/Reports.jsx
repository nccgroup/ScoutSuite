import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, ExternalLink, Trash2, ShieldAlert,
  Clock, CheckCircle2, XCircle, Search, Filter
} from 'lucide-react';
import { scansApi } from '../api';

export default function Reports() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProvider, setSelectedProvider] = useState('all');

  const fetchScans = async () => {
    try {
      setLoading(true);
      const data = await scansApi.list();
      setScans(data);
    } catch (err) {
      console.error("Failed to load reports:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScans();
  }, []);

  const handleDelete = async (id) => {
    if (!confirm("Delete this report and its associated output files?")) return;
    try {
      await scansApi.delete(id);
      fetchScans();
    } catch (err) {
      alert("Failed to delete report");
    }
  };

  const filteredScans = scans.filter((scan) => {
    const matchesSearch = 
      scan.provider.toLowerCase().includes(searchTerm.toLowerCase()) ||
      scan.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesProvider = selectedProvider === 'all' || scan.provider === selectedProvider;
    return matchesSearch && matchesProvider;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-dark-card border border-dark-border p-6 rounded-2xl">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Audit Reports Archive</h2>
          <p className="text-sm text-slate-400 mt-1">
            Browse, inspect, and open interactive ScoutSuite HTML vulnerability reports.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search reports..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-dark-bg border border-dark-border rounded-xl pl-9 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 w-44 sm:w-60"
            />
          </div>

          <select
            value={selectedProvider}
            onChange={(e) => setSelectedProvider(e.target.value)}
            className="bg-dark-bg border border-dark-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500"
          >
            <option value="all">All Providers</option>
            <option value="aws">AWS</option>
            <option value="azure">Azure</option>
            <option value="gcp">GCP</option>
            <option value="kubernetes">Kubernetes</option>
            <option value="aliyun">Aliyun</option>
            <option value="do">DigitalOcean</option>
            <option value="oci">OCI</option>
          </select>
        </div>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredScans.length === 0 ? (
          <div className="col-span-full bg-dark-card border border-dark-border border-dashed p-12 rounded-2xl text-center space-y-3">
            <FileText className="w-10 h-10 text-slate-600 mx-auto" />
            <h3 className="text-base font-semibold text-white">No Reports Available</h3>
            <p className="text-sm text-slate-400 max-w-md mx-auto">
              Completed audit sessions will automatically store interactive HTML reports here.
            </p>
          </div>
        ) : (
          filteredScans.map((scan) => (
            <div
              key={scan.id}
              className="bg-dark-card border border-dark-border p-6 rounded-2xl shadow-xl flex flex-col justify-between space-y-5 hover:border-slate-600 transition"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-brand-500/10 text-brand-400 border border-brand-500/20">
                    {scan.provider}
                  </span>
                  <div className="flex items-center gap-2">
                    <Link
                      to={`/scans/${scan.id}`}
                      className="text-xs bg-dark-bg hover:bg-dark-border text-slate-300 hover:text-white px-2.5 py-1 rounded-lg border border-dark-border transition"
                    >
                      Logs
                    </Link>
                    <button
                      onClick={() => handleDelete(scan.id)}
                      className="p-1 text-slate-500 hover:text-red-400 rounded-lg hover:bg-red-500/10 transition"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <div className="mt-4">
                  <h3 className="text-base font-semibold text-white">
                    {scan.provider.toUpperCase()} Security Audit
                  </h3>
                  <div className="flex items-center gap-2 text-xs text-slate-400 mt-1">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{scan.start_time ? new Date(scan.start_time).toLocaleString() : '-'}</span>
                  </div>
                </div>

                {/* Findings summary badge */}
                <div className="mt-4 bg-dark-bg/60 p-3.5 rounded-xl border border-dark-border space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Audit Status:</span>
                    <span className="font-semibold capitalize text-slate-200">{scan.status}</span>
                  </div>
                  {scan.summary?.findings_count !== undefined && (
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-slate-400">Rules Triggered:</span>
                      <span className="font-semibold text-amber-400">
                        {scan.summary.findings_count}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              <div>
                {scan.report_path ? (
                  <a
                    href={scan.report_path}
                    target="_blank"
                    rel="noreferrer"
                    className="w-full flex items-center justify-center gap-2 bg-brand-500 hover:bg-brand-600 text-slate-950 font-semibold text-xs py-2.5 px-4 rounded-xl shadow-lg shadow-brand-500/20 transition cursor-pointer"
                  >
                    <FileText className="w-4 h-4" />
                    <span>Open HTML Report</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                ) : (
                  <Link
                    to={`/scans/${scan.id}`}
                    className="w-full flex items-center justify-center gap-2 bg-dark-bg border border-dark-border text-slate-300 hover:text-white text-xs py-2.5 px-4 rounded-xl transition"
                  >
                    <span>Inspect Live Console</span>
                  </Link>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
