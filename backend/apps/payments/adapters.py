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


class MTNMoMoCGAdapter(ProviderAdapter):
    """Intégration simplifiée MTN Mobile Money (Congo-Brazzaville).
    Mode maquette si les clés ne sont pas fournies.
    Variables d'env attendues:
    - MTN_MOMO_BASE_URL (par ex. https://sandbox.momodeveloper.mtn.com)
    - MTN_MOMO_SUBSCRIPTION_KEY
    - MTN_MOMO_API_USER
    - MTN_MOMO_API_KEY
    - MTN_MOMO_TARGET_ENV (sandbox|production)
    - MTN_MOMO_CURRENCY (par défaut XAF)
    """
    def __init__(self):
        self.base_url = os.getenv('MTN_MOMO_BASE_URL', 'https://sandbox.momodeveloper.mtn.com')
        self.sub_key = os.getenv('MTN_MOMO_SUBSCRIPTION_KEY', '')
        self.api_user = os.getenv('MTN_MOMO_API_USER', '')
        self.api_key = os.getenv('MTN_MOMO_API_KEY', '')
        self.target_env = os.getenv('MTN_MOMO_TARGET_ENV', 'sandbox')
        self.currency = os.getenv('MTN_MOMO_CURRENCY', os.getenv('CURRENCY', 'XAF'))
        self.mock = not (self.sub_key and self.api_user and self.api_key)

    def create_payment_intent(self, order) -> ProviderResult:
        ref = f"MOMO-{uuid.uuid4().hex[:10].upper()}"
        if self.mock:
            logger.info('Create MTN MoMo (mock) intent', extra={'order_id': order.id, 'reference': ref})
            return ProviderResult(reference=ref, checkout_url='', raw={'mock': True, 'reference': ref})
        # En implémentation réelle, appeler l'API Collections: RequestToPay (RTP)
        # Ici on journalise et renvoie une référence, le statut sera récupéré côté webhook/polling.
        logger.info('Create MTN MoMo intent', extra={'order_id': order.id, 'reference': ref, 'amount': str(order.total_amount), 'currency': order.currency})
        return ProviderResult(reference=ref, checkout_url='', raw={'reference': ref})

    def verify_webhook(self, payload, headers):
        # Pour le sandbox, on peut faire simple; en prod: vérifier l'authentification/headers
        return payload

    def fetch_status(self, reference: str):
        # Maquette: succès automatique
        return {'reference': reference, 'status': 'SUCCEEDED'}
