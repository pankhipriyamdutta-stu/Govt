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
  async login(username: string, password: string = 'GovtSecure@2026') {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) throw new Error('Login failed');
    const data = await res.json();
    setAuthToken(data.access_token);
    return data;
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
  }
};
