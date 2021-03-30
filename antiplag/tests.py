from django.test import TestCase
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from .models import Submission
from .views import SubmissionList
from django.test import Client
# Create your tests here.

class EmailTestCase(TestCase):
    def test_invalid_email(self):
        """Verify that an invalid email returns correct error message"""
        c = Client()
        response = c.post('/api/submissions/', {"email" : "invalid"})
        self.assertEqual(response.content.decode('utf-8'), "{\"error\":\"Unrecognized email address format.\"}")
        self.assertEqual(response.status_code, 400)

    def test_valid_email(self):
        """Verify that a valid email passes through validation"""
        c = Client()
        response = c.post('/api/submissions/', {"email" : "test@gmail.com"})
        self.assertEqual(response.content.decode('utf-8'), "{\"error\":\"No files present.\"}")
        self.assertEqual(response.status_code, 400)

    def test_API_key(self):
        """Verify that some Api key is set for mail sending"""
        self.assertNotEqual(settings.EMAIL_HOST_PASSWORD, None)
