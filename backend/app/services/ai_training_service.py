import os
import json
import csv
from typing import List, Dict, Any
from app.config import settings

class AITrainingService:
    TRAINING_DIR = os.path.join(settings.BASE_DIR, "training_data")

    @classmethod
    def ensure_dir(cls):
        os.makedirs(cls.TRAINING_DIR, exist_ok=True)

    @classmethod
    def build_training_dataset(cls) -> Dict[str, Any]:
        """
        Compiles the master government dataset sheets into standard
        Generative AI training formats:
        1. Google Gemini Supervised Fine-Tuning (SFT) JSONL format
        2. Alpaca / HuggingFace Instruction-Tuning JSON format
        3. Dynamic In-Context Few-Shot Exemplar Store
        """
        cls.ensure_dir()

        eval_csv_path = os.path.join(settings.DATASET_CSV_DIR, "11_AI_Answer_Evaluation_Dataset.csv")
        rag_csv_path = os.path.join(settings.DATASET_CSV_DIR, "10_RAG_Retrieval_Dataset.csv")
        evidence_csv_path = os.path.join(settings.DATASET_CSV_DIR, "08_Evidence_and_Claim_Ledger.csv")

        eval_rows = []
        if os.path.exists(eval_csv_path):
            with open(eval_csv_path, "r", encoding="utf-8-sig", errors="ignore") as f:
                eval_rows = list(csv.DictReader(f))

        evidence_rows = []
        if os.path.exists(evidence_csv_path):
            with open(evidence_csv_path, "r", encoding="utf-8-sig", errors="ignore") as f:
                evidence_rows = list(csv.DictReader(f))

        evidence_by_doc = {}
        for ev in evidence_rows:
            doc_id = ev.get("document_id", "")
            if doc_id not in evidence_by_doc:
                evidence_by_doc[doc_id] = []
            evidence_by_doc[doc_id].append(ev)

        gemini_sft_examples = []
        alpaca_examples = []
        in_context_exemplars = []

        system_instruction = (
            "You are NESFIC-D-36, the Trusted Government Knowledge, Rules & Document Assistant. "
            "You strictly follow the Government Trust Principle: never extrapolate from pretrained memory. "
            "Every answer must be based exclusively on the provided official government context. "
            "Output one of three states:\n"
            "1. STATUS: VERIFIED (Green) - Supported 100% by active, authenticated primary statutory text.\n"
            "2. STATUS: VERIFICATION_REQUIRED (Amber) - Ambiguity, conflict, or vintage anomaly requires human review.\n"
            "3. STATUS: CANNOT_GENERATE (Red) - Evidence missing, expired, quarantined, or ungrounded."
        )

        for row in eval_rows:
            query = row.get("query", "").strip()
            retrieved_docs = row.get("retrieved_documents", "").strip()
            expected_answer = row.get("expected_answer", "").strip()
            expected_claims = row.get("expected_claims", "").strip()
            expected_citations = row.get("expected_citations", "").strip()
            expected_status = row.get("expected_status", "VERIFIED").strip()

            if not query or not expected_answer:
                continue

            # Assemble context from evidence ledger
            doc_key = retrieved_docs.split(" ")[0].strip()
            ev_list = evidence_by_doc.get(doc_key, [])
            context_text = "\n".join([
                f"[{e.get('document_id')}] Section: {e.get('section_number')}\nText: {e.get('exact_evidence_text')}\nHash: {e.get('evidence_hash')}"
                for e in ev_list[:2]
            ])
            if not context_text:
                context_text = f"Official Record: {retrieved_docs}"

            # 1. Gemini Fine-Tuning Format (Multi-Turn Chat Contents)
            user_prompt = f"CONTEXT:\n{context_text}\n\nGOVERNMENT STATUTORY QUERY:\n{query}"
            model_target = (
                f"STATUS: {expected_status}\n\n"
                f"ANSWER:\n{expected_answer}\n\n"
                f"CLAIMS:\n- {expected_claims}\n\n"
                f"CITATIONS:\n- {expected_citations}"
            )

            gemini_sft_examples.append({
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": system_instruction}]
                },
                "messages": [
                    {"role": "user", "content": user_prompt},
                    {"role": "model", "content": model_target}
                ]
            })

            # 2. Alpaca Instruction-Tuning Format
            alpaca_examples.append({
                "instruction": system_instruction,
                "input": user_prompt,
                "output": model_target
            })

            # 3. In-Context Exemplar for Runtime Generative Prompt Conditioning
            in_context_exemplars.append({
                "query": query,
                "context": context_text,
                "status": expected_status,
                "answer": expected_answer,
                "claims": expected_claims,
                "citations": expected_citations
            })

        # Save files to training directory
        gemini_file = os.path.join(cls.TRAINING_DIR, "gemini_finetune_dataset.jsonl")
        with open(gemini_file, "w", encoding="utf-8") as f:
            for ex in gemini_sft_examples:
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")

        alpaca_file = os.path.join(cls.TRAINING_DIR, "alpaca_instruct_dataset.json")
        with open(alpaca_file, "w", encoding="utf-8") as f:
            json.dump(alpaca_examples, f, indent=2, ensure_ascii=False)

        in_context_file = os.path.join(cls.TRAINING_DIR, "in_context_exemplars.json")
        with open(in_context_file, "w", encoding="utf-8") as f:
            json.dump(in_context_exemplars, f, indent=2, ensure_ascii=False)

        return {
            "status": "DATASET_COMPILED",
            "total_training_pairs": len(gemini_sft_examples),
            "formats_generated": [
                "Google Gemini SFT JSONL (gemini_finetune_dataset.jsonl)",
                "Alpaca Instruction JSON (alpaca_instruct_dataset.json)",
                "Dynamic In-Context Conditioning Store (in_context_exemplars.json)"
            ],
            "training_directory": cls.TRAINING_DIR,
            "target_model_architectures": [
                "gemini-2.5-flash",
                "gemini-1.5-flash",
                "gemini-2.0-flash",
                "HuggingFace PEFT / LoRA"
            ]
        }

    @classmethod
    def get_in_context_exemplars(cls, top_n: int = 3) -> List[Dict[str, Any]]:
        """Loads cached in-context few-shot exemplars to condition generative LLM prompts."""
        in_context_file = os.path.join(cls.TRAINING_DIR, "in_context_exemplars.json")
        if not os.path.exists(in_context_file):
            cls.build_training_dataset()

        try:
            with open(in_context_file, "r", encoding="utf-8") as f:
                exemplars = json.load(f)
                return exemplars[:top_n]
        except Exception:
            return []

    @classmethod
    def get_training_status(cls) -> Dict[str, Any]:
        """Returns statistics on training readiness and dataset composition."""
        gemini_file = os.path.join(cls.TRAINING_DIR, "gemini_finetune_dataset.jsonl")
        is_compiled = os.path.exists(gemini_file)
        if not is_compiled:
            res = cls.build_training_dataset()
            pair_count = res["total_training_pairs"]
        else:
            with open(gemini_file, "r", encoding="utf-8") as f:
                pair_count = len(f.readlines())

        return {
            "training_compiled": True,
            "total_training_pairs": pair_count,
            "supervised_fine_tuning_ready": True,
            "in_context_conditioning_active": True,
            "recommended_primary_api": "Google Gemini 2.5 Flash (via google-genai / HTTP v1beta)",
            "sovereign_fallback_active": True,
            "supported_models": [
                {"id": "gemini-2.5-flash", "name": "Google Gemini 2.5 Flash", "type": "Generative AI", "recommended": True},
                {"id": "gemini-1.5-flash", "name": "Google Gemini 1.5 Flash", "type": "Generative AI", "recommended": False},
                {"id": "gemini-2.0-flash", "name": "Google Gemini 2.0 Flash", "type": "Generative AI", "recommended": False},
                {"id": "gemini-2.5-pro", "name": "Google Gemini 2.5 Pro (Deep Reasoning)", "type": "Generative AI", "recommended": False},
                {"id": "local-sovereign", "name": "Sovereign Neural Grounded Reasoner", "type": "Autonomous In-House", "recommended": False}
            ]
        }
