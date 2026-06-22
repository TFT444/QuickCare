import os
import httpx
import logging

logger = logging.getLogger(__name__)

NHS_LOGIN_BASE = "https://auth.login.nhs.uk"
CLIENT_ID = os.getenv("NHS_LOGIN_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("NHS_LOGIN_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("NHS_LOGIN_REDIRECT_URI", "")


def get_auth_url(state: str) -> str:
    params = (
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid+profile+nhs_number"
        f"&state={state}"
    )
    return f"{NHS_LOGIN_BASE}/authorize{params}"


async def exchange_code(code: str) -> dict:
    # Stub — full PKCE flow to be implemented in Phase 2
    logger.info("NHS Login token exchange (stub) for code: %s...", code[:8])
    return {"access_token": "stub_token", "nhs_number": "9000000009"}
