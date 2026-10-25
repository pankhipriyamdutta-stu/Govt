import {
  UserProfile,
  DemoUser,
  QueryResponse,
  DocumentItem,
  EvidenceTrail,
  VerificationQueueItem,
  AuditLogItem,
  SecurityAlertItem,
  EvalCaseItem
} from './types';

const API_BASE = '/api/v1';

// Token storage
let currentToken = localStorage.getItem('nesfic_token') || '';

export const setAuthToken = (token: string) => {
  currentToken = token;
  localStorage.setItem('nesfic_token', token);
};

const getHeaders = () => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  };
  if (currentToken) {
    headers['Authorization'] = `Bearer ${currentToken}`;
  }
  return headers;
};

export const api = {
  // Auth
  async login(username: string, password: string = 'GovtSecure@2026', mfa_code?: string) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, mfa_code })
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    setAuthToken(data.access_token);
    return data;
  },

  async demoLogin(username: string) {
    const res = await fetch(`${API_BASE}/auth/demo-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username })
    });
    if (!res.ok) throw new Error('Demo login failed');
    const data = await res.json();
    setAuthToken(data.access_token);
    return data;
  },

  async logout() {
    try {
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ token: currentToken })
      });
    } finally {
      setAuthToken('');
      localStorage.removeItem('nesfic_token');
    }
  },

  async getProfile(): Promise<UserProfile> {
    const res = await fetch(`${API_BASE}/auth/me`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Failed to load profile');
    return res.json();
  },

  async getDemoUsers(): Promise<DemoUser[]> {
    const res = await fetch(`${API_BASE}/auth/demo-users`);
    return res.json();
  },

  // AI Assistant
  async sendQuery(query: string, language: string = 'English'): Promise<QueryResponse> {
    const res = await fetch(`${API_BASE}/assistant/query`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ query, query_language: language })
    });
    if (!res.ok) throw new Error('Assistant query failed');
    return res.json();
  },

  async summarizeDocument(document_id: string) {
    const res = await fetch(`${API_BASE}/assistant/summarize`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ document_id })
    });
    return res.json();
  },

  async compareVersions(document_id_a: string, document_id_b: string) {
    const res = await fetch(`${API_BASE}/assistant/compare-versions`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ document_id_a, document_id_b })
    });
    return res.json();
  },

  async translatePassage(text: string, target_language: string = 'Assamese') {
    const res = await fetch(`${API_BASE}/assistant/translate`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ text, target_language })
    });
    return res.json();
  },

  async draftOfficeNote(subject: string, evidence_ids: string[]) {
    const res = await fetch(`${API_BASE}/assistant/draft`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ subject, evidence_ids })
    });
    return res.json();
  },

  // Documents
  async listDocuments(params?: {
    query?: string;
    department?: string;
    doc_type?: string;
    verification_status?: string;
    include_quarantined?: boolean;
  }): Promise<DocumentItem[]> {
    const sp = new URLSearchParams();
    if (params?.query) sp.append('query', params.query);
    if (params?.department) sp.append('department', params.department);
    if (params?.doc_type) sp.append('doc_type', params.doc_type);
    if (params?.verification_status) sp.append('verification_status', params.verification_status);
    if (params?.include_quarantined) sp.append('include_quarantined', 'true');

    const res = await fetch(`${API_BASE}/documents?${sp.toString()}`, { headers: getHeaders() });
    return res.json();
  },

  async getDocument(docId: string) {
    const res = await fetch(`${API_BASE}/documents/${docId}`, { headers: getHeaders() });
    return res.json();
  },

  async uploadDocument(formData: FormData) {
    const headers: Record<string, string> = {};
    if (currentToken) {
      headers['Authorization'] = `Bearer ${currentToken}`;
    }
    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      headers,
      body: formData
    });
    return res.json();
  },

  async scanDocumentRules(documentId: string) {
    const res = await fetch(`${API_BASE}/documents/scan-rules`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ document_id: documentId })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Document scanning failed');
    }
    return res.json();
  },

  async scanUploadedDocument(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const headers: Record<string, string> = {};
    if (currentToken) {
      headers['Authorization'] = `Bearer ${currentToken}`;
    }
    const res = await fetch(`${API_BASE}/documents/scan-upload`, {
      method: 'POST',
      headers,
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'File scanning failed');
    }
    return res.json();
  },

  // Source Detective
  async inspectEvidenceTrail(claimOrHash: string): Promise<EvidenceTrail> {
    const res = await fetch(`${API_BASE}/evidence/detective/${encodeURIComponent(claimOrHash)}`, {
      headers: getHeaders()
    });
    if (!res.ok) throw new Error('Evidence trail not found');
    return res.json();
  },

  async getEvidenceLedger(document_id?: string) {
    const sp = document_id ? `?document_id=${document_id}` : '';
    const res = await fetch(`${API_BASE}/evidence/ledger${sp}`, { headers: getHeaders() });
    return res.json();
  },

  // Verification Queue
  async getVerificationQueue(status?: string): Promise<VerificationQueueItem[]> {
    const sp = status ? `?status=${status}` : '';
    const res = await fetch(`${API_BASE}/verification/queue${sp}`, { headers: getHeaders() });
    return res.json();
  },

  async recordVerificationDecision(itemId: number, decision: string, rationale: string) {
    const res = await fetch(`${API_BASE}/verification/${itemId}/decision`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ decision, rationale })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Decision rejected');
    }
    return res.json();
  },

  // Admin & Security
  async getAuditLogs(limit: number = 30): Promise<{ chain_intact_overall: boolean; logs: AuditLogItem[] }> {
    const res = await fetch(`${API_BASE}/admin/audit-logs?limit=${limit}`, { headers: getHeaders() });
    return res.json();
  },

  async getSecurityAlerts(): Promise<SecurityAlertItem[]> {
    const res = await fetch(`${API_BASE}/admin/security-alerts`, { headers: getHeaders() });
    return res.json();
  },

  async getSystemMetrics() {
    const res = await fetch(`${API_BASE}/admin/metrics`, { headers: getHeaders() });
    return res.json();
  },

  async getEvaluationSuite(): Promise<EvalCaseItem[]> {
    const res = await fetch(`${API_BASE}/admin/eval-suite`, { headers: getHeaders() });
    return res.json();
  },

  async getSources() {
    const res = await fetch(`${API_BASE}/admin/sources`, { headers: getHeaders() });
    return res.json();
  },

  // Generative AI Configuration & Training Harness
  async getAIConfig() {
    const res = await fetch(`${API_BASE}/admin/ai-config`, { headers: getHeaders() });
    return res.json();
  },

  async updateAIConfig(config: { api_key?: string; model_name?: string; temperature?: number }) {
    const res = await fetch(`${API_BASE}/admin/ai-config`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(config)
    });
    return res.json();
  },

  async testAIConnection(apiKey?: string, modelName?: string) {
    const res = await fetch(`${API_BASE}/admin/test-ai-connection`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ api_key: apiKey, model_name: modelName })
    });
    return res.json();
  },

  async getAITrainingStatus() {
    const res = await fetch(`${API_BASE}/admin/ai-training-status`, { headers: getHeaders() });
    return res.json();
  },

  async rebuildTrainingDataset() {
    const res = await fetch(`${API_BASE}/admin/rebuild-training-dataset`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  },

  async runTrainingEvaluation() {
    const res = await fetch(`${API_BASE}/admin/run-training-eval`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  },

  // Sovereign Cybersecurity, CERT-In, & PKI Verification
  async getSecurityPosture() {
    const res = await fetch(`${API_BASE}/security/posture`, { headers: getHeaders() });
    return res.json();
  },

  async getCertInIncidents() {
    const res = await fetch(`${API_BASE}/security/cert-in/incidents`, { headers: getHeaders() });
    return res.json();
  },

  async exportCertInDossier(eventId: number) {
    const res = await fetch(`${API_BASE}/security/cert-in/export/${eventId}`, { headers: getHeaders() });
    return res.json();
  },

  async runPenetrationTest() {
    const res = await fetch(`${API_BASE}/security/run-penetration-test`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  },

  async getCCATrustStore() {
    const res = await fetch(`${API_BASE}/security/cca-trust-store`, { headers: getHeaders() });
    return res.json();
  },

  async getSourceCertificate(documentId: string) {
    const res = await fetch(`${API_BASE}/security/source-certificate/${encodeURIComponent(documentId)}`, {
      headers: getHeaders()
    });
    return res.json();
  },

  // -------------------------------------------------------------------------
  // VERITRACE AI: Document Fraud, Forensics, Fact Verification & Provenance
  // -------------------------------------------------------------------------
  async getVeritraceStats() {
    const res = await fetch(`${API_BASE}/veritrace/stats`, { headers: getHeaders() });
    return res.json();
  },

  async getVeritraceDocuments(riskFilter?: string, statusFilter?: string) {
    const params = new URLSearchParams();
    if (riskFilter && riskFilter !== 'ALL') params.append('risk_filter', riskFilter);
    if (statusFilter && statusFilter !== 'ALL') params.append('status_filter', statusFilter);
    const res = await fetch(`${API_BASE}/veritrace/documents?${params.toString()}`, { headers: getHeaders() });
    return res.json();
  },

  async getVeritraceDocument(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}`, { headers: getHeaders() });
    return res.json();
  },

  async uploadVeritraceDocument(formData: FormData) {
    const headers: Record<string, string> = {};
    if (currentToken) {
      headers['Authorization'] = `Bearer ${currentToken}`;
    }
    const res = await fetch(`${API_BASE}/veritrace/upload`, {
      method: 'POST',
      headers,
      body: formData
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(err.detail || 'Upload failed');
    }
    return res.json();
  },

  async analyzeVeritraceDocument(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/analyze`, {
      method: 'POST',
      headers: getHeaders()
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
      throw new Error(err.detail || 'Analysis failed');
    }
    return res.json();
  },

  async getVeritraceForensics(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/forensics`, { headers: getHeaders() });
    return res.json();
  },

  async getVeritraceClaims(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/claims`, { headers: getHeaders() });
    return res.json();
  },

  async getVeritraceProvenance(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/provenance`, { headers: getHeaders() });
    return res.json();
  },

  async getVeritraceReport(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/report`, { headers: getHeaders() });
    return res.json();
  },

  // -------------------------------------------------------------------------
  // Sovereign Forensic Innovations & Zero-Leakage ML Evaluation
  // -------------------------------------------------------------------------
  async getC3iHubCertificate(documentId: string, officerName?: string) {
    const params = new URLSearchParams();
    if (officerName) params.append('officer_name', officerName);
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/c3ihub-certificate?${params.toString()}`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async verifyC3iHubCertificate(certificate: any) {
    const res = await fetch(`${API_BASE}/veritrace/c3ihub-certificate/verify`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(certificate)
    });
    return res.json();
  },

  async runCopyMoveDetection(documentId: string, pageNumber: number = 0) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/cmfd?page_number=${pageNumber}`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  },

  async enhanceDocumentScan(documentId: string, pageNumber: number = 0) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/enhance-scan?page_number=${pageNumber}`, {
      method: 'POST',
      headers: getHeaders()
    });
    return res.json();
  },

  async checkPromptContainment(text: string) {
    const res = await fetch(`${API_BASE}/veritrace/containment-check`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ text })
    });
    return res.json();
  },

  async getStatutoryCompliance(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/statutory-compliance`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async getStructuralDiscrepancies(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/structural-discrepancies`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async getIndicScriptAnalysis(documentId: string) {
    const res = await fetch(`${API_BASE}/veritrace/documents/${encodeURIComponent(documentId)}/script-analysis`, {
      headers: getHeaders()
    });
    return res.json();
  },

  async getMLModelMetrics() {
    const res = await fetch(`${API_BASE}/veritrace/ml/metrics`, { headers: getHeaders() });
    return res.json();
  },

  async retrainMLModels() {
    const res = await fetch(`${API_BASE}/veritrace/ml/retrain`, {
      method: 'POST',
      headers: getHeaders()
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Retraining failed' }));
      throw new Error(err.detail || 'Retraining failed');
    }
    return res.json();
  }
};

