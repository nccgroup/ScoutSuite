import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Lock, User, AlertCircle, ArrowRight } from 'lucide-react';
import { authApi } from '../api';

export default function Login() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await authApi.login(username, password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to authenticate. Check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center p-4 relative overflow-hidden">
      {/* Glow Effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="w-full max-w-md bg-dark-card border border-dark-border rounded-2xl p-8 shadow-2xl relative z-10">
        <div className="flex flex-col items-center text-center mb-8">
          <div className="bg-brand-500/20 p-3.5 rounded-2xl text-brand-500 border border-brand-500/30 mb-4 shadow-lg">
            <Shield className="w-9 h-9" />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">ScoutSuite GUI Console</h2>
          <p className="text-sm text-slate-400 mt-1">Multi-Cloud Security Auditing Engine</p>
        </div>

        {error && (
          <div className="mb-6 p-3.5 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center gap-3 text-sm text-red-400">
            <AlertCircle className="w-5 h-5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Username
            </label>
            <div className="relative">
              <User className="w-5 h-5 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin"
                className="w-full bg-dark-bg border border-dark-border rounded-xl pl-11 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="w-5 h-5 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-dark-bg border border-dark-border rounded-xl pl-11 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 bg-brand-500 hover:bg-brand-600 disabled:opacity-50 text-slate-950 font-semibold py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-brand-500/20 transition cursor-pointer"
          >
            {loading ? (
              <span className="inline-block w-5 h-5 border-2 border-slate-900 border-t-transparent rounded-full animate-spin"></span>
            ) : (
              <>
                <span>Sign In to Console</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-dark-border text-center text-xs text-slate-500">
          Default credentials: <span className="font-mono text-slate-400">admin / admin123</span>
        </div>
      </div>
    </div>
  );
}
