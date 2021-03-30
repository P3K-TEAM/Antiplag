from django.test import TestCase
from django.core.mail import send_mail
from django.conf import settings
# Create your tests here.

class EmailTestCase(TestCase):

    def test_sending(self):
        """Verify that send_mail function works"""
        self.assertEqual(send_mail('testing', 'my message', 'hello@mydomain.com', ['personal@example.com'], fail_silently=False), 1)

    def test_API_key(self):
        """Verify that some Api key is set for mail sending"""
        self.assertNotEqual(settings.EMAIL_HOST_PASSWORD, None)
