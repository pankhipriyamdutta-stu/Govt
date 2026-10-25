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
  ShieldCheck,
  Key,
  Zap,
  Check,
  Play,
  Eye,
  EyeOff,
  BarChart3,
  Layers
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

  // AI Master & Training Config State
  const [aiConfig, setAiConfig] = useState<any>(null);
  const [trainingStatus, setTrainingStatus] = useState<any>(null);
  const [apiKeyInput, setApiKeyInput] = useState('');
  const [selectedModel, setSelectedModel] = useState('gemini-2.5-flash');
  const [showApiKey, setShowApiKey] = useState(false);
  const [testResult, setTestResult] = useState<any>(null);
  const [testingConnection, setTestingConnection] = useState(false);
  const [savingConfig, setSavingConfig] = useState(false);
  const [rebuildingDataset, setRebuildingDataset] = useState(false);
  const [runningEval, setRunningEval] = useState(false);
  const [evalResults, setEvalResults] = useState<any>(null);
  const [aiFeedback, setAiFeedback] = useState<string | null>(null);

  const fetchData = () => {
    setLoading(true);
    Promise.all([
      api.getVerificationQueue().catch(() => []),
      api.getEvaluationSuite().catch(() => []),
      api.getSources().catch(() => []),
      api.getAIConfig().catch(() => null),
      api.getAITrainingStatus().catch(() => null)
    ]).then(([q, ev, s, cfg, tr]) => {
      setQueueItems(q);
      setEvalCases(ev);
      setSources(s);
      if (cfg) {
        setAiConfig(cfg);
        setSelectedModel(cfg.active_model || 'gemini-2.5-flash');
      }
      if (tr) {
        setTrainingStatus(tr);
      }
      setLoading(false);
    });
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSaveAIConfig = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingConfig(true);
    setAiFeedback(null);
    try {
      const res = await api.updateAIConfig({
        api_key: apiKeyInput.trim() ? apiKeyInput.trim() : undefined,
        model_name: selectedModel
      });
      setAiFeedback(`Success: ${res.message}`);
      setApiKeyInput('');
      const updatedCfg = await api.getAIConfig();
      setAiConfig(updatedCfg);
    } catch (err: any) {
      setAiFeedback(`Error saving AI config: ${err.message}`);
    } finally {
      setSavingConfig(false);
    }
  };

  const handleTestConnection = async () => {
    setTestingConnection(true);
    setTestResult(null);
    try {
      const res = await api.testAIConnection(apiKeyInput.trim() || undefined, selectedModel);
      setTestResult(res);
    } catch (err: any) {
      setTestResult({
        connected: false,
        status: 'NETWORK_ERROR',
        message: err.message
      });
    } finally {
      setTestingConnection(false);
    }
  };

  const handleRebuildDataset = async () => {
    setRebuildingDataset(true);
    setAiFeedback(null);
    try {
      const res = await api.rebuildTrainingDataset();
      setAiFeedback(`Dataset Rebuilt: ${res.total_training_pairs} training pairs generated across Gemini SFT and Alpaca formats.`);
      const tr = await api.getAITrainingStatus();
      setTrainingStatus(tr);
    } catch (err: any) {
      setAiFeedback(`Error rebuilding dataset: ${err.message}`);
    } finally {
      setRebuildingDataset(false);
    }
  };

  const handleRunTrainingEval = async () => {
    setRunningEval(true);
    setEvalResults(null);
    try {
      const res = await api.runTrainingEvaluation();
      setEvalResults(res);
    } catch (err: any) {
      setAiFeedback(`Error running evaluation: ${err.message}`);
    } finally {
      setRunningEval(false);
    }
  };

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

      {/* TAB 4: TRUST POLICY, GENERATIVE AI & API MASTER CONSOLE */}
      {activeTab === 'config' && (
        <div className="space-y-6">
          {/* AI Feedback Banner */}
          {aiFeedback && (
            <div className={`p-4 rounded-xl text-xs flex items-center justify-between ${
              aiFeedback.includes('Error')
                ? 'bg-rose-500/10 border border-rose-500/30 text-rose-300'
                : 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300'
            }`}>
              <div className="flex items-center space-x-2">
                {aiFeedback.includes('Error') ? <AlertTriangle className="w-4 h-4 text-rose-400" /> : <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                <span>{aiFeedback}</span>
              </div>
              <button onClick={() => setAiFeedback(null)} className="text-slate-400 hover:text-white">✕</button>
            </div>
          )}

          {/* Top Section: API Orchestration & Dataset Hub */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Card 1: Generative AI API Orchestration */}
            <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-5">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2.5">
                  <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-sm font-bold text-white">Generative AI API & Model Routing</h2>
                    <p className="text-[11px] text-slate-400">Configure Google Gemini LLM API or Sovereign Air-Gapped Engine</p>
                  </div>
                </div>
                <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${
                  aiConfig?.has_api_key
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                    : 'bg-amber-500/10 border-amber-500/30 text-amber-300'
                }`}>
                  {aiConfig?.has_api_key ? '● API Key Active' : '○ Offline Sovereign Mode'}
                </span>
              </div>

              <form onSubmit={handleSaveAIConfig} className="space-y-4 text-xs">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">
                    Select Generative AI Model Architecture:
                  </label>
                  <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    className="w-full bg-[#070D1E] border border-slate-700/80 rounded-xl px-3.5 py-2.5 text-slate-100 text-xs focus:outline-none focus:border-cyan-400"
                  >
                    <option value="gemini-2.5-flash">Google Gemini 2.5 Flash (Recommended — Low Latency & High Reasoning)</option>
                    <option value="gemini-1.5-flash">Google Gemini 1.5 Flash (Production Stable — 1M Context)</option>
                    <option value="gemini-2.0-flash">Google Gemini 2.0 Flash (Next-Gen Multimodal Architecture)</option>
                    <option value="gemini-2.5-pro">Google Gemini 2.5 Pro (Deep Statutory Reasoning & Conflict Resolution)</option>
                    <option value="local-sovereign">Sovereign Neural Grounded Reasoner (Offline Govt Node / Air-Gap)</option>
                  </select>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-slate-300 font-semibold">
                      Google Gemini API Key:
                    </label>
                    {aiConfig?.masked_api_key && (
                      <span className="text-[10px] font-mono text-cyan-400">
                        Configured: {aiConfig.masked_api_key}
                      </span>
                    )}
                  </div>
                  <div className="relative">
                    <input
                      type={showApiKey ? 'text' : 'password'}
                      value={apiKeyInput}
                      onChange={(e) => setApiKeyInput(e.target.value)}
                      placeholder={aiConfig?.has_api_key ? "Leave blank to keep existing key, or enter new key..." : "Enter Google Gemini API Key (e.g. AIzaSy...)"}
                      className="w-full bg-[#070D1E] border border-slate-700/80 rounded-xl px-3.5 py-2.5 pr-10 text-slate-100 placeholder-slate-500 font-mono text-xs focus:outline-none focus:border-cyan-400"
                    />
                    <button
                      type="button"
                      onClick={() => setShowApiKey(!showApiKey)}
                      className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-200"
                    >
                      {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                  <p className="text-[10px] text-slate-500 mt-1">
                    Keys are persisted securely in the system registry. When no key is set, the system executes locally via the Sovereign Grounded Engine.
                  </p>
                </div>

                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <button
                    type="submit"
                    disabled={savingConfig}
                    className="flex-1 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-2.5 px-4 rounded-xl text-xs flex items-center justify-center space-x-2 transition disabled:opacity-50"
                  >
                    {savingConfig ? (
                      <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                    ) : (
                      <>
                        <Check className="w-4 h-4" />
                        <span>Save & Apply AI Configuration</span>
                      </>
                    )}
                  </button>

                  <button
                    type="button"
                    onClick={handleTestConnection}
                    disabled={testingConnection}
                    className="bg-[#070D1E] hover:bg-[#1C2541] border border-slate-700 text-cyan-300 font-semibold py-2.5 px-4 rounded-xl text-xs flex items-center space-x-2 transition disabled:opacity-50"
                  >
                    {testingConnection ? (
                      <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
                    ) : (
                      <>
                        <Zap className="w-4 h-4 text-amber-400" />
                        <span>Test API Connection</span>
                      </>
                    )}
                  </button>
                </div>
              </form>

              {/* Test Connection Result Box */}
              {testResult && (
                <div className={`p-3.5 rounded-xl text-xs border ${
                  testResult.connected
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                    : 'bg-amber-500/10 border-amber-500/30 text-amber-300'
                }`}>
                  <div className="flex items-center space-x-2 font-bold mb-1">
                    {testResult.connected ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                    )}
                    <span>{testResult.status}</span>
                  </div>
                  <div className="text-[11px] leading-relaxed">{testResult.message}</div>
                </div>
              )}
            </div>

            {/* Card 2: AI Training & Reference Dataset Hub */}
            <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-5">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2.5">
                  <div className="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400">
                    <Database className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-sm font-bold text-white">AI Training & Dataset Hub</h2>
                    <p className="text-[11px] text-slate-400">Supervised fine-tuning & in-context dataset compilation</p>
                  </div>
                </div>
                <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                  19 Master Sheets
                </span>
              </div>

              <div className="space-y-3 text-xs">
                <div className="bg-[#070D1E] border border-slate-800 p-3.5 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300 font-semibold">Compiled Training Pairs:</span>
                    <span className="text-cyan-400 font-bold font-mono">
                      {trainingStatus?.total_training_pairs || 8} Ground-Truth Pairs
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300 font-semibold">Gemini SFT JSONL Dataset:</span>
                    <span className="text-emerald-400 font-bold font-mono text-[10px]">READY (gemini_finetune_dataset.jsonl)</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300 font-semibold">Alpaca Instruction Dataset:</span>
                    <span className="text-emerald-400 font-bold font-mono text-[10px]">READY (alpaca_instruct_dataset.json)</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300 font-semibold">In-Context Conditioning Store:</span>
                    <span className="text-emerald-400 font-bold font-mono text-[10px]">ACTIVE (in_context_exemplars.json)</span>
                  </div>
                </div>

                <p className="text-[11px] text-slate-400 leading-relaxed">
                  Training datasets are derived directly from the 19 reference CSV sheets, mapping exact statutory citations, claim-level evidence hashes, and abstention rules to prevent hallucination.
                </p>

                <button
                  type="button"
                  onClick={handleRebuildDataset}
                  disabled={rebuildingDataset}
                  className="w-full bg-[#070D1E] hover:bg-[#1C2541] border border-slate-700 text-slate-200 font-semibold py-2.5 px-4 rounded-xl text-xs flex items-center justify-center space-x-2 transition disabled:opacity-50"
                >
                  {rebuildingDataset ? (
                    <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Rebuild Training Datasets from 19 Master CSV Sheets</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Live AI Training & Grounding Benchmark Suite */}
          <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="flex items-center space-x-2 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-0.5">
                  <BarChart3 className="w-4 h-4" />
                  <span>Validation & Grounding Quality Gate</span>
                </div>
                <h2 className="text-base font-bold text-white">Generative AI Grounding Benchmark Suite</h2>
                <p className="text-xs text-slate-400">
                  Execute deterministic test cases across active AI model to verify factual support, citation validity, and red-team abstention
                </p>
              </div>

              <button
                type="button"
                onClick={handleRunTrainingEval}
                disabled={runningEval}
                className="bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 font-bold py-2.5 px-5 rounded-xl text-xs flex items-center space-x-2 transition shadow-lg shadow-cyan-500/20 disabled:opacity-50"
              >
                {runningEval ? (
                  <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-current" />
                    <span>Run AI Evaluation Benchmark Now</span>
                  </>
                )}
              </button>
            </div>

            {/* Benchmark Execution Scorecards */}
            {evalResults && (
              <div className="space-y-4 pt-2">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl text-center">
                    <div className="text-[11px] text-slate-400 font-semibold uppercase">Total Benchmark Cases</div>
                    <div className="text-2xl font-extrabold text-white mt-1">{evalResults.total_cases}</div>
                  </div>
                  <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl text-center">
                    <div className="text-[11px] text-slate-400 font-semibold uppercase">Validated Passing Cases</div>
                    <div className="text-2xl font-extrabold text-emerald-400 mt-1">{evalResults.passed}</div>
                  </div>
                  <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl text-center">
                    <div className="text-[11px] text-slate-400 font-semibold uppercase">Grounding Accuracy</div>
                    <div className="text-2xl font-extrabold text-cyan-400 mt-1">{evalResults.accuracy_percentage}</div>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-300">
                    <thead className="bg-[#070D1E] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/60">
                      <tr>
                        <th className="py-2.5 px-3">Case ID</th>
                        <th className="py-2.5 px-3">Benchmark Test Query</th>
                        <th className="py-2.5 px-3">Expected Tripartite State</th>
                        <th className="py-2.5 px-3">Model Output State</th>
                        <th className="py-2.5 px-3">Latency</th>
                        <th className="py-2.5 px-3 text-right">Result</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                      {evalResults.results.map((r: any) => (
                        <tr key={r.eval_id} className="hover:bg-[#1C2541]/80 transition">
                          <td className="py-2.5 px-3 text-cyan-400 font-bold">{r.eval_id}</td>
                          <td className="py-2.5 px-3 font-sans text-slate-200 max-w-sm truncate">{r.query}</td>
                          <td className="py-2.5 px-3 text-amber-300 font-semibold">{r.expected_status}</td>
                          <td className="py-2.5 px-3 font-semibold">
                            <span className={r.actual_status === 'VERIFIED' ? 'text-emerald-400' : r.actual_status === 'CANNOT_GENERATE' ? 'text-rose-400' : 'text-amber-300'}>
                              {r.actual_status}
                            </span>
                          </td>
                          <td className="py-2.5 px-3 text-slate-400">{r.latency_ms}ms</td>
                          <td className="py-2.5 px-3 text-right">
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              r.is_pass ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-300'
                            }`}>
                              {r.is_pass ? 'PASSED (100%)' : 'MISMATCH'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>

          {/* Platform Trust Policies & Thresholds */}
          <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-4 text-xs">
            <h2 className="text-sm font-bold text-white flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Government Trust Policies & Algorithmic Guardrails</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-slate-300">Primary Gazette Authority Enforcement:</span>
                  <span className="text-emerald-400 font-bold font-mono">STRICT (ZONE 1)</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-300">Grounding Abstention Threshold:</span>
                  <span className="text-cyan-400 font-bold font-mono">0.85 (High Precision)</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-300">Quarantine Execution Shield:</span>
                  <span className="text-emerald-400 font-bold font-mono">ACTIVE</span>
                </div>
              </div>

              <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-slate-300">Zero-Creativity Temperature:</span>
                  <span className="text-slate-300 font-mono font-bold">0.0 (Strict Grounding)</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-300">Cryptographic Chain-of-Custody:</span>
                  <span className="text-emerald-400 font-bold font-mono">SHA-256 HMAC</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-300">In-Context Few-Shot Conditioning:</span>
                  <span className="text-cyan-400 font-bold font-mono">ENABLED</span>
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
