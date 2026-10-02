"use client";

import { useState } from 'react';
import { Sliders, Save, Shield } from 'lucide-react';

export default function SettingsPage() {
  const [threshold, setThreshold] = useState(0.75);
  const [system2Enabled, setSystem2Enabled] = useState(true);

  const handleSave = () => {
    alert("Configuration saved successfully!");
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-700 max-w-4xl">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-white">Calibration & Routing</h2>
        <p className="text-neutral-400 mt-1">Fine-tune the ReflexGate Engine thresholds.</p>
      </div>

      <div className="bg-neutral-900/40 border border-neutral-800/60 rounded-3xl p-8 backdrop-blur-md shadow-xl space-y-10">
        <div className="flex items-start gap-5">
          <div className="p-3.5 bg-indigo-500/10 rounded-2xl text-indigo-400 border border-indigo-500/20 shadow-inner">
            <Sliders className="w-6 h-6" />
          </div>
          <div className="flex-1 space-y-5 mt-1">
            <div>
              <h3 className="text-lg font-semibold text-white">RLCD Confidence Cutoff</h3>
              <p className="text-sm text-neutral-400 mt-1.5 leading-relaxed">
                If the model's confidence in its safety assessment falls below this threshold, the action will be escalated.
              </p>
            </div>
            <div className="flex items-center gap-6 bg-neutral-900/50 p-4 rounded-2xl border border-neutral-800">
              <input 
                type="range" 
                min="0.5" 
                max="0.95" 
                step="0.01"
                value={threshold}
                onChange={(e) => setThreshold(parseFloat(e.target.value))}
                className="w-full accent-indigo-500 h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer"
              />
              <span className="text-2xl font-bold text-white w-20 text-right">
                {(threshold * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        </div>

        <div className="w-full h-px bg-neutral-800/60" />

        <div className="flex items-start gap-5">
          <div className="p-3.5 bg-amber-500/10 rounded-2xl text-amber-400 border border-amber-500/20 shadow-inner">
            <Shield className="w-6 h-6" />
          </div>
          <div className="flex-1 flex items-center justify-between mt-1">
            <div className="pr-8">
              <h3 className="text-lg font-semibold text-white">Automated System 2 Fallback</h3>
              <p className="text-sm text-neutral-400 mt-1.5 leading-relaxed">
                When enabled, uncertain actions automatically route to a heavy reasoning model (e.g., GPT-4o) instead of blocking immediately.
              </p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer shrink-0">
              <input type="checkbox" className="sr-only peer" checked={system2Enabled} onChange={() => setSystem2Enabled(!system2Enabled)} />
              <div className="w-14 h-7 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-indigo-500"></div>
            </label>
          </div>
        </div>

        <div className="w-full h-px bg-neutral-800/60" />

        <div className="flex justify-end pt-2">
          <button 
            onClick={handleSave}
            className="flex items-center gap-2 px-6 py-3 bg-indigo-500 hover:bg-indigo-400 text-white rounded-xl font-semibold transition-all shadow-lg shadow-indigo-500/20 active:scale-95"
          >
            <Save className="w-4 h-4" />
            Save Configuration
          </button>
        </div>
      </div>
    </div>
  );
}
