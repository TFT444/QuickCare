import logging

logger = logging.getLogger(__name__)


async def send_push_notification(user_id: str, message: str, language: str = "en") -> bool:
    # Stub — integrate with FCM or Azure Notification Hubs in Phase 2
    logger.info("Push notification to user %s [%s]: %s", user_id, language, message[:80])
    return True
