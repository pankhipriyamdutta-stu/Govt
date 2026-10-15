import React, { useState } from 'react';
import {
  FileSpreadsheet,
  Download,
  Printer,
  FileCheck2,
  FileText,
  Clock,
  Sparkles,
  Award,
  CheckCircle2,
  ChevronRight,
  ExternalLink
} from 'lucide-react';
import { UserProfile } from '../types';

interface ReportsWorkspaceProps {
  userProfile: UserProfile | null;
}

export const ReportsWorkspace: React.FC<ReportsWorkspaceProps> = ({ userProfile }) => {
  const [selectedReport, setSelectedReport] = useState<'audit_cert' | 'proc_diff' | 'draft_note'>('audit_cert');

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <FileSpreadsheet className="w-4 h-4" />
            <span>Workspace & Evidence Export</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white">
            Reports & Operational Workspace
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Generate exportable evidence audit certificates, inspect statutory difference reports, and review drafted office notes
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handlePrint}
            className="bg-[#070D1E] hover:bg-[#1C2541] border border-slate-700 text-slate-200 px-3.5 py-2 rounded-xl text-xs flex items-center space-x-2 transition"
          >
            <Printer className="w-4 h-4 text-cyan-400" />
            <span>Print Report</span>
          </button>
        </div>
      </div>

      {/* Report Selector Pills */}
      <div className="flex space-x-2 border-b border-[#1C2541] pb-3">
        <button
          onClick={() => setSelectedReport('audit_cert')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
            selectedReport === 'audit_cert'
              ? 'bg-cyan-500 text-slate-950 font-bold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          1. Evidence Audit Certificate (SC/ST Exemption 2024)
        </button>

        <button
          onClick={() => setSelectedReport('proc_diff')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
            selectedReport === 'proc_diff'
              ? 'bg-cyan-500 text-slate-950 font-bold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          2. Statutory Precedence Report (State vs Central Procurement)
        </button>

        <button
          onClick={() => setSelectedReport('draft_note')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
            selectedReport === 'draft_note'
              ? 'bg-cyan-500 text-slate-950 font-bold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]'
          }`}
        >
          3. Drafted Office Memorandum (Recruitment Fee Waiver)
        </button>
      </div>

      {/* REPORT CONTENT VIEW */}
      <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl p-6 shadow-2xl">
        {selectedReport === 'audit_cert' && (
          <div className="max-w-4xl mx-auto bg-white text-slate-900 p-8 rounded-xl shadow-2xl space-y-6 font-serif">
            {/* Government Emblem Header */}
            <div className="text-center border-b-2 border-slate-900 pb-4">
              <div className="text-xs uppercase tracking-widest font-bold text-slate-600">
                GOVERNMENT OF ASSAM • LEGISLATIVE DEPARTMENT
              </div>
              <h2 className="text-xl font-extrabold uppercase mt-1 tracking-wide">
                STATUTORY EVIDENCE AUDIT CERTIFICATE
              </h2>
              <div className="text-xs font-mono text-slate-500 mt-1">
                CERTIFICATE ID: NESFIC-EVD-CERT-2026-0894 • ISSUED UNDER NESFIC TRUST PROTOCOL
              </div>
            </div>

            {/* Certificate Details */}
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="font-bold text-slate-600 block uppercase text-[10px]">Subject Matter:</span>
                <span className="font-semibold text-slate-900">Exemption of Exam Fees for Scheduled Castes and Scheduled Tribes</span>
              </div>
              <div>
                <span className="font-bold text-slate-600 block uppercase text-[10px]">Governing Statute:</span>
                <span className="font-semibold text-slate-900">The Assam Scheduled Castes and Scheduled Tribes (Amendment) Act, 2024</span>
              </div>
              <div>
                <span className="font-bold text-slate-600 block uppercase text-[10px]">Enactment & Reference:</span>
                <span>Assam Act No. XXXI of 2024 / Gazette Extraordinary No. 530</span>
              </div>
              <div>
                <span className="font-bold text-slate-600 block uppercase text-[10px]">Assenting Authority:</span>
                <span>Hon'ble Governor of Assam (Assented on 19th October 2024)</span>
              </div>
            </div>

            {/* Verbatim Certified Excerpt */}
            <div className="border border-slate-300 p-4 rounded-lg bg-slate-50 space-y-2">
              <div className="text-[10px] uppercase font-bold tracking-wider text-slate-600">
                Certified Excerpt (Section 2 - Substitution of Section 4(b)):
              </div>
              <p className="text-sm italic leading-relaxed text-slate-800">
                "Fees, if any, prescribed for any examinations for selection to any service or posts shall be exempted in case of candidates belonging to the Scheduled Castes and Scheduled Tribes."
              </p>
            </div>

            {/* Cryptographic Proof Table */}
            <table className="w-full text-left text-xs border border-slate-300">
              <thead className="bg-slate-100 font-bold border-b border-slate-300 text-[10px] uppercase">
                <tr>
                  <th className="p-2">Forensic Check</th>
                  <th className="p-2">Registry Value</th>
                  <th className="p-2">Validation Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 font-mono text-[11px]">
                <tr>
                  <td className="p-2 font-sans font-semibold">Source File Hash</td>
                  <td className="p-2 text-slate-600">2159844f3b6b19a9786a760c6d7054f15bb36d75b3992b453a251b5bc93892eb</td>
                  <td className="p-2 text-emerald-700 font-bold font-sans">MATCHED</td>
                </tr>
                <tr>
                  <td className="p-2 font-sans font-semibold">Excerpt Hash</td>
                  <td className="p-2 text-slate-600">3f01d05729f8d7adc36b1912e628e384f4ca38f6ce55e2b7820d1de82554ca6e</td>
                  <td className="p-2 text-emerald-700 font-bold font-sans">MATCHED</td>
                </tr>
                <tr>
                  <td className="p-2 font-sans font-semibold">Signer Authority</td>
                  <td className="p-2 font-sans text-slate-600">Geetanjali Das Saikia, Secretary to Govt of Assam</td>
                  <td className="p-2 text-emerald-700 font-bold font-sans">INSTITUTIONALLY_AUTHORIZED</td>
                </tr>
                <tr>
                  <td className="p-2 font-sans font-semibold">Temporal Status</td>
                  <td className="p-2 font-sans text-slate-600">Active Law (Published 25th Oct 2024 - Perpetual)</td>
                  <td className="p-2 text-emerald-700 font-bold font-sans">IN_FORCE</td>
                </tr>
              </tbody>
            </table>

            {/* Official Certification Signature Block */}
            <div className="pt-6 border-t border-slate-400 flex items-center justify-between text-xs">
              <div>
                <div className="font-bold text-slate-900">Dr. Mridul Baruah</div>
                <div className="text-slate-600">Senior Verification Officer, Directorate of Legislative Inspection</div>
                <div className="text-[10px] text-slate-500 font-mono">Digitally Certified via NESFIC-D-36 Engine</div>
              </div>
              <div className="text-right">
                <span className="inline-block px-3 py-1 border-2 border-emerald-700 text-emerald-800 font-extrabold uppercase text-xs rounded tracking-widest">
                  VERIFIED STATUTORY EVIDENCE
                </span>
              </div>
            </div>
          </div>
        )}

        {selectedReport === 'proc_diff' && (
          <div className="space-y-4 text-xs">
            <h3 className="font-bold text-white text-base">
              Statutory Precedence Report: Assam Public Procurement Rules 2020 vs Central GFR 2017
            </h3>
            <p className="text-slate-300">
              Analysis of jurisdictional boundaries between state and central procurement instruments:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl space-y-2">
                <span className="font-bold text-cyan-400 block text-sm">Assam Public Procurement Rules, 2020</span>
                <p className="text-slate-300">
                  Enacted under Section 55 of the Assam Public Procurement Act, 2017 (Assam Act XXIV of 2017).
                  Applies mandatorily to all State Government departments, public sector undertakings, and local authorities.
                </p>
                <div className="p-2 rounded bg-slate-900 text-slate-400">
                  <span className="font-bold text-white">Rule 3 Prohibition: </span>
                  Splitting of procurement requirements to avoid sanction of higher authority is strictly prohibited.
                </div>
              </div>

              <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl space-y-2">
                <span className="font-bold text-amber-400 block text-sm">Central GFR 2017 / MoF Manual 2022</span>
                <p className="text-slate-300">
                  Executive financial guidelines issued by Department of Expenditure, Ministry of Finance, Government of India.
                  Applies directly to Central Ministries and CPSEs. Does not automatically override state rules without formal adoption notification.
                </p>
                <div className="p-2 rounded bg-slate-900 text-slate-400">
                  <span className="font-bold text-white">Precedence Verdict: </span>
                  Assam state-funded procurements are governed strictly by Assam Act XXIV of 2017.
                </div>
              </div>
            </div>
          </div>
        )}

        {selectedReport === 'draft_note' && (
          <div className="bg-[#070D1E] border border-slate-800 p-6 rounded-xl font-mono text-xs space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="font-bold text-cyan-400">AI DRAFTED MEMORANDUM (REQUIRES SECRETARY APPROVAL)</span>
              <span className="text-slate-400">STATUS: PROVISIONAL DRAFT</span>
            </div>
            <pre className="text-slate-200 whitespace-pre-wrap leading-relaxed font-mono">
{`GOVERNMENT OF ASSAM
DEPARTMENT OF PERSONNEL :: PERSONNEL (A)
DISPUR, GUWAHATI-781006

NO. AAP.45/2026/12                                          Dated Dispur, the 15th October, 2026

OFFICE MEMORANDUM

SUBJECT: Mandatory Exemption of Examination Fees for Scheduled Castes and Scheduled Tribes Candidates in all Direct Recruitment Examinations.

1. Attention is invited to Section 2 of The Assam Scheduled Castes and Scheduled Tribes (Reservation of Vacancies in Services and Posts) (Amendment) Act, 2024 (Assam Act No. XXXI of 2024), published in the Assam Gazette Extraordinary No. 530 dated 25th October, 2024.

2. Under the amended statutory provisions, Section 4(b) has been substituted with immediate effect as follows:
   "Fees, if any, prescribed for any examinations for selection to any service or posts shall be exempted in case of candidates belonging to the Scheduled Castes and Scheduled Tribes."

3. Accordingly, all Administrative Departments, Heads of Departments, and Appointing Authorities are hereby directed to strictly ensure that no examination or application fee is levied on SC and ST applicants in any forthcoming departmental recruitment advertisements.

4. This issues with the approval of the Competent Authority.

                                                                      (Pranjal Kalita)
                                                          Joint Secretary to the Govt. of Assam
                                                            Administrative Reforms Department`}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
