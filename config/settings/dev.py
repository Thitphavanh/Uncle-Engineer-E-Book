"""
Development settings for config project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('POSTGRES_DB', 'uncleebook_dev'),
        "USER": os.environ.get('POSTGRES_USER', 'uncleebook'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD', 'uncleebook123'),
        "HOST": os.environ.get('POSTGRES_HOST', 'db-dev'),
        "PORT": os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Development specific settings
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Email backend for development (console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging configuration for development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
