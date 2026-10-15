export type TripartiteStatus = 'VERIFIED' | 'VERIFICATION_REQUIRED' | 'CANNOT_GENERATE';

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  full_name: string;
  department: string;
  department_code: string;
  role_id: string;
  role_name: string;
  permitted_action: string;
  mfa_enabled: boolean;
}

export interface DemoUser {
  username: string;
  full_name: string;
  role_id: string;
  role_name: string;
  department: string;
}

export interface ClaimItem {
  claim_id: string;
  claim_text: string;
  verification_status: string;
  evidence_hash: string;
  section?: string;
}

export interface CitationItem {
  citation_id: string;
  document_id: string;
  document_title: string;
  section: string;
  issuing_authority: string;
  sha256_hash: string;
  locator: string;
  verification_flag: string;
}

export interface QueryResponse {
  query: string;
  query_language: string;
  status: TripartiteStatus;
  answer: string;
  limitation?: string;
  claims: ClaimItem[];
  citations: CitationItem[];
  retrieved_evidence: any[];
  latency_ms: number;
  tamper_hash: string;
  trust_policy_passed: boolean;
  model_used: string;
  suggested_actions: string[];
}

export interface DocumentItem {
  id: number;
  document_id: string;
  document_title: string;
  document_type: string;
  department: string;
  issuing_authority: string;
  reference_number?: string;
  publication_date?: string;
  effective_date?: string;
  verification_status: string;
  approval_status: string;
  classification: string;
  original_file_hash: string;
  notes?: string;
}

export interface EvidenceTrail {
  claim_id: string;
  claim_text: string;
  support_status: string;
  document_id: string;
  document_title: string;
  issuing_authority: string;
  department: string;
  reference_number: string;
  publication_date: string;
  issue_date: string;
  effective_date: string;
  jurisdiction: string;
  version_number: string;
  is_active_version: boolean;
  locator: {
    page_id: string;
    printed_page_number: string;
    physical_pdf_page: number;
    section_number: string;
    paragraph_id: string;
  };
  exact_evidence_text: string;
  evidence_hash: string;
  source_file_hash: string;
  hash_matches_original: boolean;
  cryptographic_verification: {
    has_digital_signature: boolean;
    signature_format: string;
    signature_valid: boolean;
    cert_chain_valid: boolean;
    signing_time: string;
    signer_identity: string;
    signer_institutional_authority: string;
    anomaly_flags: string[];
  };
  trust_policy_verdict: {
    overall_status: string;
    requires_human_review: boolean;
    reviewer_notes: string;
  };
}

export interface VerificationQueueItem {
  id: number;
  document_id: string;
  document_title: string;
  department: string;
  submission_type: string;
  submitted_by: string;
  current_status: string;
  reviewer_notes?: string;
  decision?: string;
  decided_at?: string;
  created_at?: string;
}

export interface AuditLogItem {
  id: number;
  user_id: string;
  department_id: string;
  query_text: string;
  query_language: string;
  response_status: string;
  latency_ms: number;
  claims_count: number;
  citations_count: number;
  tamper_hash: string;
  previous_hash: string;
  chain_intact: boolean;
  timestamp: string;
}

export interface SecurityAlertItem {
  id: number;
  event_type: string;
  severity: string;
  source_ip: string;
  user_id: string;
  details: string;
  payload_sample?: string;
  action_taken: string;
  timestamp: string;
}

export interface EvalCaseItem {
  evaluation_id: string;
  query: string;
  expected_status: string;
  retrieved_documents: string;
  factual_support_score: number;
  citation_accuracy: number;
  version_accuracy: number;
  abstention_correctness: number;
  result: string;
  reviewer_notes: string;
}
