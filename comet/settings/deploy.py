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

# Email stuff
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'noreply@fossgalaxy.com')
DEFAULT_FROM_EMAIL = SERVER_EMAIL # not sure why there are two settings >.<

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True # No, i'm not letting you turn this off.

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

PINAX_NOTIFICATIONS_QUEUE_ALL = True # Stop the email server killing the build scripts.

# People to email with django explodes
ADMINS = os.environ.get('ADMINS', '').split(",")

FILEPROVIDER_NAME = "nginx"

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
