import logging
import os

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, html: str) -> bool:
    api_key = os.getenv('BREVO_API_KEY')
    sender = os.getenv('BREVO_SENDER', 'no-reply@example.com')
    if not api_key:
        logger.info('[MOCK EMAIL] to=%s subject=%s', to_email, subject)
        return True
    # TODO: Implement Brevo/Sendinblue API call
    logger.info('[SIMULATED EMAIL] to=%s subject=%s', to_email, subject)
    return True
