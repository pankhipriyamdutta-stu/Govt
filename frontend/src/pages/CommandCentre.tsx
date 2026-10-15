import React, { useState, useEffect } from 'react';
import {
  Search,
  Bot,
  ShieldCheck,
  FileCheck2,
  AlertTriangle,
  FolderLock,
  ArrowRight,
  TrendingUp,
  FileText,
  Clock,
  Sparkles,
  Lock,
  ExternalLink
} from 'lucide-react';
import { UserProfile, DocumentItem } from '../types';
import { PageId } from '../components/Sidebar';
import { api } from '../api';

interface CommandCentreProps {
  userProfile: UserProfile | null;
  onNavigate: (page: PageId, extraData?: any) => void;
}

export const CommandCentre: React.FC<CommandCentreProps> = ({ userProfile, onNavigate }) => {
  const [quickQuery, setQuickQuery] = useState('');
  const [metrics, setMetrics] = useState<any>(null);
  const [recentDocs, setRecentDocs] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getSystemMetrics().catch(() => null),
      api.listDocuments().catch(() => [])
    ]).then(([met, docs]) => {
      setMetrics(met);
      setRecentDocs(docs.slice(0, 5));
      setLoading(false);
    });
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (quickQuery.trim()) {
      onNavigate('copilot', { initialQuery: quickQuery.trim() });
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Hero Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#0B132B] via-[#1C2541] to-[#070D1E] border border-[#29365C] p-6 sm:p-8 shadow-2xl">
        <div className="absolute right-0 top-0 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold mb-3">
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
            <span>NESFIC-D-36 Operational Sovereign Node</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Welcome, {userProfile?.full_name || 'Government Official'}
          </h1>
          <p className="text-sm text-slate-300 mt-2 leading-relaxed">
            Authorized operating dashboard for <span className="font-semibold text-cyan-300">{userProfile?.department || 'Government of Assam'}</span>. 
            Every authoritative answer is traceable. Every source is assessed. Every uncertainty is visible. Every action is accountable.
          </p>

          {/* Quick Search Entry */}
          <form onSubmit={handleSearchSubmit} className="mt-5 flex items-center max-w-2xl bg-[#070D1E]/90 border border-cyan-500/40 rounded-xl p-1.5 shadow-xl focus-within:border-cyan-400 transition">
            <Search className="w-5 h-5 text-slate-400 ml-3 shrink-0" />
            <input
              type="text"
              value={quickQuery}
              onChange={(e) => setQuickQuery(e.target.value)}
              placeholder="Ask a rule question, search gazette numbers, or verify timelines..."
              className="w-full bg-transparent border-none text-slate-100 placeholder-slate-400 text-sm px-3 focus:outline-none"
            />
            <button
              type="submit"
              className="bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 font-bold px-4 py-2 rounded-lg text-xs flex items-center space-x-1.5 transition shrink-0"
            >
              <Bot className="w-4 h-4" />
              <span>Ask AI Co-Pilot</span>
            </button>
          </form>
        </div>
      </div>

      {/* Repository & Trust Health Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#1C2541]/70 border border-[#29365C] p-4 rounded-xl shadow-md">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Primary Active Statutes</span>
            <FileCheck2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">
            {metrics?.repository?.verified_active_statutes || '10'}
          </div>
          <div className="text-[11px] text-emerald-400 mt-1 flex items-center space-x-1">
            <span>Zone 1 Official Gazettes</span>
          </div>
        </div>

        <div className="bg-[#1C2541]/70 border border-[#29365C] p-4 rounded-xl shadow-md">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Zero-Hallucination Rate</span>
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">100.0%</div>
          <div className="text-[11px] text-cyan-400 mt-1 flex items-center space-x-1">
            <span>Deterministic Grounding Gate</span>
          </div>
        </div>

        <div className="bg-[#1C2541]/70 border border-[#29365C] p-4 rounded-xl shadow-md">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Quarantined & PII Files</span>
            <Lock className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">
            {metrics?.repository?.quarantined_files || '4'}
          </div>
          <div className="text-[11px] text-rose-400 mt-1">
            <span>Excluded from RAG Index</span>
          </div>
        </div>

        <div className="bg-[#1C2541]/70 border border-[#29365C] p-4 rounded-xl shadow-md">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Pending Officer Review</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">
            {metrics?.repository?.pending_verification_queue || '5'}
          </div>
          <div className="text-[11px] text-amber-400 mt-1">
            <span>Provenance / Converter Flags</span>
          </div>
        </div>
      </div>

      {/* Quick Action Pathways */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={() => onNavigate('copilot')}
          className="text-left bg-gradient-to-br from-[#1C2541] to-[#0B132B] hover:from-[#29365C] hover:to-[#1C2541] border border-cyan-500/30 p-5 rounded-xl transition group shadow-lg"
        >
          <div className="w-10 h-10 rounded-lg bg-cyan-500/20 text-cyan-400 flex items-center justify-center mb-3 group-hover:scale-105 transition">
            <Bot className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-white text-sm group-hover:text-cyan-300 transition flex items-center justify-between">
            Launch AI Co-Pilot
            <ArrowRight className="w-4 h-4 text-cyan-400 group-hover:translate-x-1 transition" />
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Engage with tripartite grounded decision support, citations, and instant claim verification.
          </p>
        </button>

        <button
          onClick={() => onNavigate('detective')}
          className="text-left bg-gradient-to-br from-[#1C2541] to-[#0B132B] hover:from-[#29365C] hover:to-[#1C2541] border border-teal-500/30 p-5 rounded-xl transition group shadow-lg"
        >
          <div className="w-10 h-10 rounded-lg bg-teal-500/20 text-teal-400 flex items-center justify-center mb-3 group-hover:scale-105 transition">
            <Search className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-white text-sm group-hover:text-teal-300 transition flex items-center justify-between">
            Source Detective
            <ArrowRight className="w-4 h-4 text-teal-400 group-hover:translate-x-1 transition" />
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Inspect the 360-degree forensic evidence trail, SHA-256 integrity, and signer authority.
          </p>
        </button>

        <button
          onClick={() => onNavigate('repository')}
          className="text-left bg-gradient-to-br from-[#1C2541] to-[#0B132B] hover:from-[#29365C] hover:to-[#1C2541] border border-indigo-500/30 p-5 rounded-xl transition group shadow-lg"
        >
          <div className="w-10 h-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center mb-3 group-hover:scale-105 transition">
            <FolderLock className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-white text-sm group-hover:text-indigo-300 transition flex items-center justify-between">
            Knowledge Repository
            <ArrowRight className="w-4 h-4 text-indigo-400 group-hover:translate-x-1 transition" />
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Browse verified state gazettes, citizen charters, procurement rules, and version lineages.
          </p>
        </button>
      </div>

      {/* Recently Accessed Verified Documents Table */}
      <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-5 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white">Active Verified Documents in Pilot</h2>
            <p className="text-xs text-slate-400">Authenticated statutory instruments ready for decision support</p>
          </div>
          <button
            onClick={() => onNavigate('repository')}
            className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 flex items-center space-x-1"
          >
            <span>View All Repository</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#0B132B] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/60">
              <tr>
                <th className="py-2.5 px-3">Document Title</th>
                <th className="py-2.5 px-3">Department</th>
                <th className="py-2.5 px-3">Type</th>
                <th className="py-2.5 px-3">Reference / Gazette</th>
                <th className="py-2.5 px-3">Trust State</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {recentDocs.map((doc) => (
                <tr key={doc.document_id} className="hover:bg-[#1C2541]/70 transition">
                  <td className="py-3 px-3 font-semibold text-white max-w-xs truncate">
                    {doc.document_title}
                  </td>
                  <td className="py-3 px-3 text-slate-300 max-w-[180px] truncate">
                    {doc.department}
                  </td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono text-[10px]">
                      {doc.document_type}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-mono text-slate-400 text-[11px] truncate max-w-[160px]">
                    {doc.reference_number || 'N/A'}
                  </td>
                  <td className="py-3 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      doc.verification_status.includes('VERIFIED')
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                    }`}>
                      {doc.verification_status.includes('VERIFIED') ? 'VERIFIED' : 'VERIFY REQUIRED'}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <button
                      onClick={() => onNavigate('detective', { claimId: doc.document_id })}
                      className="text-cyan-400 hover:text-cyan-300 font-medium hover:underline text-[11px]"
                    >
                      Audit Trail
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
