from pathlib import Path

import environs

APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent

env = environs.Env()
env.read_env(BASE_DIR / ".env", recurse=False)

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")

DATABASES = {
    "default": env.dj_db_url(
        "DATABASE_URL",
        default="postgresql:///{{ cookiecutter.project_slug }}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
{%- if cookiecutter.use_crispy_forms %}
    "crispy_forms",
{%- if cookiecutter.css_framework == "bootstrap" %}
    "crispy_bootstrap5",
{% endif -%}
{% endif %}
    "django_htmx",
    "debug_toolbar",
    "{{ cookiecutter.project_slug }}",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_DIR / "templates"],
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

{%- if cookiecutter.use_crispy_forms and cookiecutter.css_framework == "bootstrap" %}
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
{% endif %}
USE_TZ = True

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "static/"

# STATIC_ROOT is where collectstatic will collect files for deployment
STATIC_ROOT = env.str("STATIC_ROOT", default=str(BASE_DIR / "static"))

# STATICFILES_DIR is where "django.contrib.staticfiles" looks during development
STATICFILES_DIRS = [APP_DIR / "static"]

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "rich": {"datefmt": "[%X]"},
        },
        "handlers": {
            "console": {
                "class": "rich.logging.RichHandler",
                "formatter": "rich",
                "level": "DEBUG",
                "rich_tracebacks": True,
                "tracebacks_show_locals": True,
            },
        },
        "loggers": {
            "django": {
                "handlers": [],
                "level": "INFO",
            },
            "website": {
                "handlers": [],
                "level": "DEBUG",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }