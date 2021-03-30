from django.test import TestCase
from django.core.mail import send_mail
from django.conf import settings
# Create your tests here.

class EmailTestCase(TestCase):

    def test_API_key(self):
        """Verify that some Api key is set for mail sending"""
        self.assertNotEqual(settings.EMAIL_HOST_PASSWORD, None)
