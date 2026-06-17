import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def env_bool(key: str, default: bool) -> bool:
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def env_int(key: str, default: int) -> int:
    value = os.getenv(key)
    return int(value) if value is not None else default


SECRET_KEY = env("DJANGO_SECRET_KEY", "replace-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = [host.strip() for host in env("DJANGO_ALLOWED_HOSTS", "*").split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sync_bridge",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

BITRIX_BASE_URL = env("BITRIX_BASE_URL", "https://example.bitrix24.ru/rest")
BITRIX_SOURCE_PATH = env("BITRIX_SOURCE_PATH", "/bitrix/export")
BITRIX_TARGET_PATH = env("BITRIX_TARGET_PATH", "/bitrix/import")
BITRIX_AUTH_TOKEN = env("BITRIX_AUTH_TOKEN")
BITRIX_TIMEOUT = env_int("BITRIX_TIMEOUT", 30)

ONEC_BASE_URL = env("ONEC_BASE_URL", "http://195.94.252.194")
ONEC_INVOICE_LIST_PATH = env("ONEC_INVOICE_LIST_PATH", "/ut/hs/bitrixintegration/invoice/list")
ONEC_TARGET_PATH = env("ONEC_TARGET_PATH", "/onec/import")
ONEC_USERNAME = env("ONEC_USERNAME", "integration")
ONEC_PASSWORD = env("ONEC_PASSWORD", "Test1234")
ONEC_TIMEOUT = env_int("ONEC_TIMEOUT", 30)
