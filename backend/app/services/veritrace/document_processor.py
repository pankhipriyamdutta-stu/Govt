import os
import re
import uuid
import time
import shutil
from typing import Dict, Any, List, Optional, Tuple
from app.services.veritrace.hashing_service import HashingService
from app.services.veritrace.ocr_service import OCRService

# Maximum upload limit: 25MB
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024

SUPPORTED_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".tiff": "image/tiff",
    ".tif": "image/tiff"
}

MAGIC_SIGNATURES = [
    (b"%PDF", "application/pdf"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"II*\x00", "image/tiff"),
    (b"MM\x00*", "image/tiff")
]

class DocumentProcessor:
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Strips path traversal elements and normalizes filename."""
        base = os.path.basename(filename or "uploaded_document")
        clean = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", base)
        return clean or "document"

    @classmethod
    def validate_file(cls, filename: str, content: bytes) -> Tuple[bool, Optional[str], str]:
        """
        Validates file size, extension, and binary magic bytes.
        Returns: (is_valid, error_message, detected_mime_type)
        """
        if len(content) == 0:
            return False, "File is empty (0 bytes).", "application/octet-stream"

        if len(content) > MAX_FILE_SIZE_BYTES:
            return False, f"File exceeds maximum size limit of {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB.", "application/octet-stream"

        ext = os.path.splitext(filename)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            return False, f"Unsupported file extension '{ext}'. Supported: PDF, PNG, JPG, JPEG, TIFF.", "application/octet-stream"

        # Check binary magic signature
        matched_mime = None
        for magic, mime in MAGIC_SIGNATURES:
            if content.startswith(magic):
                matched_mime = mime
                break

        if not matched_mime:
            return False, "File signature does not match expected binary format (corrupted or disguised file).", "application/octet-stream"

        expected_mime = SUPPORTED_EXTENSIONS[ext]
        if expected_mime != matched_mime and not (ext in [".jpg", ".jpeg"] and matched_mime == "image/jpeg"):
            return False, f"File extension '{ext}' does not match real content signature '{matched_mime}'.", matched_mime

        return True, None, matched_mime

    @classmethod
    def save_uploaded_file(cls, storage_dir: str, filename: str, content: bytes) -> Dict[str, Any]:
        """
        Securely stores file on disk with random server-generated filename.
        Calculates SHA-256 and SHA-512 hashes.
        Treats file as untrusted input.
        """
        os.makedirs(storage_dir, exist_ok=True)
        doc_uuid = f"VT-DOC-{uuid.uuid4().hex[:12].upper()}"
        ext = os.path.splitext(filename)[1].lower()
        safe_server_filename = f"{doc_uuid}_{int(time.time())}{ext}"
        storage_path = os.path.join(storage_dir, safe_server_filename)

        with open(storage_path, "wb") as f:
            f.write(content)

        sha256_hash = HashingService.calculate_sha256(storage_path)
        sha512_hash = HashingService.calculate_sha512(storage_path)

        # Explicit malware scanning statement
        malware_scan_status = "NOT_PERFORMED"
        malware_scan_details = "Malware scanning not performed (no external scanner configured)"

        return {
            "document_id": doc_uuid,
            "original_filename": cls.sanitize_filename(filename),
            "storage_path": storage_path,
            "file_size_bytes": len(content),
            "sha256_hash": sha256_hash,
            "sha512_hash": sha512_hash,
            "malware_scan_status": malware_scan_status,
            "malware_scan_details": malware_scan_details
        }

    @classmethod
    def extract_document_content(cls, storage_path: str, file_type: str) -> Dict[str, Any]:
        """
        Module Two: Document Extraction.
        Extracts text, page count, embedded images count, and entities.
        Uses PyMuPDF (fitz) for digital PDFs, and OCR fallback for scanned pages or images.
        """
        extracted_text = ""
        page_count = 0
        ocr_used = False
        text_extraction_method = "direct_binary"
        embedded_images_count = 0
        warnings: List[str] = []
        status = "COMPLETED"

        if file_type == "application/pdf":
            try:
                import pymupdf

                doc = pymupdf.open(storage_path)
                page_count = len(doc)
                pages_text = []

                for page_idx in range(page_count):
                    page = doc[page_idx]
                    p_text = page.get_text("text").strip()
                    pages_text.append(p_text)
                    images = page.get_images(full=True)
                    embedded_images_count += len(images)

                doc.close()
                combined_text = "\n\n".join(pages_text).strip()

                if len(combined_text) > 50:
                    extracted_text = combined_text
                    text_extraction_method = "pdf_text_extraction"
                    ocr_used = False
                else:
                    # Scanned PDF with minimal digital text: run OCR fallback on first pages
                    warnings.append("Digital text sparse or absent. Engaging OCR scan on rendered pages.")
                    ocr_used = True
                    text_extraction_method = "ocr_rendered_pages"
                    
                    doc = pymupdf.open(storage_path)
                    ocr_chunks = []
                    # Process first 3 pages for responsive speed
                    max_scan_pages = min(3, len(doc))
                    for i in range(max_scan_pages):
                        page = doc[i]
                        pix = page.get_pixmap(dpi=150)
                        temp_png = f"{storage_path}_p{i}.png"
                        try:
                            pix.save(temp_png)
                            ocr_res = OCRService.perform_ocr_on_image(temp_png)
                            if ocr_res.get("success") and ocr_res.get("text"):
                                ocr_chunks.append(ocr_res["text"])
                        finally:
                            if os.path.exists(temp_png):
                                try:
                                    os.remove(temp_png)
                                except Exception:
                                    pass
                    doc.close()
                    extracted_text = "\n\n".join(ocr_chunks).strip()
            except Exception as e:
                status = "FAILED"
                warnings.append(f"PDF extraction error: {str(e)}")
        else:
            # Direct Image OCR (PNG / JPG / TIFF)
            page_count = 1
            ocr_used = True
            text_extraction_method = "image_ocr"
            ocr_res = OCRService.perform_ocr_on_image(storage_path)
            if ocr_res.get("success"):
                extracted_text = ocr_res.get("text", "")
            else:
                warnings.append(ocr_res.get("warning") or "OCR failed on image")

        # Extract structured entities
        entities = cls.extract_entities(extracted_text)

        return {
            "extraction_status": status,
            "page_count": page_count,
            "embedded_images_count": embedded_images_count,
            "ocr_used": ocr_used,
            "text_extraction_method": text_extraction_method,
            "extracted_text": extracted_text,
            "extracted_entities": entities,
            "warnings": warnings
        }

    @staticmethod
    def extract_entities(text: str) -> List[Dict[str, str]]:
        """Extracts structured entities: Names, Dates, Organizations, IDs, Monetary amounts, URLs."""
        if not text:
            return []

        entities = []
        
        # 1. Dates
        date_patterns = [
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{4}\b",
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b"
        ]
        for pattern in date_patterns:
            for match in re.findall(pattern, text, re.IGNORECASE):
                entities.append({"type": "DATE", "value": match})

        # 2. Document Identifiers / Gazettes / Notifications
        id_patterns = [
            r"\b(?:No\.|Ref\.|Order No\.|Act No\.|Notification No\.)\s*[:\-]?\s*([A-Za-z0-9_\-\.\/]+)\b",
            r"\b[A-Z]{2,4}/(?:[A-Z0-9\-_]+/)+\d{4}\b"
        ]
        for pattern in id_patterns:
            for match in re.findall(pattern, text, re.IGNORECASE):
                val = match if isinstance(match, str) else match[0]
                entities.append({"type": "DOCUMENT_ID", "value": val.strip()})

        # 3. Monetary Amounts
        money_matches = re.findall(r"(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:lakh|crore|thousand|billion|million))?", text, re.IGNORECASE)
        for m in money_matches:
            entities.append({"type": "MONETARY_VALUE", "value": m.strip()})

        # 4. URLs
        url_matches = re.findall(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+", text)
        for u in url_matches:
            entities.append({"type": "URL", "value": u.strip()})

        # 5. Organizations & Authorities
        org_patterns = [
            r"Government of [A-Z][a-zA-Z\s]+",
            r"Ministry of [A-Z][a-zA-Z\s]+",
            r"Department of [A-Z][a-zA-Z\s]+",
            r"[A-Z][a-zA-Z\s]+ Directorate",
            r"[A-Z][a-zA-Z\s]+ Municipal Corporation",
            r"[A-Z][a-zA-Z\s]+ University"
        ]
        for pattern in org_patterns:
            for match in re.findall(pattern, text):
                cleaned = match.strip()
                if len(cleaned) < 60:
                    entities.append({"type": "ORGANIZATION", "value": cleaned})

        # Deduplicate while preserving order
        seen = set()
        unique_entities = []
        for e in entities:
            key = (e["type"], e["value"].lower())
            if key not in seen:
                seen.add(key)
                unique_entities.append(e)

        return unique_entities[:35]
