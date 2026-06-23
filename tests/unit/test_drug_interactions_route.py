import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport


@pytest.fixture
def app():
    from src.api.main import app as fastapi_app
    return fastapi_app


@pytest.mark.asyncio
async def test_single_medication_returns_no_interactions(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/drug-interactions/check",
            json={"medications": ["Paracetamol"], "language": "en"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["medications"] == ["Paracetamol"]
    assert data["interactions_detected"] is False


@pytest.mark.asyncio
async def test_multiple_medications_calls_checker(app):
    mock_result = {
        "medications": ["Warfarin", "Aspirin"],
        "language": "en",
        "guidance": "Warfarin and Aspirin together increase bleeding risk.\n\n---\nThis information is for guidance only. Always consult your pharmacist or GP for medical advice.",
        "interactions": [],
    }
    with patch("src.core.drug_checker.check", new_callable=AsyncMock, return_value=mock_result):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/drug-interactions/check",
                json={"medications": ["Warfarin", "Aspirin"], "language": "en"},
            )
    assert response.status_code == 200
    data = response.json()
    assert data["interactions_detected"] is True
    assert data["language"] == "en"
    assert "Warfarin" in data["medications"]


@pytest.mark.asyncio
async def test_urdu_language_accepted(app):
    mock_result = {
        "medications": ["Metformin", "Lisinopril"],
        "language": "ur",
        "guidance": "ان دوائوں کو ایک ساتھ لینے سے پہلے ڈاکٹر سے مشورہ کریں۔\n\n---\nیہ معلومات صرف رہنمائی کے لیے ہے۔",
        "interactions": [],
    }
    with patch("src.core.drug_checker.check", new_callable=AsyncMock, return_value=mock_result):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/drug-interactions/check",
                json={"medications": ["Metformin", "Lisinopril"], "language": "ur"},
            )
    assert response.status_code == 200
    assert response.json()["language"] == "ur"
