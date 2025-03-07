"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from environ import Env
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


def require_env(name):
    """Raise an error if the environment variable isn't defined"""
    value = env(name)
    if value is None or "":
        raise ImproperlyConfigured(
            f'Required environment variable "{name}" is not set.'
        )
    return value


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env(DEBUG=(bool, False))
env.read_env(".env")

DEBUG = require_env("DEBUG")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Unique secret can be generated as `base64 /dev/urandom | head -c50`
SECRET_KEY = require_env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = ["www.antiplag.sk", "antiplag.sk", "localhost", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_elasticsearch_dsl",
    # Our apps
    "antiplag",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("http://localhost:8080",)

ROOT_URLCONF = "django_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.db()}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "antiplag",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en-us", _("English")),
    ("sk", _("Slovak")),
]

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = "Europe/Bratislava"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "files"
MEDIA_URL = "/files/"

# Celery configuration
CELERY_BROKER_URL = require_env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = require_env("CELERY_RESULT_BACKEND")
CELERY_RESULT_PERSISTENT = require_env("CELERY_RESULT_PERSISTENT")

# Elasticsearch config
ELASTICSEARCH_DSL = {
    "default": {"hosts": require_env("ELASTIC_HOST")},
}

TESSERACT_PATH = require_env("TESSERACT_PATH")

# Set max file size in requests in MB
MAX_FILE_SIZE = 20

# Set max files in a request
MAX_FILES_PER_REQUEST = 50

# Minimal string length considered similarity
MIN_SIMILARITY_LENGTH = 50

# Ignore similarities below this value
SIMILARITY_THRESHOLD = 0.15

# Email settings, service provider SendGrid
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = require_env("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
