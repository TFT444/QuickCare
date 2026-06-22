import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_single_medication_returns_no_interactions():
    from src.core.drug_checker import check
    result = await check(["Paracetamol"])
    assert result["interactions"] == []


@pytest.mark.asyncio
async def test_multiple_medications_calls_ai():
    from src.core.drug_checker import check
    with patch("src.core.drug_checker.check_drug_interactions", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = "No significant interactions found.\n\n---\nDisclaimer."
        result = await check(["Warfarin", "Aspirin"], "en")
    mock_ai.assert_called_once()
    assert result["language"] == "en"
