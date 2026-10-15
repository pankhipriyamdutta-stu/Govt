import React, { useState, useEffect } from 'react';
import {
  FolderLock,
  Search,
  Filter,
  UploadCloud,
  FileCheck2,
  AlertTriangle,
  XCircle,
  Lock,
  ExternalLink,
  Clock,
  Eye,
  ShieldCheck,
  X,
  CheckCircle2
} from 'lucide-react';
import { DocumentItem, UserProfile } from '../types';
import { PageId } from '../components/Sidebar';
import { api } from '../api';

interface DocumentRepositoryProps {
  userProfile: UserProfile | null;
  onNavigate: (page: PageId, extraData?: any) => void;
}

export const DocumentRepository: React.FC<DocumentRepositoryProps> = ({ userProfile, onNavigate }) => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [selectedType, setSelectedType] = useState('ALL');
  const [selectedStatus, setSelectedStatus] = useState('ALL');
  const [includeQuarantined, setIncludeQuarantined] = useState(false);

  // Modals
  const [selectedDoc, setSelectedDoc] = useState<any>(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadDept, setUploadDept] = useState('Finance Department');
  const [uploadType, setUploadType] = useState('CIRCULAR');
  const [uploadRef, setUploadRef] = useState('');
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState<any>(null);

  const fetchDocs = () => {
    setLoading(true);
    api.listDocuments({
      query: searchQuery || undefined,
      department: selectedDept !== 'ALL' ? selectedDept : undefined,
      doc_type: selectedType !== 'ALL' ? selectedType : undefined,
      verification_status: selectedStatus !== 'ALL' ? selectedStatus : undefined,
      include_quarantined: includeQuarantined
    }).then((docs) => {
      setDocuments(docs);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchDocs();
  }, [selectedDept, selectedType, selectedStatus, includeQuarantined]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchDocs();
  };

  const handleOpenDocModal = async (docId: string) => {
    try {
      const data = await api.getDocument(docId);
      setSelectedDoc(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile || !uploadTitle.trim()) return;
    setUploadLoading(true);
    setUploadSuccess(null);
    try {
      const fd = new FormData();
      fd.append('file', uploadFile);
      fd.append('document_title', uploadTitle.trim());
      fd.append('department', uploadDept);
      fd.append('document_type', uploadType);
      if (uploadRef) fd.append('reference_number', uploadRef);

      const res = await api.uploadDocument(fd);
      setUploadSuccess(res);
      setUploadFile(null);
      setUploadTitle('');
      fetchDocs();
    } catch (e) {
      console.error(e);
    } finally {
      setUploadLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#1C2541]/70 border border-[#29365C] p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <FolderLock className="w-4 h-4" />
            <span>Government Knowledge Repository</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white">
            Official Acts, Statutory Rules & Citizen Charters
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Curated, version-controlled repository of Assam State Gazettes and Union statutory instruments
          </p>
        </div>

        <button
          onClick={() => setShowUploadModal(true)}
          className="bg-gradient-to-r from-cyan-500 to-teal-600 hover:from-cyan-400 hover:to-teal-500 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs flex items-center space-x-2 transition shadow-lg"
        >
          <UploadCloud className="w-4 h-4" />
          <span>Ingest New Document</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-[#070D1E] border border-[#1C2541] p-4 rounded-2xl space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex items-center space-x-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filter by title, reference number, or issuing authority..."
              className="w-full bg-[#1C2541]/70 border border-slate-700 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-400 focus:outline-none focus:border-cyan-400"
            />
          </div>
          <button
            type="submit"
            className="bg-[#1C2541] hover:bg-[#29365C] border border-slate-700 text-slate-200 px-4 py-2 rounded-xl text-xs font-semibold transition"
          >
            Search
          </button>
        </form>

        <div className="flex flex-wrap items-center gap-3 text-xs">
          <div className="flex items-center space-x-1.5 text-slate-400">
            <Filter className="w-3.5 h-3.5 text-cyan-400" />
            <span>Filters:</span>
          </div>

          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="bg-[#1C2541] border border-slate-700 text-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none text-xs"
          >
            <option value="ALL">All Departments</option>
            <option value="Legislative">Legislative Department</option>
            <option value="Administrative Reforms">Administrative Reforms (ART)</option>
            <option value="Finance">Finance Department</option>
            <option value="Guwahati Municipal">Guwahati Municipal Corp (GMC)</option>
            <option value="Personnel">DoPT (Union)</option>
          </select>

          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="bg-[#1C2541] border border-slate-700 text-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none text-xs"
          >
            <option value="ALL">All Types</option>
            <option value="ACT">Primary Act / Statute</option>
            <option value="AMENDMENT_ACT">Amendment Act</option>
            <option value="STATUTORY_RULES">Subordinate Rules</option>
            <option value="CITIZEN_CHARTER">Citizen Charter</option>
            <option value="OFFICE_MEMORANDUM">Office Memorandum</option>
          </select>

          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="bg-[#1C2541] border border-slate-700 text-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none text-xs"
          >
            <option value="ALL">All Trust States</option>
            <option value="VERIFIED">Verified Primary</option>
            <option value="PENDING">Pending Verification</option>
            <option value="UNCONFIRMED">Unconfirmed Vintage</option>
          </select>

          <label className="flex items-center space-x-1.5 ml-auto text-slate-400 cursor-pointer">
            <input
              type="checkbox"
              checked={includeQuarantined}
              onChange={(e) => setIncludeQuarantined(e.target.checked)}
              className="rounded bg-slate-800 border-slate-700 text-rose-500 focus:ring-rose-500"
            />
            <span className="text-[11px] text-rose-400 font-medium">Show Quarantined / Excluded Files</span>
          </label>
        </div>
      </div>

      {/* Documents Table */}
      <div className="bg-[#1C2541]/50 border border-[#29365C] rounded-2xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#070D1E] text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/60">
              <tr>
                <th className="py-3 px-4">Doc ID</th>
                <th className="py-3 px-4">Document Title</th>
                <th className="py-3 px-4">Department & Authority</th>
                <th className="py-3 px-4">Type & Category</th>
                <th className="py-3 px-4">Publication / In-Force</th>
                <th className="py-3 px-4">Trust State</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {documents.map((doc) => {
                const isQuarantined = doc.approval_status.includes('REJECTED_QUARANTINED') || doc.classification.includes('RESTRICTED');
                return (
                  <tr
                    key={doc.document_id}
                    className={`transition hover:bg-[#1C2541]/80 ${
                      isQuarantined ? 'bg-rose-500/5' : ''
                    }`}
                  >
                    <td className="py-3 px-4 font-mono text-[11px] text-cyan-400 font-semibold">
                      {doc.document_id}
                    </td>
                    <td className="py-3 px-4 max-w-xs">
                      <div className="font-bold text-white truncate">{doc.document_title}</div>
                      <div className="font-mono text-[10px] text-slate-400 truncate">
                        Ref: {doc.reference_number || 'N/A'}
                      </div>
                    </td>
                    <td className="py-3 px-4 max-w-[200px]">
                      <div className="text-slate-200 truncate">{doc.department}</div>
                      <div className="text-[10px] text-slate-400 truncate">{doc.issuing_authority}</div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono text-[10px]">
                        {doc.document_type}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-[11px] text-slate-300 font-mono">
                      {doc.publication_date || doc.effective_date || 'In Force'}
                    </td>
                    <td className="py-3 px-4">
                      {isQuarantined ? (
                        <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-bold flex items-center space-x-1 w-max">
                          <Lock className="w-3 h-3" />
                          <span>QUARANTINED</span>
                        </span>
                      ) : doc.verification_status.includes('VERIFIED') ? (
                        <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold flex items-center space-x-1 w-max">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>VERIFIED</span>
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold flex items-center space-x-1 w-max">
                          <AlertTriangle className="w-3 h-3" />
                          <span>REVIEW REQUIRED</span>
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-right space-x-2">
                      <button
                        onClick={() => handleOpenDocModal(doc.document_id)}
                        className="text-slate-300 hover:text-white bg-[#070D1E] px-2.5 py-1 rounded border border-slate-700 text-[11px] hover:border-cyan-400 transition"
                      >
                        Details
                      </button>
                      <button
                        onClick={() => onNavigate('detective', { claimId: doc.document_id })}
                        className="text-cyan-400 hover:text-cyan-300 bg-cyan-500/10 px-2.5 py-1 rounded border border-cyan-500/30 text-[11px] font-medium transition"
                      >
                        Lineage
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* DOCUMENT DETAIL MODAL */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-[#0B132B] border border-[#29365C] rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <span className="text-xs font-mono text-cyan-400">{selectedDoc.document.document_id}</span>
                <h3 className="text-base font-bold text-white">{selectedDoc.document.title}</h3>
              </div>
              <button
                onClick={() => setSelectedDoc(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs bg-[#070D1E] p-4 rounded-xl border border-slate-800">
              <div><span className="text-slate-400">Department:</span> <span className="font-semibold text-slate-200">{selectedDoc.document.department}</span></div>
              <div><span className="text-slate-400">Issuing Authority:</span> <span className="font-semibold text-slate-200">{selectedDoc.document.issuing_authority}</span></div>
              <div><span className="text-slate-400">Reference Number:</span> <span className="font-semibold text-slate-200">{selectedDoc.document.reference_number || 'N/A'}</span></div>
              <div><span className="text-slate-400">Effective Date:</span> <span className="font-semibold text-slate-200">{selectedDoc.document.effective_date || 'In Force'}</span></div>
              <div className="col-span-2">
                <span className="text-slate-400">SHA-256 Hash:</span> 
                <span className="font-mono text-cyan-400 text-[11px] ml-1">{selectedDoc.document.sha256_hash}</span>
              </div>
            </div>

            {selectedDoc.document.notes && (
              <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs">
                <span className="font-bold">Provenance Audit Note: </span>
                {selectedDoc.document.notes}
              </div>
            )}

            {/* Live Cryptographic Inspection Output */}
            {selectedDoc.live_inspection && (
              <div className="bg-[#070D1E] border border-slate-800 p-4 rounded-xl space-y-2 text-xs">
                <div className="font-bold text-slate-200 flex items-center space-x-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Real-Time Cryptographic File Verification</span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div>Producer: <span className="font-mono text-slate-300">{selectedDoc.live_inspection.producer || 'Standard PDF Engine'}</span></div>
                  <div>Signature Format: <span className="font-mono text-cyan-400">{selectedDoc.live_inspection.signature_format}</span></div>
                  <div>Signer Authority: <span className="font-mono text-amber-300">{selectedDoc.live_inspection.signer_authority_status}</span></div>
                  <div>Trust Recommendation: <span className="font-mono text-emerald-400">{selectedDoc.live_inspection.trust_recommendation}</span></div>
                </div>
              </div>
            )}

            <div className="flex justify-end space-x-3 pt-3 border-t border-slate-800">
              <button
                onClick={() => {
                  const docId = selectedDoc.document.document_id;
                  setSelectedDoc(null);
                  onNavigate('detective', { claimId: docId });
                }}
                className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs transition"
              >
                Inspect in Source Detective →
              </button>
            </div>
          </div>
        </div>
      )}

      {/* UPLOAD & QUARANTINE MODAL */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-[#0B132B] border border-[#29365C] rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                <UploadCloud className="w-5 h-5 text-cyan-400" />
                <h3 className="text-base font-bold text-white">Secure Government Document Ingestion</h3>
              </div>
              <button
                onClick={() => {
                  setShowUploadModal(false);
                  setUploadSuccess(null);
                }}
                className="text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              Every uploaded document is automatically hashed (SHA-256), scanned for malware & converter anomalies, 
              and quarantined until human Verification Officer certification.
            </p>

            {uploadSuccess ? (
              <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs space-y-2">
                <div className="font-bold text-sm flex items-center space-x-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Document Ingested into Quarantine Vault</span>
                </div>
                <div>Assigned ID: <span className="font-mono text-white font-bold">{uploadSuccess.document_id}</span></div>
                <div>SHA-256: <span className="font-mono text-cyan-300">{uploadSuccess.sha256_hash}</span></div>
                <p className="text-[11px] text-slate-300">{uploadSuccess.message}</p>
                <button
                  onClick={() => {
                    setShowUploadModal(false);
                    setUploadSuccess(null);
                  }}
                  className="mt-2 w-full bg-slate-800 text-white font-semibold py-2 rounded-lg text-xs"
                >
                  Close & View in Repository
                </button>
              </div>
            ) : (
              <form onSubmit={handleUploadSubmit} className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Document Title:</label>
                  <input
                    type="text"
                    required
                    value={uploadTitle}
                    onChange={(e) => setUploadTitle(e.target.value)}
                    placeholder="e.g. Circular on Procurement Threshold Revisions 2026"
                    className="w-full bg-[#070D1E] border border-slate-700 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-cyan-400"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-400 font-semibold mb-1">Department:</label>
                    <input
                      type="text"
                      value={uploadDept}
                      onChange={(e) => setUploadDept(e.target.value)}
                      className="w-full bg-[#070D1E] border border-slate-700 rounded-xl px-3 py-2 text-slate-200 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 font-semibold mb-1">Document Type:</label>
                    <select
                      value={uploadType}
                      onChange={(e) => setUploadType(e.target.value)}
                      className="w-full bg-[#070D1E] border border-slate-700 rounded-xl px-3 py-2 text-slate-200 focus:outline-none"
                    >
                      <option value="CIRCULAR">Departmental Circular</option>
                      <option value="OFFICE_ORDER">Office Order</option>
                      <option value="NOTIFICATION">Gazette Notification</option>
                      <option value="GUIDELINE">Standard Operating Procedure</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Official Reference Number (Optional):</label>
                  <input
                    type="text"
                    value={uploadRef}
                    onChange={(e) => setUploadRef(e.target.value)}
                    placeholder="e.g. NO. FEB/PRO/2026/04"
                    className="w-full bg-[#070D1E] border border-slate-700 rounded-xl px-3 py-2 text-slate-200 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Select File (PDF):</label>
                  <input
                    type="file"
                    required
                    accept=".pdf,.docx"
                    onChange={(e) => setUploadFile(e.target.files ? e.target.files[0] : null)}
                    className="w-full bg-[#070D1E] border border-slate-700 rounded-xl px-3 py-2 text-slate-300 focus:outline-none"
                  />
                </div>

                <div className="pt-2 flex justify-end space-x-2">
                  <button
                    type="button"
                    onClick={() => setShowUploadModal(false)}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={uploadLoading}
                    className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-5 py-2 rounded-xl text-xs transition disabled:opacity-50"
                  >
                    {uploadLoading ? 'Scanning & Hashing...' : 'Ingest Document'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
