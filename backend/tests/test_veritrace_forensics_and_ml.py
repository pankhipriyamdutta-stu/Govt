import pytest
import io
import os
import numpy as np
from fastapi.testclient import TestClient
from app.main import app
from app.services.veritrace.visual_forensics import VisualForensicsService
from app.services.veritrace.fraud_detection import FraudDetectionMLService
from app.services.veritrace.forensic_service import ForensicService

client = TestClient(app)

def test_visual_forensics_clean_synthetic_image():
    import cv2
    # Create clean synthetic image
    img = np.ones((120, 120, 3), dtype=np.uint8) * 245
    cv2.putText(img, "OFFICIAL GAZETTE", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (10, 10, 10), 1)
    
    test_img_path = "test_clean_img.png"
    try:
        cv2.imwrite(test_img_path, img)
        res = VisualForensicsService.analyze_image_tampering(test_img_path)
        assert res["evaluated"] is True
        assert res["visual_tampering_score"] < 0.35
        assert res["verdict"] == "NATURAL_COMPRESSION_CONSISTENT"
    finally:
        if os.path.exists(test_img_path):
            os.remove(test_img_path)

def test_fraud_ml_feature_extraction():
    feats = FraudDetectionMLService.extract_features(
        metadata_anomalies_count=1,
        structural_revisions_count=0,
        visual_tamper_score=0.15,
        ocr_confidence=0.95,
        has_signature=True,
        page_count=2,
        text_length=1500
    )
    assert "feat_metadata_anomaly_score" in feats
    assert "feat_visual_tamper_score" in feats
    assert feats["feat_signature_present"] == 1.0
    assert feats["feat_ocr_confidence"] == 0.95

def test_fraud_ml_evaluation_reference_match():
    feats = FraudDetectionMLService.extract_features(0, 0, 0.05, 0.98, True, 1, 1000)
    res = FraudDetectionMLService.evaluate_fraud_risk(feats, has_signature=True, ref_hash_matches=True)
    assert res["fraud_probability"] <= 0.05
    assert res["anomaly_verdict"] == "REFERENCE_INTEGRITY_VERIFIED"
    assert "precision" in res["evaluation_metrics"]
    assert res["evaluation_metrics"]["precision"] >= 0.90

def test_fraud_ml_evaluation_high_anomaly():
    feats = FraudDetectionMLService.extract_features(3, 4, 0.85, 0.40, False, 1, 500)
    res = FraudDetectionMLService.evaluate_fraud_risk(feats, has_signature=False, ref_hash_matches=False)
    assert res["fraud_probability"] >= 0.60
    assert res["anomaly_verdict"] == "HIGH_ANOMALY_FRAUD_INDICATORS"
    assert res["is_outlier"] is True

def create_valid_test_pdf(text: str = "Official Gazette Verification Record") -> bytes:
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((50, 72), text, fontsize=12)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def test_end_to_end_document_analysis_pipeline():
    # 1. Upload a document containing text
    sample_pdf = create_valid_test_pdf("The Assam Right to Public Services Act was enacted in 2012 by Dispur.")

    upload_res = client.post(
        "/api/v1/veritrace/upload",
        files={"file": ("pipeline_test.pdf", io.BytesIO(sample_pdf), "application/pdf")},
        data={"uploaded_by": "lead_forensic_examiner"}
    )
    assert upload_res.status_code == 200
    doc_id = upload_res.json()["document_id"]

    # 2. Trigger pipeline analysis
    analysis_res = client.post(f"/api/v1/veritrace/documents/{doc_id}/analyze")
    assert analysis_res.status_code == 200
    data = analysis_res.json()
    assert data["status"] == "ANALYSIS_COMPLETED"
    assert "executive_verdict" in data
    assert data["executive_verdict"]["verdict"] in ["LOW", "MODERATE", "HIGH", "INSUFFICIENT_DATA"]

    # 3. Check forensics endpoint
    forensics_res = client.get(f"/api/v1/veritrace/documents/{doc_id}/forensics")
    assert forensics_res.status_code == 200
    f_data = forensics_res.json()
    assert "findings" in f_data
    assert len(f_data["findings"]) > 0

    # 4. Check report endpoint
    report_res = client.get(f"/api/v1/veritrace/documents/{doc_id}/report")
    assert report_res.status_code == 200
    r_data = report_res.json()
    assert "document_summary" in r_data
    assert "executive_verdict" in r_data
    assert "independent_dimensions" in r_data
