import logging
import os
import json
import urllib.request

logger = logging.getLogger(__name__)


def send_sms(phone: str, message: str) -> bool:
    """Envoi d'un SMS via MTN (maquette si variables absentes).
    Variables attendues:
    - MTN_SMS_BASE_URL (ex: https://api.mtn.com/sms) — dépend de l'environnement
    - MTN_SMS_API_KEY (ou MTN_SMS_SUBSCRIPTION_KEY)
    - MTN_SMS_SENDER (SenderID/shortcode si applicable)
    Implémentation minimale: en l'absence de clés, log et renvoie True (mode dev/tests).
    En prod: adapter l'URL/headers selon le partenaire MTN CG.
    """
    base = os.getenv('MTN_SMS_BASE_URL', '')
    api_key = os.getenv('MTN_SMS_API_KEY') or os.getenv('MTN_SMS_SUBSCRIPTION_KEY')
    sender = os.getenv('MTN_SMS_SENDER', 'GCShop')

    if not api_key or not base:
        logger.info('[MOCK MTN SMS] to=%s sender=%s msg=%s', phone, sender, message)
        return True

    try:
        # Exemple générique; à adapter au endpoint MTN effectif.
        url = base.rstrip('/') + '/messages'
        payload = {'from': sender, 'to': phone, 'text': message}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {api_key}')
        with urllib.request.urlopen(req, timeout=10) as resp:
            ok = 200 <= resp.getcode() < 300
            logger.info('MTN SMS sent: %s', ok, extra={'phone': phone, 'status': resp.getcode()})
            return ok
    except Exception as e:
        logger.exception('MTN SMS error: %s', e)
        return False
