"use client";

import { useState, useEffect } from 'react';
import { BarChart3, Clock, DollarSign, AlertTriangle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function AnalyticsDashboard() {
  const [stats, setStats] = useState({
    total_requests: 0,
    avg_total_latency_ms: 0,
    avg_jev_latency_ms: 0,
    route_distribution: {},
    total_cost_usd: 0,
    estimated_savings_usd: 0
  });

  const [latencyData, setLatencyData] = useState<any[]>([]);

  const fetchStats = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/v1/analytics/stats`);
      const data = await res.json();
      setStats(data);
      
      // Build real-time latency chart on client side
      const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      setLatencyData(prev => {
        const newData = [...prev, { time: now, jev: data.avg_jev_latency_ms, system2: data.avg_total_latency_ms }];
        if (newData.length > 8) return newData.slice(1);
        return newData;
      });
    } catch (e) {
      console.error("Failed to fetch stats", e);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 3000);
    return () => clearInterval(interval);
  }, []);

  // Compute derived values for UI
  const sys2Count = Object.entries(stats.route_distribution)
    .filter(([k]) => k.includes('SYSTEM2'))
    .reduce((sum, [_, v]) => sum + (v as number), 0);
    
  const rlcdEscalationRate = stats.total_requests > 0 
    ? ((sys2Count / stats.total_requests) * 100).toFixed(1) 
    : "0.0";

  // Parse route distribution for Pie Chart
  const routeColors: Record<string, string> = {
    'FAST_PATH_LOCAL': '#34d399',
    'ALLOW_FAST_PATH': '#34d399',
    'ESCALATE_TO_SYSTEM2': '#fbbf24',
    'SYSTEM2_APPROVED': '#fbbf24',
    'SYSTEM2_BLOCK': '#f97316',
    'BLOCK': '#f87171',
    'BLOCK_IMMEDIATELY': '#f87171'
  };

  const routeData = Object.entries(stats.route_distribution).map(([name, value]) => ({
    name: name.replace(/_/g, ' '),
    value: value,
    color: routeColors[name] || '#6366f1'
  }));

  // Calculate percentages
  const totalRoutes = routeData.reduce((sum, item) => sum + (item.value as number), 0);
  const routeDataWithPercentages = routeData.map(item => ({
    ...item,
    percentage: totalRoutes > 0 ? (((item.value as number) / totalRoutes) * 100).toFixed(1) : 0
  }));

  return (
    <div className="space-y-10 animate-in fade-in duration-700">
      <div>
        <h2 className="text-4xl font-bold tracking-tight text-white">Analytics Overview</h2>
        <p className="text-neutral-400 mt-2 text-lg">Live metrics streamed from PostgreSQL.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Decisions', value: stats.total_requests.toLocaleString(), icon: BarChart3, color: 'text-blue-400', bg: 'bg-blue-400/10' },
          { label: 'Avg Latency', value: `${stats.avg_total_latency_ms} ms`, icon: Clock, color: 'text-indigo-400', bg: 'bg-indigo-400/10' },
          { label: 'RLCD Escalation', value: `${rlcdEscalationRate}%`, icon: AlertTriangle, color: 'text-amber-400', bg: 'bg-amber-400/10' },
          { label: 'Total Savings', value: `$${stats.estimated_savings_usd.toFixed(2)}`, icon: DollarSign, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
        ].map((kpi, i) => (
          <div key={i} className="p-7 bg-neutral-900/40 border border-neutral-800/60 rounded-3xl backdrop-blur-md flex flex-col gap-4 shadow-xl hover:border-neutral-700 transition-colors">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-neutral-400 tracking-wide uppercase">{kpi.label}</span>
              <div className={`p-2 rounded-xl ${kpi.bg}`}>
                <kpi.icon className={`w-5 h-5 ${kpi.color}`} />
              </div>
            </div>
            <span className="text-4xl font-bold text-white tracking-tight">{kpi.value}</span>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Latency Chart */}
        <div className="lg:col-span-2 p-8 bg-neutral-900/40 border border-neutral-800/60 rounded-3xl backdrop-blur-md shadow-xl">
          <h3 className="text-xl font-semibold mb-8 text-white">Live Average Latency Trends (ms)</h3>
          <div className="h-[320px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={latencyData}>
                <defs>
                  <linearGradient id="colorJev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#818cf8" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#818cf8" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorSys2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#fbbf24" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#fbbf24" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" stroke="#737373" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#737373" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#171717', border: '1px solid #262626', borderRadius: '12px', color: '#fff' }} 
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="jev" stroke="#818cf8" strokeWidth={3} fillOpacity={1} fill="url(#colorJev)" name="Jev Fast Path" />
                <Area type="monotone" dataKey="system2" stroke="#fbbf24" strokeWidth={3} fillOpacity={1} fill="url(#colorSys2)" name="System 2 (Total)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Route Distribution */}
        <div className="p-8 bg-neutral-900/40 border border-neutral-800/60 rounded-3xl backdrop-blur-md shadow-xl">
          <h3 className="text-xl font-semibold mb-8 text-white">Live Route Distribution</h3>
          <div className="h-[260px] w-full flex items-center justify-center">
            {routeData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={routeData} cx="50%" cy="50%" innerRadius={70} outerRadius={110} paddingAngle={6} dataKey="value" stroke="none">
                    {routeData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#171717', border: '1px solid #262626', borderRadius: '12px' }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-neutral-500">Waiting for data...</p>
            )}
          </div>
          <div className="flex flex-col gap-4 mt-8">
            {routeDataWithPercentages.map((route, i) => (
              <div key={i} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-3 text-neutral-300">
                  <div className="w-4 h-4 rounded-full shadow-sm" style={{ backgroundColor: route.color }} />
                  {route.name}
                </div>
                <span className="font-semibold text-white">{route.percentage}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
