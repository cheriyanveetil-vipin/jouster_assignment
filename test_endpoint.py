import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import db
from main import app

client = TestClient(app)
TEST_DB_FILE = "test_analysis.db"

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    db.DB_FILE = TEST_DB_FILE
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    db.init_db()
    db.insert_analysis(
        summary="summary 1",
        title="Sample Title 1",
        topics=",".join(["topic1", "topic2"]),
        sentiment="positive",
        keywords=",".join(["key1", "key2"])
    )
    db.insert_analysis(
        summary="Summary 2",
        title="Sample Title 2",
        topics=",".join(["topic2", "topic3"]),
        sentiment="neutral",
        keywords=",".join(["key2", "key3"])
    )
    yield
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)



class TestAnalyzeEndpoint:

    def test_analyze_success(self):
        payload = {"text": "Some sample text for testing."}
        with patch("main.analyze_text", return_value={
                        "summary": "Mocked summary for testing.",
                        "structured_data": {
                            "title": "Mocked Title",
                            "topics": ["mock1", "mock2", "mock3"],
                            "sentiment": "positive"
                        }
                    }):
            response = client.post("/analyze", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Mocked summary for testing."
        assert data["title"] == "Mocked Title"
        assert data["topics"] == ["mock1", "mock2", "mock3"]
        assert data["sentiment"] == "positive"
        assert "keywords" in data

    def test_analyze_missing_text(self):
        response = client.post("/analyze", json={})
        data = response.json()
        assert response.status_code == 422  # Pydantic validation error
        assert any("Field required" in err["msg"] for err in data["detail"])

    def test_analyze_empty_text(self):
        response = client.post("/analyze", json={"text": "   "})
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]



class TestSearchEndpoint:

    def test_search_topic1(self):
        response = client.get("/search?topic=topic1")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Sample Title 1"

    def test_search_topic2(self):
        response = client.get("/search?topic=topic2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 2

    def test_search_topic3(self):
        response = client.get("/search?topic=topic3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Sample Title 2"

    def test_search_empty_topic(self):
        response = client.get("/search?topic=   ")
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]
