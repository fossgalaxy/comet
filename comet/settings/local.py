"""
Local settings - debug friendly values for development
"""

from .base import *
import os

# SECURITY WARNING: development only values
SECRET_KEY = 'VeryInsecureSecretKey'
SITE_ID=1
DEBUG = True

# Database - use SQLite for local testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

FILEPROVIDER_NAME = "python"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
