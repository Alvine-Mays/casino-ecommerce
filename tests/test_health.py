from django.test import TestCase, Client


class HealthEndpointTests(TestCase):
    """Tests unitaires simples pour l'endpoint de santé.
    Vérifie qu'un GET /api/health/ renvoie 200 et {"status":"ok"}.
    """
    def test_health_ok(self):
        client = Client()
        resp = client.get('/api/health/')
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
