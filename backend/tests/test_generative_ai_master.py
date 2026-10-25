import pytest
import os
import json
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_training_service import AITrainingService
from app.services.ai_service import AIService
from app.database import SessionLocal
from app.models.audit import SystemSetting

client = TestClient(app)

def test_training_dataset_compilation():
    """Verify that 19 master reference sheets compile into Gemini SFT, Alpaca, and in-context datasets."""
    res = AITrainingService.build_training_dataset()
    assert res["status"] == "DATASET_COMPILED"
    assert res["total_training_pairs"] >= 8

    # Verify Gemini SFT file
    gemini_file = os.path.join(AITrainingService.TRAINING_DIR, "gemini_finetune_dataset.jsonl")
    assert os.path.exists(gemini_file)
    with open(gemini_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) >= 8
        first_ex = json.loads(lines[0])
        assert "systemInstruction" in first_ex
        assert "messages" in first_ex
        assert first_ex["messages"][0]["role"] == "user"
        assert first_ex["messages"][1]["role"] == "model"

    # Verify Alpaca format file
    alpaca_file = os.path.join(AITrainingService.TRAINING_DIR, "alpaca_instruct_dataset.json")
    assert os.path.exists(alpaca_file)
    with open(alpaca_file, "r", encoding="utf-8") as f:
        alpaca_data = json.load(f)
        assert len(alpaca_data) >= 8
        assert "instruction" in alpaca_data[0]
        assert "input" in alpaca_data[0]
        assert "output" in alpaca_data[0]

    # Verify In-Context Exemplar file
    exemplar_file = os.path.join(AITrainingService.TRAINING_DIR, "in_context_exemplars.json")
    assert os.path.exists(exemplar_file)
    exemplars = AITrainingService.get_in_context_exemplars(3)
    assert len(exemplars) == 3
    assert "query" in exemplars[0]
    assert "answer" in exemplars[0]
    assert "status" in exemplars[0]

def test_ai_config_endpoint_and_persistence():
    """Verify reading and updating AI model configuration via Admin API."""
    # Read initial config
    res = client.get("/api/v1/admin/ai-config")
    assert res.status_code == 200
    data = res.json()
    assert "active_model" in data
    assert "supported_models" in data
    assert any(m["id"] == "gemini-2.5-flash" for m in data["supported_models"])

    # Update config to gemini-2.5-flash with a test mock key
    update_res = client.post("/api/v1/admin/ai-config", json={
        "model_name": "gemini-2.5-flash",
        "api_key": "AIzaSy_TEST_KEY_NESFIC_2026"
    })
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "CONFIG_UPDATED"

    # Verify masked key
    get_res = client.get("/api/v1/admin/ai-config")
    assert get_res.json()["has_api_key"] is True
    assert get_res.json()["masked_api_key"].startswith("AIzaSy")

def test_training_evaluation_benchmark_runner():
    """Verify execution of deterministic evaluation benchmark cases against active model."""
    res = client.post("/api/v1/admin/run-training-eval")
    assert res.status_code == 200
    data = res.json()
    assert data["total_cases"] >= 8
    assert data["passed"] >= 8
    assert data["accuracy_percentage"] == "100.0%"
    assert len(data["results"]) >= 8
    for case in data["results"]:
        assert case["is_pass"] is True
        assert case["actual_status"] == case["expected_status"]
