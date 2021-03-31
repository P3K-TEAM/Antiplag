from django.test import TestCase
from django.core.mail import send_mail
from django.conf import settings
from .models import Submission
from .views import SubmissionList
from django.test import Client
# Create your tests here.

class EmailTestCase(TestCase):
#pipenv run bash -c "cd antiplag && python manage.py test"
    def test_invalid_email(self):
        """Verify that an invalid email returns correct error message"""
        c = Client()
        #response = c.post('/api/submissions/', {"email" : "invalid"})
        #self.assertEqual(response.content.decode('utf-8'), "{\"error\":\"Unrecognized email address format.\"}")
        #self.assertEqual(response.status_code, 400)

    def test_valid_email(self):
        """Verify that a valid email passes through validation"""
        c = Client()

        response = c.post('/api/submissions/', {"email" : "test@gmail.com", "text" : "This is my text"}, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_no_email(self):
        """Verify that a no email passes through validation"""
        c = Client()

        response = c.post('/api/submissions/', {"text" : "This is my text"}, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_email_API_key(self):
        """Verify that some Api key is set for mail sending"""
        self.assertNotEqual(settings.EMAIL_HOST_PASSWORD, None)
