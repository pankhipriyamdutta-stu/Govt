import re
import uuid
from typing import List, Dict, Any, Optional

class ClaimExtractor:
    """
    Module Five: Claim Extraction.
    Extracts structured factual claims from document text.
    Identifies subject, predicate, object, and full claim sentence.
    """

    PATTERNS = [
        # 1. Statutory enactment & establishment
        (
            r"([A-Z][a-zA-Z\s]{2,40})\s+(?:was|is)\s+(?:established|enacted|passed|instituted|founded)\s+in\s+(\d{4})",
            "established_in"
        ),
        # 2. Section references and provisions
        (
            r"Section\s+(\d+[A-Z]?)\s+of\s+(?:the\s+)?([A-Z][a-zA-Z\s]{3,40}(?:Act|Rules|Regulations|Code),?\s+\d{4})\s+(?:provides|mandates|stipulates|specifies)\s+([^.,;\n]{10,120})",
            "stipulates_provision"
        ),
        # 3. Appointments and designations
        (
            r"([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:,\s*[A-Z]{2,4})?)\s+(?:is|was|has been)\s+appointed\s+as\s+([A-Za-z\s]{5,50})\s+(?:under|in|for)\s+([A-Za-z\s]{3,50})",
            "appointed_as"
        ),
        # 4. Effective dates and notifications
        (
            r"(?:The\s+)?([A-Z][a-zA-Z\s]{3,50})\s+(?:shall\s+come|came)\s+into\s+force\s+on\s+([0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+,?\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            "effective_date_is"
        ),
        # 5. Financial allocation / budgets / fees
        (
            r"([A-Za-z\s]{4,40})\s+(?:allocated|sanctioned|granted|prescribes\s+a\s+fee\s+of)\s+(?:an\s+amount\s+of\s+)?((?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:crore|lakh|thousand))?)\s+for\s+([A-Za-z\s]{4,60})",
            "financial_allocation"
        ),
        # 6. Jurisdiction & Powers
        (
            r"([A-Za-z\s]{4,40})\s+(?:has\s+jurisdiction\s+over|shall\s+extend\s+to)\s+(?:the\s+whole\s+of\s+)?([A-Za-z\s]{3,50})",
            "jurisdiction_extends_to"
        )
    ]

    @classmethod
    def extract_claims(cls, text: str) -> List[Dict[str, Any]]:
        """
        Parses document text into atomic factual claims.
        Returns list of structured claim dictionaries:
        { claim_id, claim_text, subject, predicate, object }
        """
        if not text:
            return []

        claims: List[Dict[str, Any]] = []
        seen_texts = set()

        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)

        for sentence in sentences:
            sentence_clean = sentence.strip().replace("\n", " ")
            if len(sentence_clean) < 25 or len(sentence_clean) > 350:
                continue

            matched = False
            for pattern, predicate_name in cls.PATTERNS:
                m = re.search(pattern, sentence_clean, re.IGNORECASE)
                if m:
                    groups = m.groups()
                    subject = groups[0].strip() if len(groups) > 0 else "Document Subject"
                    obj = groups[1].strip() if len(groups) > 1 else ""
                    if len(groups) > 2:
                        obj = f"{obj} ({groups[2].strip()})"

                    if sentence_clean not in seen_texts:
                        seen_texts.add(sentence_clean)
                        claims.append({
                            "claim_id": f"CLM-{uuid.uuid4().hex[:8].upper()}",
                            "claim_text": sentence_clean,
                            "subject": subject,
                            "predicate": predicate_name,
                            "object": obj
                        })
                        matched = True
                        break

            # General fallback for prominent statutory / official declarations
            if not matched and any(k in sentence_clean for k in ["Section", "Notification No", "Government of Assam", "hereby declares", "Gazette", "Act, 20"]):
                if len(claims) < 8 and sentence_clean not in seen_texts:
                    seen_texts.add(sentence_clean)
                    # Extract rough subject
                    words = sentence_clean.split()
                    subj = " ".join(words[:4])
                    claims.append({
                        "claim_id": f"CLM-{uuid.uuid4().hex[:8].upper()}",
                        "claim_text": sentence_clean,
                        "subject": subj,
                        "predicate": "asserts",
                        "object": " ".join(words[4:15]) if len(words) > 4 else ""
                    })

        return claims[:10]
