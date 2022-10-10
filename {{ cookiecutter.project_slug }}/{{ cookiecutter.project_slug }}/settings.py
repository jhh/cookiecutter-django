import sys
from pathlib import Path

import environ

# 0. Setup

BASE_DIR = Path(__file__).resolve().parent.parent
# {{ cookiecutter.project_slug }}/
APPS_DIR = BASE_DIR / "{{ cookiecutter.project_slug }}"
env = environ.Env()

# Load env vars from .env file if not testing
try:
    command = sys.argv[1]
except IndexError:
    command = "help"

if command != "test":
    env.read_env(str(BASE_DIR / ".env"))

# Django Core Settings
# ------------------------------------------------------------------------------
#    https://docs.djangoproject.com/en/4.1/ref/settings/#core-settings

DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = (
    ["localhost", "0.0.0.0", "127.0.0.1"]
    if DEBUG
    else env.list("DJANGO_ALLOWED_HOSTS", default=["{{ cookiecutter.domain_name }}"])
)

SECRET_KEY = env("DJANGO_SECRET_KEY")

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Detroit"

USE_I18N = True

USE_TZ = True

# Database
DATABASES = {}
DATABASES["default"] = env.db(
    "DATABASE_URL",
    default="postgres:///{{cookiecutter.project_slug}}",
)  # noqa F405
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int(
    "DATABASE_CONN_MAX_AGE", default=60
)  # noqa F405
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCAL_APPS = [
    "{{ cookiecutter.project_slug }}.core",
]

# Apps
THIRD_PARTY_APPS = []
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]


INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLs
ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"

# Templates

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


# Django Contrib Settings
# ------------------------------------------------------------------------------
# django.contrib.auth
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

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

# django.contrib.staticfiles
STATIC_URL = "static/"

# Third Party Settings
# ------------------------------------------------------------------------------


# Project Settings
# ------------------------------------------------------------------------------
