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
    "DATABASE_CONN_MAX_AGE",
    default=60,
)  # noqa F405
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Apps

LOCAL_APPS = [
    "{{ cookiecutter.project_slug }}.core",
]

THIRD_PARTY_APPS = [
    "debug_toolbar",
{%- if cookiecutter.use_htmx == 'y' %}
    "django_htmx",
{%- endif %}
]
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
{%- if cookiecutter.use_htmx == 'y' %}
    "django_htmx.middleware.HtmxMiddleware",
{%- endif %}
]

# URLs
ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"

# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APPS_DIR / "templates"],
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rich": {"datefmt": "[%X]"},
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
            "filters": ["require_debug_true"],
        },
        "production": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["production"],
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console", "production"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}


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
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [APPS_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Third Party Settings
# ------------------------------------------------------------------------------
# enable debug_toolbar and debug context
INTERNAL_IPS = ["127.0.0.1"]

# Project Settings
# ------------------------------------------------------------------------------
