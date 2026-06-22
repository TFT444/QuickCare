import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.fixture
def client():
    with patch("src.api.main.create_async_engine"), \
         patch("src.api.main.aioredis") as mock_redis:
        mock_redis.from_url = AsyncMock(return_value=MagicMock())
        from src.api.main import app
        from fastapi.testclient import TestClient
        with TestClient(app) as c:
            yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_explain_text(client):
    with patch("src.prescriptions.explainer.ai_explain", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = "Take one tablet daily.\n\n---\nGuidance only."
        response = client.post(
            "/prescriptions/explain",
            data={"text": "Metformin 500mg twice daily with meals"},
        )
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert "disclaimer" in data
