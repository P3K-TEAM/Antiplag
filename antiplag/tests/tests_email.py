from django.test import TestCase
from django.conf import settings
from django.test import Client
from environ import Env

# Create your tests here.


class EmailTestCase(TestCase):
    def test_invalid_email(self):
        """Verify that an invalid email returns correct error message"""
        c = Client()
        response = c.post(
            "/api/submissions/",
            {"email": "invalid", "text": "This is my text"},
            content_type="application/json",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error":"Unrecognized email address format."}',
        )
        self.assertEqual(response.status_code, 400)

    def test_valid_email(self):
        """Verify that a valid email passes through validation"""
        c = Client()

        response = c.post(
            "/api/submissions/",
            {"email": "test@gmail.com", "text": "This is my text"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_no_email(self):
        """Verify that a no email passes through validation"""
        c = Client()

        response = c.post(
            "/api/submissions/",
            {"text": "This is my text"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_email_API_key(self):
        """Verify that some Api key is set for mail sending"""
        env = Env(DEBUG=(bool, False))
        env.read_env(".env")
        print(env("SENDGRID_API_KEY"))
        print(env("DJANGO_SECRET_KEY"))
        self.assertNotEqual(settings.EMAIL_HOST_PASSWORD, "")
