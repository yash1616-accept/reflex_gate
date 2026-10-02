"use client";

import { useState, useEffect } from 'react';
import { Search, ShieldAlert, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';

interface LogEntry {
  id: string;
  agent: string;
  tool: string;
  risk: number;
  confidence: number;
  route: string;
  time: string;
}

export default function LogsPage() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/v1/logs`);
      const data = await res.json();
      setLogs(data.logs || []);
    } catch (e) {
      console.error("Failed to fetch logs", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 3000);
    return () => clearInterval(interval);
  }, []);

  const getRiskBadge = (risk: number) => {
    if (risk <= 2) return <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold flex items-center gap-1 w-max"><CheckCircle2 className="w-3 h-3"/> Low ({risk})</span>;
    if (risk === 3) return <span className="px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-400 text-xs font-semibold flex items-center gap-1 w-max"><AlertCircle className="w-3 h-3"/> Med ({risk})</span>;
    return <span className="px-2.5 py-1 rounded-full bg-red-500/10 text-red-400 text-xs font-semibold flex items-center gap-1 w-max"><ShieldAlert className="w-3 h-3"/> High ({risk})</span>;
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-white">Live Audit Stream</h2>
          <p className="text-neutral-400 mt-1">Real-time inspection of agent actions pulling from PostgreSQL.</p>
        </div>
        <div className="relative">
          <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-500" />
          <input 
            type="text" 
            placeholder="Search agents or tools..." 
            className="pl-10 pr-4 py-2.5 bg-neutral-900/50 border border-neutral-800 rounded-xl focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 text-sm w-72 text-white transition-all shadow-inner"
          />
        </div>
      </div>

      <div className="bg-neutral-900/40 border border-neutral-800/60 rounded-3xl overflow-hidden backdrop-blur-md shadow-xl min-h-[400px] relative">
        {loading && logs.length === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="bg-neutral-800/30 text-neutral-400 border-b border-neutral-800/60">
              <tr>
                <th className="px-6 py-5 font-semibold">Timestamp</th>
                <th className="px-6 py-5 font-semibold">Agent ID</th>
                <th className="px-6 py-5 font-semibold">Proposed Tool</th>
                <th className="px-6 py-5 font-semibold">Risk Score</th>
                <th className="px-6 py-5 font-semibold">RLCD Confidence</th>
                <th className="px-6 py-5 font-semibold">Execution Route</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800/60 text-neutral-300">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-neutral-800/40 transition-colors cursor-pointer group">
                  <td className="px-6 py-4 whitespace-nowrap text-neutral-400">{log.time}</td>
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-white">{log.agent}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-indigo-300 font-mono text-xs bg-indigo-500/5 rounded-lg inline-block mt-2 ml-4 px-2 py-1">{log.tool}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{getRiskBadge(log.risk)}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-3">
                      <div className="w-20 h-1.5 bg-neutral-800 rounded-full overflow-hidden">
                        <div className="h-full bg-blue-500 rounded-full" style={{ width: `${log.confidence * 100}%` }} />
                      </div>
                      <span className="text-xs text-neutral-400 font-medium">{(log.confidence * 100).toFixed(0)}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2.5 py-1 rounded-md text-xs font-semibold border shadow-sm ${
                      log.route === 'Fast Path' ? 'border-emerald-500/20 text-emerald-400 bg-emerald-500/10' :
                      log.route === 'System 2' ? 'border-amber-500/20 text-amber-400 bg-amber-500/10' :
                      'border-red-500/20 text-red-400 bg-red-500/10'
                    }`}>
                      {log.route}
                    </span>
                  </td>
                </tr>
              ))}
              {logs.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-neutral-500 text-lg">
                    No evaluations logged yet. Waiting for Agents...
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
