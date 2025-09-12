import logging
import os

logger = logging.getLogger(__name__)


def send_sms(phone: str, message: str) -> bool:
    api_key = os.getenv('AFRICASTALKING_API_KEY')
    sender = os.getenv('AFRICASTALKING_SENDER', 'GCCasino')
    if not api_key:
        logger.info('[MOCK SMS] to=%s sender=%s msg=%s', phone, sender, message)
        return True
    # TODO: Implement real Africa's Talking integration
    logger.info('[SIMULATED SMS] to=%s sender=%s msg=%s', phone, sender, message)
    return True
