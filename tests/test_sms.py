from django.test import TestCase
from backend.apps.notifications.sms import send_sms


class SmsTests(TestCase):
    def test_sms_mock(self):
        ok = send_sms('+242060000000', 'Test')
        assert ok is True
