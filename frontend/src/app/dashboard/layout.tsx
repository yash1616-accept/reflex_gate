import Link from 'next/link';
import { Activity, LayoutDashboard, Settings, FileText } from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-[#0a0a0a] text-neutral-50 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-72 border-r border-neutral-800/60 bg-neutral-900/30 flex flex-col backdrop-blur-xl">
        <div className="p-6 border-b border-neutral-800/60">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent flex items-center gap-3">
            <Activity className="w-7 h-7 text-indigo-400" />
            ReflexGate
          </h1>
        </div>
        <nav className="flex-1 p-6 space-y-3">
          <Link href="/dashboard" className="flex items-center gap-4 px-4 py-3.5 text-neutral-300 hover:text-white hover:bg-neutral-800/50 rounded-xl transition-all font-medium">
            <LayoutDashboard className="w-5 h-5" />
            Analytics
          </Link>
          <Link href="/dashboard/logs" className="flex items-center gap-4 px-4 py-3.5 text-neutral-300 hover:text-white hover:bg-neutral-800/50 rounded-xl transition-all font-medium">
            <FileText className="w-5 h-5" />
            Live Audit Stream
          </Link>
          <Link href="/dashboard/settings" className="flex items-center gap-4 px-4 py-3.5 text-neutral-300 hover:text-white hover:bg-neutral-800/50 rounded-xl transition-all font-medium">
            <Settings className="w-5 h-5" />
            Calibration
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto p-10 relative">
        <div className="absolute top-[-20%] left-[20%] w-[500px] h-[500px] bg-indigo-600/10 blur-[120px] rounded-full pointer-events-none" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[600px] h-[600px] bg-purple-600/10 blur-[150px] rounded-full pointer-events-none" />
        {children}
      </main>
    </div>
  );
}
