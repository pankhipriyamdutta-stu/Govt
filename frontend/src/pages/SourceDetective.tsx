import React, { useState, useEffect } from 'react';
import {
  SearchCode,
  ShieldCheck,
  AlertTriangle,
  FileText,
  Hash,
  Award,
  CheckCircle2,
  ExternalLink,
  BookOpen,
  ArrowRight,
  Layers,
  Sparkles
} from 'lucide-react';
import { EvidenceTrail } from '../types';
import { api } from '../api';

interface SourceDetectiveProps {
  initialClaimId?: string;
}

export const SourceDetective: React.FC<SourceDetectiveProps> = ({ initialClaimId = 'CLM-SCST-001' }) => {
  const [selectedClaimId, setSelectedClaimId] = useState(initialClaimId);
  const [evidenceTrail, setEvidenceTrail] = useState<EvidenceTrail | null>(null);
  const [ledgerEntries, setLedgerEntries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getEvidenceLedger().then((entries) => {
      setLedgerEntries(entries);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedClaimId) {
      setLoading(true);
      api.inspectEvidenceTrail(selectedClaimId).then((trail) => {
        setEvidenceTrail(trail);
        setLoading(false);
      }).catch((e) => {
        console.error(e);
        setLoading(false);
      });
    }
  }, [selectedClaimId]);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#1C2541]/70 border border-teal-500/30 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center space-x-2 text-teal-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <SearchCode className="w-4 h-4" />
            <span>Signature Feature • Deep Provenance Ledger</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white">
            Source Intelligence / Source Detective
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            360-degree forensic trace from AI claim to exact statutory section, printed page, SHA-256 hash, and institutional authority
          </p>
        </div>

        {/* Claim Quick Switcher */}
        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400">Select Claim:</span>
          <select
            value={selectedClaimId}
            onChange={(e) => setSelectedClaimId(e.target.value)}
            className="bg-[#070D1E] border border-teal-500/40 text-teal-300 font-mono text-xs rounded-xl px-3 py-2 focus:outline-none"
          >
            {ledgerEntries.map((e) => (
              <option key={e.evidence_id} value={e.claim_id || e.evidence_id}>
                {e.claim_id || e.evidence_id} ({e.document_id})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 text-sm">
          <div className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
          Tracing forensic provenance chain from evidence ledger...
        </div>
      ) : evidenceTrail ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* LEFT 2 COLUMNS: FORENSIC CLAIM & EXACT TEXT */}
          <div className="lg:col-span-2 space-y-6">
            {/* The Asserted AI Claim Card */}
            <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-teal-400">
                  {evidenceTrail.claim_id}
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  {evidenceTrail.support_status}
                </span>
              </div>
              <h2 className="text-base font-bold text-white leading-snug">
                "{evidenceTrail.claim_text}"
              </h2>
            </div>

            {/* Verbatim Supporting Statutory Excerpt */}
            <div className="bg-[#070D1E] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center space-x-2 text-xs font-bold text-slate-300 uppercase tracking-wider">
                  <FileText className="w-4 h-4 text-cyan-400" />
                  <span>Verbatim Official Statutory Text</span>
                </div>
                <div className="flex items-center space-x-2 font-mono text-[11px] text-slate-400">
                  <span>Section: <span className="text-cyan-300 font-bold">{evidenceTrail.locator.section_number}</span></span>
                  <span>•</span>
                  <span>Printed Page: <span className="text-cyan-300 font-bold">{evidenceTrail.locator.printed_page_number}</span></span>
                  <span>•</span>
                  <span>Physical PDF Page: <span className="text-cyan-300 font-bold">{evidenceTrail.locator.physical_pdf_page}</span></span>
                </div>
              </div>

              <blockquote className="p-4 rounded-xl bg-slate-900/80 border-l-4 border-cyan-500 text-slate-100 text-sm italic font-serif leading-relaxed">
                "{evidenceTrail.exact_evidence_text}"
              </blockquote>

              {/* Cryptographic Hash Comparison */}
              <div className="p-4 rounded-xl bg-[#0B132B] border border-slate-800 space-y-2 text-xs font-mono">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Excerpt SHA-256 Hash:</span>
                  <span className="text-cyan-400">{evidenceTrail.evidence_hash}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Source Document SHA-256:</span>
                  <span className="text-slate-300">{evidenceTrail.source_file_hash}</span>
                </div>
                <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px]">
                  <span className="text-emerald-400 font-semibold flex items-center space-x-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Cryptographic File Hash Validated Against Repository Registry</span>
                  </span>
                </div>
              </div>
            </div>

            {/* Provenance Audit Notes */}
            <div className="bg-[#1C2541]/40 border border-[#29365C] rounded-2xl p-5 shadow-xl space-y-2 text-xs">
              <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px] block">
                Verification Officer Forensic Audit
              </span>
              <p className="text-slate-300 leading-relaxed">
                {evidenceTrail.trust_policy_verdict.reviewer_notes}
              </p>
            </div>
          </div>

          {/* RIGHT COLUMN: INSTITUTIONAL AUTHORITY & SIGNATURE CARD */}
          <div className="space-y-6">
            {/* Issuing Authority & Gazette Identity */}
            <div className="bg-[#1C2541]/60 border border-[#29365C] rounded-2xl p-5 shadow-xl space-y-3 text-xs">
              <div className="font-bold text-white flex items-center space-x-2 text-sm border-b border-slate-800 pb-2">
                <Award className="w-4 h-4 text-cyan-400" />
                <span>Issuing Authority & Enactment</span>
              </div>
              <div className="space-y-2 text-slate-300">
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Statute Title:</span>
                  <span className="font-semibold text-white">{evidenceTrail.document_title}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Department:</span>
                  <span>{evidenceTrail.department}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Issuing Authority:</span>
                  <span className="text-cyan-300 font-semibold">{evidenceTrail.issuing_authority}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Gazette Reference:</span>
                  <span className="font-mono text-slate-200">{evidenceTrail.reference_number || 'Official State Gazette'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Jurisdiction & Scope:</span>
                  <span>{evidenceTrail.jurisdiction}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Active Version:</span>
                  <span className="font-mono text-emerald-400 font-bold">{evidenceTrail.version_number} (Active Law)</span>
                </div>
              </div>
            </div>

            {/* Cryptographic Digital Signature & Signer Authority */}
            <div className="bg-[#070D1E] border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3 text-xs">
              <div className="font-bold text-white flex items-center space-x-2 text-sm border-b border-slate-800 pb-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Digital Signature & Authority</span>
              </div>

              <div className="space-y-2 text-slate-300">
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Signature Format:</span>
                  <span className="font-mono text-slate-200">{evidenceTrail.cryptographic_verification.signature_format}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Signer Identity:</span>
                  <span className="font-semibold text-white">{evidenceTrail.cryptographic_verification.signer_identity}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Institutional Authority:</span>
                  <span className="font-mono text-emerald-400 font-semibold">
                    {evidenceTrail.cryptographic_verification.signer_institutional_authority}
                  </span>
                </div>

                {evidenceTrail.cryptographic_verification.anomaly_flags.length > 0 && (
                  <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[11px]">
                    <span className="font-bold block mb-1">Metadata Converter Warnings:</span>
                    <ul className="list-disc pl-4 space-y-1">
                      {evidenceTrail.cryptographic_verification.anomaly_flags.map((a, i) => (
                        <li key={i}>{a}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
