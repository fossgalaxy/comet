"""
Docker deployment config - should be hardened to stop bad things happening
"""
from .base import *
import os

# Require secret key from envrioment variable
SECRET_KEY = os.environ['SECRET_KEY']

# Disable Debug
DEBUG = bool(os.environ.get('DEBUG', False))

# CSRF protection - allowed hostnames
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# SSL/Proxy related (only allow https)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SSL_ONLY = bool(os.environ.get('SSL_ONLY', False))
CSRF_COOKIE_SECURE = SSL_ONLY
SESSION_COOKIE_SECURE = SSL_ONLY

# Database Related
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'NAME': os.environ.get('DB_ENV_DB', 'postgres'),
	'USER': os.environ.get('DB_ENV_POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_ENV_POSTGRES_PASSWORD', ''),
	'HOST': os.environ.get('DB_ENV_HOST', 'db'),
    }
}
