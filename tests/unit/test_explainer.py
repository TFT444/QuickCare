import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_explain_returns_structure():
    from src.prescriptions.explainer import explain_prescription
    with patch("src.prescriptions.explainer.ai_explain", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = "Take one tablet daily.\n\n---\nGuidance only."
        result = await explain_prescription("Amlodipine 5mg once daily", "en")
    assert "explanation" in result
    assert "medications" in result
    assert "disclaimer" in result
    assert result["language"] == "en"


@pytest.mark.asyncio
async def test_empty_text_raises():
    from src.prescriptions.explainer import explain_prescription
    with pytest.raises(ValueError):
        await explain_prescription("", "en")
