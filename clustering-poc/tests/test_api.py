import pandas as pd
from pathlib import Path
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_topics_endpoint(tmp_path, monkeypatch):
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    df = pd.DataFrame({"Topic": [0], "Count": [2], "Name": ["Support Issues"]})
    df.to_csv(output_dir / "topic_info.csv", index=False)

    monkeypatch.setattr("app.api.OUTPUT_DIR", output_dir)

    response = client.get("/topics")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["Topic"] == 0

def test_documents_endpoint(tmp_path, monkeypatch):
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    df = pd.DataFrame({"Document": ["test"], "Topic": [0]})
    df.to_csv(output_dir / "document_info.csv", index=False)

    monkeypatch.setattr("app.api.OUTPUT_DIR", output_dir)

    response = client.get("/documents")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["Topic"] == 0
