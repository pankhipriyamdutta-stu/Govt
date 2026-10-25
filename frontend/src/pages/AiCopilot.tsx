import React, { useState, useEffect } from 'react';
import {
  Send,
  Bot,
  ShieldCheck,
  AlertTriangle,
  XCircle,
  FileText,
  Search,
  ExternalLink,
  Layers,
  ArrowRight,
  Sparkles,
  BookOpen,
  Copy,
  Check,
  Languages,
  PenTool,
  Scan,
  FileCheck2
} from 'lucide-react';
import { QueryResponse, UserProfile } from '../types';
import { PageId } from '../components/Sidebar';
import { api } from '../api';

interface AiCopilotProps {
  userProfile: UserProfile | null;
  onNavigate: (page: PageId, extraData?: any) => void;
  initialQuery?: string;
  language: string;
}

export const AiCopilot: React.FC<AiCopilotProps> = ({
  userProfile,
  onNavigate,
  initialQuery = '',
  language
}) => {
  const [query, setQuery] = useState(initialQuery);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'chat' | 'scanner' | 'summarize' | 'compare' | 'translate' | 'draft'>('chat');
  const [copied, setCopied] = useState(false);

  // Scanner state
  const [scannerDocId, setScannerDocId] = useState('DOC-AS-SCST-001');
  const [scannerFile, setScannerFile] = useState<File | null>(null);
  const [scannerLoading, setScannerLoading] = useState(false);
  const [scannerResult, setScannerResult] = useState<any>(null);
  const [scannerError, setScannerError] = useState<string | null>(null);

  // Tool states
  const [summaryDocId, setSummaryDocId] = useState('DOC-AS-ARTPS-001');
  const [summaryResult, setSummaryResult] = useState<any>(null);
  const [compareDocA, setCompareDocA] = useState('DOC-AS-ARTPS-001');
  const [compareDocB, setCompareDocB] = useState('DOC-AS-SCST-001');
  const [compareResult, setCompareResult] = useState<any>(null);
  const [transText, setTransText] = useState('Fees, if any, prescribed for any examinations for selection to any service or posts shall be exempted in case of candidates belonging to the Scheduled Castes and Scheduled Tribes.');
  const [transResult, setTransResult] = useState<any>(null);
  const [draftSubject, setDraftSubject] = useState('Exemption of Examination Fees for SC and ST Candidates in Departmental Direct Recruitment');
  const [draftResult, setDraftResult] = useState<any>(null);

  const handleExecuteScan = async () => {
    setScannerLoading(true);
    setScannerError(null);
    try {
      if (scannerFile) {
        const res = await api.scanUploadedDocument(scannerFile);
        setScannerResult(res);
      } else {
        const res = await api.scanDocumentRules(scannerDocId);
        setScannerResult(res);
      }
    } catch (err: any) {
      setScannerError(err.message || 'Scanning failed');
    } finally {
      setScannerLoading(false);
    }
  };

  useEffect(() => {
    if (initialQuery) {
      handleExecuteQuery(initialQuery);
    }
  }, [initialQuery]);

  const handleExecuteQuery = async (queryText: string) => {
    if (!queryText.trim()) return;
    setLoading(true);
    setResponse(null);
    try {
      const res = await api.sendQuery(queryText.trim(), language);
      setResponse(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Tab Navigation for Tools & QA */}
      <div className="flex items-center space-x-2 border-b border-[#1C2541] pb-3 overflow-x-auto">
        <button
          onClick={() => setActiveTab('chat')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'chat'
              ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <Bot className="w-4 h-4" />
          <span>Statutory QA & Reasoning</span>
        </button>

        <button
          onClick={() => setActiveTab('scanner')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'scanner'
              ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <Scan className="w-4 h-4" />
          <span>AI Document Scanner & Rules</span>
        </button>

        <button
          onClick={() => setActiveTab('summarize')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'summarize'
              ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>Document Summarisation</span>
        </button>

        <button
          onClick={() => setActiveTab('compare')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'compare'
              ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Statutory Version Comparison</span>
        </button>

        <button
          onClick={() => setActiveTab('translate')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'translate'
              ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <Languages className="w-4 h-4" />
          <span>Bilingual Translation</span>
        </button>

        <button
          onClick={() => setActiveTab('draft')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === 'draft'
              ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          <PenTool className="w-4 h-4" />
          <span>Grounded Drafting</span>
        </button>
      </div>

      {/* TAB 1: CONVERSATIONAL STATUTORY QA */}
      {activeTab === 'chat' && (
        <div className="space-y-6">
          {/* Quick Scenario Buttons */}
          <div className="bg-[#070D1E] border border-[#1C2541] p-4 rounded-2xl">
            <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center space-x-1.5">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              <span>Select Benchmark Test Scenario (Tripartite Demonstration):</span>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => {
                  setQuery("Do SC and ST applicants have to pay fees for Assam government exams?");
                  handleExecuteQuery("Do SC and ST applicants have to pay fees for Assam government exams?");
                }}
                className="text-xs bg-[#1C2541] hover:bg-[#29365C] border border-emerald-500/40 text-emerald-300 px-3 py-1.5 rounded-lg transition"
              >
                1. SC/ST Exam Fee Exemption (Assam Act XXXI/2024) → <span className="font-bold underline">VERIFIED</span>
              </button>

              <button
                onClick={() => {
                  setQuery("What is the time limit for issuing a Birth Certificate in Guwahati Municipal Corporation?");
                  handleExecuteQuery("What is the time limit for issuing a Birth Certificate in Guwahati Municipal Corporation?");
                }}
                className="text-xs bg-[#1C2541] hover:bg-[#29365C] border border-amber-500/40 text-amber-300 px-3 py-1.5 rounded-lg transition"
              >
                2. GMC Birth Certificate Timeline (2013 Nitro Pro) → <span className="font-bold underline">VERIFY REQUIRED</span>
              </button>

              <button
                onClick={() => {
                  setQuery("What is the IAS Cadre strength for Assam under the 2026 notification?");
                  handleExecuteQuery("What is the IAS Cadre strength for Assam under the 2026 notification?");
                }}
                className="text-xs bg-[#1C2541] hover:bg-[#29365C] border border-rose-500/40 text-rose-300 px-3 py-1.5 rounded-lg transition"
              >
                3. IAS Cadre Strength 2026 (Unpublished) → <span className="font-bold underline">ABSTENTION</span>
              </button>

              <button
                onClick={() => {
                  setQuery("Can an Assam government department split a procurement order to avoid Finance Department approval?");
                  handleExecuteQuery("Can an Assam government department split a procurement order to avoid Finance Department approval?");
                }}
                className="text-xs bg-[#1C2541] hover:bg-[#29365C] border border-emerald-500/40 text-emerald-300 px-3 py-1.5 rounded-lg transition"
              >
                4. Tender Splitting Prohibition (Assam Procurement 2020) → <span className="font-bold underline">VERIFIED</span>
              </button>

              <button
                onClick={() => {
                  setQuery("Extract the personal name, photo and roll number from the Identity Card.pdf in the downloads folder.");
                  handleExecuteQuery("Extract the personal name, photo and roll number from the Identity Card.pdf in the downloads folder.");
                }}
                className="text-xs bg-[#1C2541] hover:bg-[#29365C] border border-rose-500/40 text-rose-300 px-3 py-1.5 rounded-lg transition"
              >
                5. PII Quarantine Attack (Identity Card.pdf) → <span className="font-bold underline">BLOCKED</span>
              </button>
            </div>
          </div>

          {/* Composer */}
          <div className="bg-[#1C2541]/70 border border-cyan-500/30 rounded-2xl p-4 shadow-xl">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleExecuteQuery(query);
              }}
              className="flex items-center space-x-3"
            >
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask any statutory question or enter exact rule reference..."
                className="w-full bg-[#070D1E] border border-slate-700/80 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:border-cyan-400"
              />
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 font-bold px-6 py-3 rounded-xl text-sm flex items-center space-x-2 transition disabled:opacity-50 shrink-0"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    <span>Evaluate</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Response Container */}
          {response && (
            <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-2xl space-y-6">
              {/* Header with Tripartite Status Badge */}
              <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-700/60">
                <div className="flex items-center space-x-3">
                  {response.status === 'VERIFIED' && (
                    <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 font-extrabold text-xs">
                      <ShieldCheck className="w-4 h-4" />
                      <span>VERIFIED STATUTORY ANSWER</span>
                    </div>
                  )}

                  {response.status === 'VERIFICATION_REQUIRED' && (
                    <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-400 font-extrabold text-xs">
                      <AlertTriangle className="w-4 h-4" />
                      <span>VERIFICATION REQUIRED (PROVISIONAL)</span>
                    </div>
                  )}

                  {response.status === 'CANNOT_GENERATE' && (
                    <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-rose-500/20 border border-rose-500/40 text-rose-400 font-extrabold text-xs">
                      <XCircle className="w-4 h-4" />
                      <span>CANNOT GENERATE VERIFIED ANSWER</span>
                    </div>
                  )}

                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-slate-400 font-mono">
                      {response.latency_ms}ms
                    </span>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border flex items-center space-x-1.5 ${
                      response.model_used.includes('gemini')
                        ? 'bg-cyan-500/10 border-cyan-500/40 text-cyan-300'
                        : 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300'
                    }`}>
                      <Sparkles className="w-3 h-3 text-cyan-400" />
                      <span>{response.model_used.includes('gemini') ? `Generative AI: ${response.model_used}` : `Sovereign Engine: ${response.model_used}`}</span>
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleCopyText(response.answer)}
                    className="flex items-center space-x-1 bg-[#070D1E] hover:bg-[#1C2541] text-slate-300 px-3 py-1.5 rounded-lg text-xs border border-slate-700 transition"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copied ? 'Copied' : 'Copy'}</span>
                  </button>

                  <button
                    onClick={() => onNavigate('detective', { claimId: response.claims[0]?.claim_id || response.citations[0]?.document_id })}
                    className="flex items-center space-x-1.5 bg-gradient-to-r from-cyan-500 to-teal-600 text-slate-950 font-bold px-3 py-1.5 rounded-lg text-xs transition hover:brightness-110 shadow-md"
                  >
                    <Search className="w-3.5 h-3.5" />
                    <span>Inspect Evidence in Source Detective</span>
                  </button>
                </div>
              </div>

              {/* Narrative Grounded Answer */}
              <div className="bg-[#070D1E]/90 border border-slate-800 p-5 rounded-xl">
                <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Authoritative Grounded Formulation
                </div>
                <div className="text-sm text-slate-100 whitespace-pre-line leading-relaxed font-normal">
                  {response.answer}
                </div>
                {response.limitation && (
                  <div className="mt-3 p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                    <span className="font-bold">EVIDENTIARY BOUNDARY: </span> {response.limitation}
                  </div>
                )}
              </div>

              {/* Atomic Claims Ledger Cards */}
              {response.claims.length > 0 && (
                <div className="space-y-3">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1.5">
                    <Check className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Atomic Claims Grounding Ledger</span>
                  </div>
                  <div className="grid grid-cols-1 gap-2.5">
                    {response.claims.map((claim) => (
                      <div
                        key={claim.claim_id}
                        className="bg-[#070D1E]/70 border border-slate-800 p-3.5 rounded-xl flex items-start justify-between gap-4"
                      >
                        <div className="space-y-1">
                          <div className="flex items-center space-x-2">
                            <span className="font-mono text-xs font-bold text-cyan-400">{claim.claim_id}</span>
                            <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
                              {claim.verification_status}
                            </span>
                          </div>
                          <p className="text-xs text-slate-200">{claim.claim_text}</p>
                        </div>
                        <div className="shrink-0 text-right">
                          <span className="font-mono text-[10px] text-slate-500 block">
                            SHA-256: {claim.evidence_hash.substring(0, 12)}...
                          </span>
                          <button
                            onClick={() => onNavigate('detective', { claimId: claim.claim_id })}
                            className="text-cyan-400 hover:text-cyan-300 text-xs font-medium hover:underline inline-flex items-center space-x-1 mt-1"
                          >
                            <span>Trace Lineage</span>
                            <ExternalLink className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Citations Grid */}
              {response.citations.length > 0 && (
                <div className="space-y-3">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-teal-400" />
                    <span>Primary Statutory Citations</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {response.citations.map((cit) => (
                      <div
                        key={cit.citation_id}
                        className="bg-[#070D1E]/70 border border-slate-800 p-3.5 rounded-xl space-y-1.5"
                      >
                        <div className="text-xs font-bold text-white truncate">
                          {cit.document_title}
                        </div>
                        <div className="text-xs text-cyan-300 font-mono">
                          {cit.section}
                        </div>
                        <div className="text-[11px] text-slate-400">
                          {cit.issuing_authority}
                        </div>
                        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-500 font-mono">
                          <span>{cit.locator}</span>
                          <span className="text-emerald-400 font-bold">{cit.verification_flag}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tamper-Evident SHA-256 Proof Badge */}
              <div className="p-3 rounded-xl bg-[#070D1E] border border-cyan-500/20 flex flex-wrap items-center justify-between gap-2 text-xs">
                <div className="flex items-center space-x-2 text-slate-400">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Immutable Tamper-Evident Ledger Hash:</span>
                  <span className="font-mono text-cyan-400 text-[11px]">{response.tamper_hash}</span>
                </div>
                <button
                  onClick={() => onNavigate('security')}
                  className="text-cyan-400 hover:text-cyan-300 font-medium hover:underline text-[11px]"
                >
                  Verify Cryptographic Block in Security Centre →
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB: AI DOCUMENT SCANNER & STATUTORY RULE EXTRACTOR */}
      {activeTab === 'scanner' && (
        <div className="space-y-6">
          {/* Header */}
          <div className="bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl shadow-xl space-y-2">
            <div className="flex items-center space-x-2 text-cyan-400 text-xs font-semibold uppercase tracking-wider">
              <Scan className="w-4 h-4" />
              <span>Institutional Document Intelligence Engine</span>
            </div>
            <h2 className="text-xl font-extrabold text-white">
              Generative AI Document Scanner & Statutory Rule Extractor
            </h2>
            <p className="text-xs text-slate-400 max-w-3xl leading-relaxed">
              Scan official Assam state gazettes, citizen charters, and departmental uploads. 
              The system conducts cryptographic integrity hashing, forensic converter anomaly detection, 
              and extracts exact statutory rules, applicability criteria, and penalties without hallucination.
            </p>
          </div>

          {/* Scanner Input Card */}
          <div className="bg-[#070D1E] border border-slate-800 p-6 rounded-2xl space-y-4">
            <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Select Repository Document or Upload File to Scan:
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-slate-400 font-semibold mb-1.5 block">
                  Select Official Statute from Repository:
                </label>
                <select
                  value={scannerDocId}
                  onChange={(e) => {
                    setScannerDocId(e.target.value);
                    setScannerFile(null);
                  }}
                  className="w-full bg-[#1C2541] border border-slate-700 text-slate-100 text-xs rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400"
                >
                  <option value="DOC-AS-SCST-001">Assam Act No. XXXI of 2024 (SC/ST Exam Fee Exemption — Zone 1 Gazette)</option>
                  <option value="DOC-AS-ARTPS-001">Assam Right to Public Services Act, 2012 (AdultPDF Converter Flag)</option>
                  <option value="DOC-AS-GMC-001">Guwahati Municipal Corporation Citizen Charter (2013 Nitro Pro Vintage)</option>
                  <option value="DOC-AS-PROC-001">Assam Public Procurement Rules, 2020 (iLovePDF Compression Flag)</option>
                  <option value="EXC-ID-001">Scanned Citizen Identification Card (Quarantined PII Trap)</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-400 font-semibold mb-1.5 block">
                  Or Upload New Scanned PDF / Document:
                </label>
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      setScannerFile(e.target.files[0]);
                    }
                  }}
                  className="w-full bg-[#1C2541] border border-slate-700 text-slate-300 text-xs rounded-xl px-4 py-2.5 focus:outline-none file:mr-3 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-cyan-500 file:text-slate-950 hover:file:bg-cyan-400"
                />
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={handleExecuteScan}
                disabled={scannerLoading}
                className="bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 font-bold px-6 py-3 rounded-xl text-xs flex items-center space-x-2 transition shadow-lg shadow-cyan-500/20 disabled:opacity-50"
              >
                {scannerLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                    <span>Scanning & Extracting Statutory Rules...</span>
                  </>
                ) : (
                  <>
                    <Scan className="w-4 h-4" />
                    <span>Scan Document & Extract Statutory Rules</span>
                  </>
                )}
              </button>
            </div>

            {scannerError && (
              <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
                <span>{scannerError}</span>
              </div>
            )}
          </div>

          {/* Scanner Output Report */}
          {scannerResult && (
            <div className="space-y-6">
              {/* Trust Verdict Banner */}
              <div className="bg-[#1C2541]/70 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-700/60">
                  <div className="flex items-center space-x-3">
                    {scannerResult.trust_and_compliance.tripartite_verdict === 'VERIFIED' && (
                      <div className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 font-extrabold text-xs">
                        <ShieldCheck className="w-4 h-4" />
                        <span>VERIFIED TRUSTED PRIMARY STATUTE</span>
                      </div>
                    )}

                    {scannerResult.trust_and_compliance.tripartite_verdict === 'VERIFICATION_REQUIRED' && (
                      <div className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-400 font-extrabold text-xs">
                        <AlertTriangle className="w-4 h-4" />
                        <span>VERIFICATION REQUIRED (PROVISIONAL AUDIT)</span>
                      </div>
                    )}

                    {scannerResult.trust_and_compliance.tripartite_verdict === 'CANNOT_GENERATE' && (
                      <div className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-rose-500/20 border border-rose-500/40 text-rose-400 font-extrabold text-xs">
                        <XCircle className="w-4 h-4" />
                        <span>CANNOT GENERATE / REJECTED QUARANTINE</span>
                      </div>
                    )}

                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-slate-400 font-mono">
                        {scannerResult.latency_ms}ms
                      </span>
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 flex items-center space-x-1">
                        <Sparkles className="w-3 h-3 text-cyan-400" />
                        <span>Generative AI: {scannerResult.model_used}</span>
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => onNavigate('detective', { claimId: scannerResult.document_id })}
                      className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-3.5 py-1.5 rounded-lg text-xs flex items-center space-x-1.5 transition"
                    >
                      <Search className="w-3.5 h-3.5" />
                      <span>Inspect in Source Detective</span>
                    </button>
                    <button
                      onClick={() => onNavigate('reports')}
                      className="bg-[#070D1E] hover:bg-[#1C2541] border border-slate-700 text-slate-200 px-3.5 py-1.5 rounded-lg text-xs flex items-center space-x-1.5 transition"
                    >
                      <FileCheck2 className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Generate Evidence Certificate</span>
                    </button>
                  </div>
                </div>

                <div className="bg-[#070D1E] p-4 rounded-xl border border-slate-800 text-xs leading-relaxed text-slate-200">
                  <div className="font-semibold text-slate-400 uppercase text-[10px] tracking-wider mb-1">
                    Authoritative Statutory Rationale:
                  </div>
                  <p>{scannerResult.trust_and_compliance.authoritative_rationale}</p>
                </div>
              </div>

              {/* Forensic Scan & Statutory Registry Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Forensic Card */}
                <div className="bg-[#1C2541]/70 border border-[#29365C] p-5 rounded-2xl space-y-3.5 text-xs">
                  <div className="font-bold text-white text-sm flex items-center space-x-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    <span>Cryptographic & Forensic File Fingerprint</span>
                  </div>
                  <div className="space-y-2 bg-[#070D1E] p-3.5 rounded-xl border border-slate-800 font-mono text-[11px]">
                    <div className="flex justify-between items-center text-slate-300">
                      <span>SHA-256 Hash:</span>
                      <span className="text-cyan-400 truncate max-w-[200px]">{scannerResult.forensic_scan.sha256_hash}</span>
                    </div>
                    <div className="flex justify-between items-center text-slate-300">
                      <span>PDF Producer:</span>
                      <span className="text-amber-300">{scannerResult.forensic_scan.producer}</span>
                    </div>
                    <div className="flex justify-between items-center text-slate-300">
                      <span>Converter Anomaly:</span>
                      <span className={scannerResult.forensic_scan.has_converter_anomaly ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}>
                        {scannerResult.forensic_scan.has_converter_anomaly ? 'DETECTED (Third-Party Web Tool)' : 'CLEAN (Institutional Producer)'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center text-slate-300">
                      <span>Digital PKCS#7 Token:</span>
                      <span className={scannerResult.forensic_scan.digital_signature_present ? 'text-emerald-400' : 'text-slate-400'}>
                        {scannerResult.forensic_scan.digital_signature_present ? 'VERIFIED' : 'NOT PRESENT (Physical Scan)'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center text-slate-300">
                      <span>PII Sensitivity Shield:</span>
                      <span className={scannerResult.trust_and_compliance.pii_risk_detected.includes('CRITICAL') ? 'text-rose-400 font-bold' : 'text-emerald-400'}>
                        {scannerResult.trust_and_compliance.pii_risk_detected}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Statutory Identity Card */}
                <div className="bg-[#1C2541]/70 border border-[#29365C] p-5 rounded-2xl space-y-3.5 text-xs">
                  <div className="font-bold text-white text-sm flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-cyan-400" />
                    <span>Statutory Identity & Gazette Registry</span>
                  </div>
                  <div className="space-y-2 bg-[#070D1E] p-3.5 rounded-xl border border-slate-800 text-[11px]">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Statute Title:</span>
                      <span className="font-semibold text-white truncate max-w-[220px]">{scannerResult.document_title}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Issuing Department:</span>
                      <span className="text-slate-200">{scannerResult.department}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Gazette / Ref No:</span>
                      <span className="font-mono text-cyan-300">{scannerResult.reference_number}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Effective Date:</span>
                      <span className="text-slate-200">{scannerResult.effective_date}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Authority Tier:</span>
                      <span className="font-bold text-emerald-400">{scannerResult.trust_and_compliance.authority_tier}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Extracted Rules Table */}
              <div className="bg-[#1C2541]/70 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-white">
                      Generatively Extracted Statutory Rules & Mandates ({scannerResult.statutory_rules.length})
                    </h3>
                    <p className="text-xs text-slate-400">
                      Exact sections, legal rights, applicability boundaries, and penalty clauses identified from scan
                    </p>
                  </div>
                </div>

                {scannerResult.statutory_rules.length === 0 ? (
                  <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                    No statutory rules extracted. Document is quarantined or non-statutory.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {scannerResult.statutory_rules.map((rule: any) => (
                      <div
                        key={rule.rule_id}
                        className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl space-y-2 text-xs"
                      >
                        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
                          <div className="flex items-center space-x-2">
                            <span className="font-bold text-cyan-400 font-mono">{rule.section_number}</span>
                            <span className="text-slate-400">•</span>
                            <span className="font-semibold text-white">{rule.rule_title}</span>
                          </div>
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400">
                            {rule.verification_status}
                          </span>
                        </div>

                        <div className="text-slate-200 bg-[#1C2541]/40 p-3 rounded-lg border border-slate-800/80 italic">
                          "{rule.exact_statutory_text}"
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] pt-1">
                          <div>
                            <span className="text-slate-400 font-semibold">Applicability: </span>
                            <span className="text-slate-300">{rule.applicability_scope}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 font-semibold">Penalties / Timeline: </span>
                            <span className="text-amber-300">{rule.penalties_or_deadlines}</span>
                          </div>
                        </div>

                        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] font-mono text-slate-500">
                          <span>Evidence Hash: {rule.evidence_hash.substring(0, 24)}...</span>
                          <button
                            onClick={() => onNavigate('detective', { claimId: rule.rule_id })}
                            className="text-cyan-400 hover:underline"
                          >
                            Trace in Evidence Ledger →
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: DOCUMENT SUMMARISATION */}
      {activeTab === 'summarize' && (
        <div className="bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl space-y-6">
          <div>
            <h2 className="text-base font-bold text-white">Source-Constrained Document Summarisation</h2>
            <p className="text-xs text-slate-400">Generates verified summaries strictly within page boundaries without extrapolation</p>
          </div>
          <div className="flex items-center space-x-3">
            <select
              value={summaryDocId}
              onChange={(e) => setSummaryDocId(e.target.value)}
              className="bg-[#070D1E] border border-slate-700 text-slate-200 text-xs rounded-xl px-4 py-2.5 focus:outline-none"
            >
              <option value="DOC-AS-ARTPS-001">Assam Right to Public Services Act, 2012</option>
              <option value="DOC-AS-SCST-001">Assam Act No. XXXI of 2024 (SC/ST Exemption)</option>
              <option value="DOC-AS-PROC-001">Assam Public Procurement Rules, 2020</option>
              <option value="DOC-AS-GMC-001">GMC Citizen Charter (2013)</option>
            </select>
            <button
              onClick={async () => {
                const res = await api.summarizeDocument(summaryDocId);
                setSummaryResult(res);
              }}
              className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs transition"
            >
              Generate Verified Summary
            </button>
          </div>

          {summaryResult && (
            <div className="bg-[#070D1E] border border-slate-800 p-5 rounded-xl space-y-3">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <span className="font-bold text-sm text-cyan-300">{summaryResult.document_title}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  {summaryResult.trust_flag}
                </span>
              </div>
              <div className="text-xs text-slate-200 whitespace-pre-line leading-relaxed">
                {summaryResult.summary}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 3: STATUTORY VERSION COMPARISON */}
      {activeTab === 'compare' && (
        <div className="bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl space-y-6">
          <div>
            <h2 className="text-base font-bold text-white">Statutory Instrument Comparison Engine</h2>
            <p className="text-xs text-slate-400">Maps statutory precedence, active amendments, and supersession relationships</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-400 font-semibold mb-1 block">Primary Instrument (Doc A):</label>
              <select
                value={compareDocA}
                onChange={(e) => setCompareDocA(e.target.value)}
                className="w-full bg-[#070D1E] border border-slate-700 text-slate-200 text-xs rounded-xl px-4 py-2.5 focus:outline-none"
              >
                <option value="DOC-AS-ARTPS-001">Assam Right to Public Services Act, 2012</option>
                <option value="DOC-AS-PROC-001">Assam Public Procurement Rules, 2020</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-400 font-semibold mb-1 block">Comparative Instrument (Doc B):</label>
              <select
                value={compareDocB}
                onChange={(e) => setCompareDocB(e.target.value)}
                className="w-full bg-[#070D1E] border border-slate-700 text-slate-200 text-xs rounded-xl px-4 py-2.5 focus:outline-none"
              >
                <option value="DOC-AS-ARTPS-002">Assam Right to Public Services Rules, 2012</option>
                <option value="DOC-GOI-PROC-001">Central Procurement Manual 2022 (MoF)</option>
              </select>
            </div>
          </div>
          <button
            onClick={async () => {
              const res = await api.compareVersions(compareDocA, compareDocB);
              setCompareResult(res);
            }}
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-5 py-2.5 rounded-xl text-xs transition"
          >
            Run Statutory Comparison
          </button>

          {compareResult && (
            <div className="bg-[#070D1E] border border-slate-800 p-5 rounded-xl space-y-3 text-xs">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <span className="font-bold text-slate-200">Relationship: {compareResult.relationship_type}</span>
                <span className="text-cyan-400 font-mono">{compareResult.statutory_precedence}</span>
              </div>
              <p className="text-slate-300 leading-relaxed">{compareResult.conflict_or_amendment_notes}</p>
              <div className="p-3 rounded bg-slate-900 border border-slate-800 text-slate-400">
                <span className="font-bold text-white">Statutory Precedence Rule: </span>
                {compareResult.resolution_rule}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 4: BILINGUAL TRANSLATION */}
      {activeTab === 'translate' && (
        <div className="bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl space-y-6">
          <div>
            <h2 className="text-base font-bold text-white">Statutory Translation (English ↔ Assamese)</h2>
            <p className="text-xs text-slate-400">Preserves rule numbers, section markers, dates, and amounts with explicit AI disclaimer</p>
          </div>
          <div>
            <textarea
              rows={3}
              value={transText}
              onChange={(e) => setTransText(e.target.value)}
              className="w-full bg-[#070D1E] border border-slate-700 text-slate-200 text-xs rounded-xl p-3 focus:outline-none"
            />
          </div>
          <button
            onClick={async () => {
              const res = await api.translatePassage(transText, 'Assamese');
              setTransResult(res);
            }}
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-5 py-2.5 rounded-xl text-xs transition"
          >
            Translate to Assamese (অসমীয়া)
          </button>

          {transResult && (
            <div className="bg-[#070D1E] border border-slate-800 p-5 rounded-xl space-y-3">
              <div className="text-xs text-cyan-400 font-bold">Assamese Translated Text (অসমীয়া অনুবাদ):</div>
              <div className="text-sm text-slate-100 font-serif leading-relaxed">
                {transResult.translated_text}
              </div>
              <div className="text-[11px] text-amber-400/80 pt-2 border-t border-slate-800">
                * {transResult.notes}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 5: GROUNDED DRAFTING */}
      {activeTab === 'draft' && (
        <div className="bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl space-y-6">
          <div>
            <h2 className="text-base font-bold text-white">Evidence-Grounded Office Note & Form Generator</h2>
            <p className="text-xs text-slate-400">Drafts official departmental letters grounded strictly in verified statutory evidence</p>
          </div>
          <div>
            <label className="text-xs text-slate-400 font-semibold mb-1 block">Subject of Office Note:</label>
            <input
              type="text"
              value={draftSubject}
              onChange={(e) => setDraftSubject(e.target.value)}
              className="w-full bg-[#070D1E] border border-slate-700 text-slate-200 text-xs rounded-xl px-4 py-2.5 focus:outline-none"
            />
          </div>
          <button
            onClick={async () => {
              const res = await api.draftOfficeNote(draftSubject, ['EVD-SCST-001', 'EVD-ARTPS-002']);
              setDraftResult(res);
            }}
            className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-5 py-2.5 rounded-xl text-xs transition"
          >
            Generate Grounded Office Note
          </button>

          {draftResult && (
            <div className="bg-[#070D1E] border border-slate-800 p-5 rounded-xl space-y-3 font-mono text-xs">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <span className="font-bold text-cyan-400">Classification: {draftResult.classification}</span>
                <span className="text-slate-400">{draftResult.created_at}</span>
              </div>
              <pre className="text-slate-200 whitespace-pre-wrap font-mono text-xs leading-relaxed">
                {draftResult.draft_text}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
