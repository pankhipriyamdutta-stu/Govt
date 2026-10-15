import React, { useState, useEffect } from 'react';
import {
  Settings,
  Users,
  Database,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Sliders,
  Sparkles,
  RefreshCw,
  Cpu,
  FileCheck2,
  ShieldCheck
} from 'lucide-react';
import { VerificationQueueItem, EvalCaseItem, UserProfile } from '../types';
import { api } from '../api';

interface AdminControlProps {
  userProfile: UserProfile | null;
}

export const AdminControl: React.FC<AdminControlProps> = ({ userProfile }) => {
  const [activeTab, setActiveTab] = useState<'queue' | 'evals' | 'sources' | 'config'>('queue');
  const [queueItems, setQueueItems] = useState<VerificationQueueItem[]>([]);
  const [evalCases, setEvalCases] = useState<EvalCaseItem[]>([]);
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Decision Modal State
  const [selectedQueueItem, setSelectedQueueItem] = useState<VerificationQueueItem | null>(null);
  const [decisionType, setDecisionType] = useState('APPROVED_TRUSTED');
  const [rationale, setRationale] = useState('');
  const [decisionFeedback, setDecisionFeedback] = useState<string | null>(null);

  const fetchData = () => {
    setLoading(true);
    Promise.all([
      api.getVerificationQueue().catch(() => []),
      api.getEvaluationSuite().catch(() => []),
      api.getSources().catch(() => [])
    ]).then(([q, ev, s]) => {
      setQueueItems(q);
      setEvalCases(ev);
      setSources(s);
      setLoading(false);
    });
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRecordDecision = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedQueueItem || !rationale.trim()) return;
    try {
      setDecisionFeedback(null);
      await api.recordVerificationDecision(selectedQueueItem.id, decisionType, rationale.trim());
      setDecisionFeedback("Decision successfully committed to authoritative register.");
      setSelectedQueueItem(null);
      setRationale('');
      fetchData();
    } catch (err: any) {
      setDecisionFeedback(`Error: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <Settings className="w-4 h-4" />
            <span>Governance & Platform Administration</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white">
            Administration & Government Control
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Verification queues, approved source registry, trust-policy enforcement, and AI evaluation benchmarks
          </p>
        </div>

        <button
          onClick={fetchData}
          className="bg-[#070D1E] hover:bg-[#1C2541] border border-slate-700 text-slate-200 px-3.5 py-2 rounded-xl text-xs flex items-center space-x-2 transition"
        >
          <RefreshCw className="w-3.5 h-3.5 text-cyan-400" />
          <span>Refresh Governance State</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-[#1C2541] pb-3">
        <button
          onClick={() => setActiveTab('queue')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'queue'
              ? 'bg-cyan-500 text-slate-950 font-bold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <FileCheck2 className="w-4 h-4" />
          <span>Verification Queue ({queueItems.filter(q => q.current_status === 'PENDING_REVIEW').length})</span>
        </button>

        <button
          onClick={() => setActiveTab('evals')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'evals'
              ? 'bg-cyan-500 text-slate-950 font-bold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <Sparkles className="w-4 h-4" />
          <span>AI Evaluation Benchmarks ({evalCases.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('sources')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'sources'
              ? 'bg-cyan-500 text-slate-950 font-bold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Approved Sources ({sources.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('config')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'config'
              ? 'bg-cyan-500 text-slate-950 font-bold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <Sliders className="w-4 h-4" />
          <span>Trust Policy & Model Config</span>
        </button>
      </div>

      {decisionFeedback && (
        <div className={`p-4 rounded-xl text-xs ${
          decisionFeedback.includes('Error')
            ? 'bg-rose-500/10 border border-rose-500/30 text-rose-300'
            : 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300'
        }`}>
          {decisionFeedback}
        </div>
      )}

      {/* TAB 1: VERIFICATION QUEUE */}
      {activeTab === 'queue' && (
        <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white">Pending Document Verification & Provenance Queue</h2>
              <p className="text-xs text-slate-400">
                Documents flagged with third-party converter metadata or awaiting institutional officer sign-off
              </p>
            </div>
            <div className="text-xs text-slate-400 font-mono">
              Current Role: <span className="text-cyan-400 font-bold">{userProfile?.role_name}</span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#070D1E] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/60">
                <tr>
                  <th className="py-2.5 px-3">Doc ID</th>
                  <th className="py-2.5 px-3">Document Title</th>
                  <th className="py-2.5 px-3">Department</th>
                  <th className="py-2.5 px-3">Provenance Flags</th>
                  <th className="py-2.5 px-3">Current Status</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                {queueItems.map((item) => (
                  <tr key={item.id} className="hover:bg-[#1C2541]/80 transition">
                    <td className="py-3 px-3 text-cyan-400 font-bold">{item.document_id}</td>
                    <td className="py-3 px-3 font-sans font-semibold text-white max-w-xs truncate">
                      {item.document_title}
                    </td>
                    <td className="py-3 px-3 font-sans text-slate-300">{item.department}</td>
                    <td className="py-3 px-3 font-sans text-amber-300 max-w-sm truncate text-[11px]">
                      {item.reviewer_notes}
                    </td>
                    <td className="py-3 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        item.current_status === 'APPROVED_TRUSTED'
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : 'bg-amber-500/20 text-amber-300'
                      }`}>
                        {item.current_status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right">
                      <button
                        onClick={() => setSelectedQueueItem(item)}
                        className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-3 py-1 rounded text-xs transition"
                      >
                        Audit & Decide
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 2: AI EVALUATION BENCHMARKS */}
      {activeTab === 'evals' && (
        <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-4">
          <div>
            <h2 className="text-base font-bold text-white">Gold-Standard AI Grounding & Abstention Benchmark Suite</h2>
            <p className="text-xs text-slate-400">
              Deterministic evaluation cases benchmarking factual support, citation accuracy, and correct abstention
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#070D1E] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/60">
                <tr>
                  <th className="py-2.5 px-3">Eval ID</th>
                  <th className="py-2.5 px-3">Benchmark Test Query</th>
                  <th className="py-2.5 px-3">Expected Outcome</th>
                  <th className="py-2.5 px-3">Factual Score</th>
                  <th className="py-2.5 px-3">Citation Acc</th>
                  <th className="py-2.5 px-3">Abstention Acc</th>
                  <th className="py-2.5 px-3">Result</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                {evalCases.map((ev) => (
                  <tr key={ev.evaluation_id} className="hover:bg-[#1C2541]/80 transition">
                    <td className="py-3 px-3 text-cyan-400 font-bold">{ev.evaluation_id}</td>
                    <td className="py-3 px-3 font-sans text-white max-w-sm truncate">{ev.query}</td>
                    <td className="py-3 px-3 font-bold text-amber-300">{ev.expected_status}</td>
                    <td className="py-3 px-3 text-emerald-400">{(ev.factual_support_score * 100).toFixed(0)}%</td>
                    <td className="py-3 px-3 text-emerald-400">{(ev.citation_accuracy * 100).toFixed(0)}%</td>
                    <td className="py-3 px-3 text-emerald-400">{(ev.abstention_correctness * 100).toFixed(0)}%</td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[10px]">
                        {ev.result}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 3: APPROVED SOURCES */}
      {activeTab === 'sources' && (
        <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-4">
          <div>
            <h2 className="text-base font-bold text-white">Registered Government Publishing Sources</h2>
            <p className="text-xs text-slate-400">Authoritative portals, state nodal gazettes, and network allowlists</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {sources.map((s) => (
              <div key={s.source_id} className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-cyan-400 font-bold">{s.source_id}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    s.authority_tier.includes('ZONE_1')
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                  }`}>
                    {s.authority_tier}
                  </span>
                </div>
                <div className="font-bold text-white text-sm">{s.source_name}</div>
                <div className="text-slate-400">Department: {s.department}</div>
                <div className="font-mono text-cyan-300 text-[11px] truncate">
                  Domain: {s.verified_domain}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: TRUST POLICY & CONFIGURATION */}
      {activeTab === 'config' && (
        <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-6 text-xs">
          <div>
            <h2 className="text-base font-bold text-white">Platform Trust Policy & Model Orchestration</h2>
            <p className="text-xs text-slate-400">System security thresholds, AI model routing, and grounding constraints</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-[#070D1E] border border-slate-800 p-5 rounded-xl space-y-4">
              <div className="font-bold text-white text-sm flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Grounding & Abstention Policies</span>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span>Enforce Primary Gazette Authority Only</span>
                  <span className="text-emerald-400 font-bold font-mono">ENABLED</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Strict Abstention Threshold</span>
                  <span className="text-cyan-400 font-bold font-mono">0.85 (High Precision)</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Quarantine Execution Shield</span>
                  <span className="text-emerald-400 font-bold font-mono">ENABLED</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Dual Approval on Statute Revocation</span>
                  <span className="text-amber-400 font-bold font-mono">REQUIRED</span>
                </div>
              </div>
            </div>

            <div className="bg-[#070D1E] border border-slate-800 p-5 rounded-xl space-y-4">
              <div className="font-bold text-white text-sm flex items-center space-x-2">
                <Cpu className="w-4 h-4 text-cyan-400" />
                <span>AI Model Provider Abstraction</span>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span>Active Primary Model</span>
                  <span className="text-cyan-400 font-bold font-mono">gemini-2.5-flash / Gemini 3.8</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Sovereign Deterministic Engine</span>
                  <span className="text-emerald-400 font-bold font-mono">STANDBY / AIR-GAP READY</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Max Grounded Context Window</span>
                  <span className="text-slate-300 font-mono">32,768 Tokens</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Temperature (Zero-Creativity)</span>
                  <span className="text-slate-300 font-mono">0.0 (Strict Grounding)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* DECISION RECORDING MODAL */}
      {selectedQueueItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-[#0B132B] border border-[#29365C] rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4 text-xs">
            <h3 className="text-base font-bold text-white">Record Verification Officer Decision</h3>
            <div className="bg-[#070D1E] p-3 rounded-xl border border-slate-800 space-y-1">
              <div>Doc ID: <span className="font-mono text-cyan-400 font-bold">{selectedQueueItem.document_id}</span></div>
              <div>Title: <span className="font-semibold text-white">{selectedQueueItem.document_title}</span></div>
              <div className="text-amber-300 text-[11px] mt-1">{selectedQueueItem.reviewer_notes}</div>
            </div>

            <form onSubmit={handleRecordDecision} className="space-y-3">
              <div>
                <label className="block text-slate-400 font-semibold mb-1">Decision:</label>
                <select
                  value={decisionType}
                  onChange={(e) => setDecisionType(e.target.value)}
                  className="w-full bg-[#070D1E] border border-slate-700 rounded-xl px-3 py-2 text-slate-200"
                >
                  <option value="APPROVED_TRUSTED">APPROVE AS TRUSTED PRIMARY STATUTE</option>
                  <option value="REJECTED">REJECT (UNTRUSTED THIRD-PARTY TOOL)</option>
                  <option value="NEEDS_AMENDMENT_CHECK">FLAG FOR SECONDARY LEGAL REVIEW</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 font-semibold mb-1">Authoritative Rationale (Required):</label>
                <textarea
                  required
                  rows={3}
                  value={rationale}
                  onChange={(e) => setRationale(e.target.value)}
                  placeholder="Record formal gazette comparison citation or reason for rejection..."
                  className="w-full bg-[#070D1E] border border-slate-700 rounded-xl p-3 text-slate-200 focus:outline-none"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setSelectedQueueItem(null)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-5 py-2 rounded-xl transition"
                >
                  Commit Official Decision
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
