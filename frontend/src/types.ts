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
  security_clearance?: string;
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

// -------------------------------------------------------------
// SOVEREIGN CYBERSECURITY & CERT-In TYPES
// -------------------------------------------------------------
export interface SecurityPosture {
  status: string;
  zero_trust_enforced: boolean;
  environment: string;
  ntp_synchronized: boolean;
  cert_in_compliance: {
    status: string;
    section: string;
    dispatch_desk: string;
    incident_retention: string;
  };
  dpdp_act_2023_compliance: {
    status: string;
    quarantined_records: number;
    pii_shield_active: boolean;
  };
  cryptographic_integrity: {
    tamper_evident_chain_intact: boolean;
    dual_hash_engine: string;
    cca_india_root_anchors: number;
  };
  threat_telemetry: {
    total_adversarial_intercepts: number;
    critical_threats_blocked: number;
    active_mitigations: string[];
  };
}

export interface CertInIncident {
  cert_in_form_id: string;
  statutory_mandate: string;
  incident_identifier: string;
  reporting_organization: {
    organization_name: string;
    nodal_enclave: string;
    service_name: string;
    environment: string;
    ntp_synchronized: boolean;
    ntp_server: string;
  };
  incident_timeline: {
    detected_at_ist: string;
    detected_at_utc: string;
    reporting_window_compliance: string;
  };
  classification: {
    cert_in_category: string;
    mitre_atlas_id: string;
    severity_level: string;
    legal_regulatory_ref: string;
  };
  attacker_and_target_profile: {
    source_ip: string;
    actor_identity: string;
    targeted_subsystem: string;
    affected_records: string;
  };
  technical_details: {
    incident_summary: string;
    payload_sample_redacted: string;
    payload_sha256_digest: string;
    defense_action_taken: string;
    containment_status: string;
  };
  remediation_and_containment: string[];
  official_dispatch_channel: {
    cert_in_incident_desk: string;
    cert_in_toll_free: string;
    portal: string;
  };
}

export interface PenTestResult {
  test_id: string;
  threat_category: string;
  attack_vector: string;
  simulated_payload: string;
  expected_outcome: string;
  actual_outcome: string;
  status: 'PASSED' | 'FAILED';
  cvss_score: string;
  mitigation: string;
}

export interface PenetrationTestReport {
  audit_id: string;
  timestamp_ist: string;
  target_system: string;
  security_classification: string;
  overall_status: string;
  defense_score_percentage: number;
  tests_passed: number;
  total_tests: number;
  standards_evaluated: string[];
  test_results: PenTestResult[];
}

export interface CCATrustStore {
  authority: string;
  governing_statute: string;
  trust_anchors: Record<string, {
    name: string;
    entity: string;
    jurisdiction: string;
    licensed_under_cca: boolean;
    trust_tier: string;
    standard: string;
    rfc3161_tsa: string;
  }>;
  authorized_gazetted_signatories: Record<string, {
    name: string;
    role: string;
    authority_level: string;
    department: string;
    authorized: boolean;
  }>;
}

export interface StatutorySourceCertificate {
  certificate_id: string;
  document_id: string;
  document_title: string;
  issuing_authority: string;
  attestation_timestamp_ist: string;
  attesting_officer: string;
  cryptographic_hashes: {
    sha256: string;
    sha512: string;
    hash_algorithm: string;
    tamper_evident_status: string;
  };
  digital_signature_profile: {
    has_pades_pkcs7_signature: boolean;
    signature_format: string;
    certifying_authority: string;
    cca_india_licensed: boolean;
    signer_authority_status: string;
  };
  forensic_integrity_verdict: string;
  anomalies_detected: string[];
  legal_admissibility: string;
}

export interface VeritraceDocItem {
  document_id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  sha256_hash: string;
  page_count: number;
  ocr_used: boolean;
  has_digital_signature: boolean;
  overall_risk_verdict: 'LOW' | 'MODERATE' | 'HIGH' | 'INSUFFICIENT_DATA';
  overall_risk_score: number;
  analysis_status: string;
  claims_count?: number;
  claims_verified_count?: number;
  created_at?: string;
}

export interface VeritraceFinding {
  finding_id: string;
  category: string;
  status: string;
  severity: string;
  description: string;
  evidence: any[];
  limitations: string[];
}

