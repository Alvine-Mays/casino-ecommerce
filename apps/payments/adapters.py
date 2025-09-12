import os
import uuid
import logging
from dataclasses import dataclass
from typing import Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class ProviderResult:
    reference: str
    checkout_url: str
    raw: Dict[str, Any]


class ProviderAdapter:
    def create_payment_intent(self, order) -> ProviderResult:
        raise NotImplementedError

    def verify_webhook(self, payload: Dict[str, Any], headers: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def fetch_status(self, reference: str) -> Dict[str, Any]:
        raise NotImplementedError


class CinetPayAdapter(ProviderAdapter):
    def __init__(self):
        self.api_key = os.getenv('PAYMENT_CINETPAY_API_KEY', '')
        self.api_secret = os.getenv('PAYMENT_CINETPAY_API_SECRET', '')
        self.base_url = os.getenv('PAYMENT_CINETPAY_BASE_URL', 'https://api-checkout.cinetpay.com')
        self.mock = not (self.api_key and self.api_secret)

    def create_payment_intent(self, order) -> ProviderResult:
        ref = f"MVP-{uuid.uuid4().hex[:10].upper()}"
        checkout_url = f"{os.getenv('SITE_BASE_URLS', '')}"  # front will handle redirect/mock
        raw = {'mock': True, 'reference': ref}
        logger.info('Create CinetPay intent', extra={'order_id': order.id, 'reference': ref})
        return ProviderResult(reference=ref, checkout_url=checkout_url, raw=raw)

    def verify_webhook(self, payload, headers):
        # In mock mode, trust payload
        return payload

    def fetch_status(self, reference: str):
        return {'reference': reference, 'status': 'SUCCEEDED'}
