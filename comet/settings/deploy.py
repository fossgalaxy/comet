"""
Docker deployment config - should be hardened to stop bad things happening
"""
from .base import *
import os

# docker magic
def get_secret(key):
    # check if the _FILE varient is present
    if key+"_FILE" in os.environ:
        key_file = os.environ[key+"_FILE"]
        with open(key_file) as f:
            return "".join(f.readlines()).strip()

    # if not, default to the variable
    return os.envrion[key]

# Require secret key from envrioment variable
SITE_ID = int(os.environ['SITE_ID'])
SECRET_KEY = get_secret('SECRET_KEY')

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

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True # No, i'm not letting you turn this off.

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')

PINAX_NOTIFICATIONS_QUEUE_ALL = True # Stop the email server killing the build scripts.

# People to email with django explodes
ADMINS = os.environ.get('ADMINS', '').split(",")

FILEPROVIDER_NAME = "nginx"

# Database Related
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
	'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': get_secret('POSTGRES_PASSWORD'),
	'HOST': os.environ.get('POSTGRES_HOST', 'db'),
    }
}