export interface VeritraceClaim {
  claim_id: string;
  claim_text: string;
  subject: string;
  predicate: string;
  object: string;
  verification_status: 'SUPPORTED' | 'CONTRADICTED' | 'INSUFFICIENT_EVIDENCE' | 'CONFLICTING_SOURCES' | 'NOT_CHECKED';
  confidence_score: number;
  reasoning: string;
  limitations?: string;
  evidence: Array<{
    evidence_id: string;
    source_title: string;
    source_url: string;
    source_authority?: string;
    publication_date?: string;
    passage_text: string;
    alignment_label: string;
    similarity_score: number;
  }>;
}

export interface VeritraceProvenanceGraph {
  document_id: string;
  filename: string;
  sha256: string;
  nodes: Array<{
    id: string;
    node_type: string;
    label: string;
    source_url?: string;
    authority?: string;
    publication_date?: string;
    metadata?: any;
  }>;
  edges: Array<{
    source: string;
    target: string;
    relation_type: string;
    confidence: number;
    evidence_basis?: string;
  }>;
  legend: Record<string, string>;
  earliest_discovered_record?: {
    discovered: boolean;
    earliest_discovered_date: string;
    searched_scope_description: string;
    disclaimer: string;
  };
  search_scope: {
    searched: string[];
    unavailable: string[];
  };
}

export interface VeritraceReport {
  report_metadata: {
    report_id: string;
    generated_at: string;
    system_name: string;
    system_version: string;
  };
  document_summary: {
    document_id: string;
    filename: string;
    file_type: string;
    file_size_bytes: number;
    page_count: number;
    sha256_hash: string;
    sha512_hash?: string;
    uploaded_by: string;
    upload_timestamp?: string;
    malware_scan: {
      status: string;
      details: string;
    };
  };
  executive_verdict: {
    verdict: 'LOW' | 'MODERATE' | 'HIGH' | 'INSUFFICIENT_DATA';
    risk_score: number;
    confidence: string;
    explanation: string;
    policy_applied: string;
  };
  independent_dimensions: {
    file_integrity: any;
    digital_signatures: any;
    visual_tampering_forensics: any;
    document_structure_and_metadata: any;
    ml_fraud_risk: any;
    factual_accuracy: any;
    source_provenance: any;
  };
  all_forensic_findings: VeritraceFinding[];
  limitations_and_assumptions: string[];
  recommended_next_steps: string[];
}

export interface C3iHubCertificate {
  certificate_id: string;
  standards_framework: string;
  statutory_compliance: string;
  document_id: string;
  filename: string;
  attestation_timestamp_utc: string;
  merkle_provenance: {
    merkle_root: string;
    tree_depth: number;
    leaf_count: number;
    leaf_descriptors: Array<{
      index: number;
      node: string;
      hash: string;
    }>;
  };
  custody_chain_status: string;
  attesting_authority: string;
  verification_qr_payload: string;
}

export interface SovereignCMFDResult {
  copy_move_detected: boolean;
  duplicated_pairs_count: number;
  risk_rating: 'LOW' | 'MODERATE' | 'HIGH';
  sample_clusters?: Array<{
    pt1: [number, number];
    pt2: [number, number];
    descriptor_distance: number;
    spatial_displacement_px: number;
  }>;
  summary: string;
  document_id?: string;
  page_inspected?: number;
  research_institution?: string;
}

export interface AdaptiveScanEnhancementResult {
  enhanced: boolean;
  restoration_technique?: string;
  output_path?: string;
  output_filename?: string;
  resolution_maintained?: string;
  error?: string;
}

export interface AdversarialContainmentResult {
  contains_injection_vectors: boolean;
  quarantined_count: number;
  detected_patterns: string[];
  safety_action: string;
  quarantined_text: string;
  research_institution?: string;
}

export interface StatutoryComplianceAuditResult {
  services_identified_count: number;
  statutory_matches: Array<{
    service: string;
    notified_statutory_limit_days: number;
    competent_authority: string;
    governing_statute: string;
    source_reference: string;
  }>;
  governing_jurisdiction: string;
}

export interface MLModelMetrics {
  status: string;
  metadata: {
    model_version: string;
    training_timestamp_utc: string;
    model_type: string;
    split_strategy: string;
    train_samples: number;
    test_samples: number;
    train_document_groups: string[];
    test_document_groups: string[];
    metrics: {
      precision: number;
      recall: number;
      f1_score: number;
      roc_auc: number;
      false_positive_rate: number;
      false_negative_rate: number;
      confusion_matrix: {
        true_negatives: number;
        false_positives: number;
        false_negatives: number;
        true_positives: number;
      };
    };
    feature_importances: Record<string, number>;
    feature_names: string[];
    limitations: string[];
  };
}

