from .common import *

ALLOWED_HOSTS = list(set([
    'alphageek.xyz',
    'www.alphageek.xyz',
] + SECRETS.get('allowed_hosts', [])))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': SECRETS.get('memcached_host', '127.0.0.1:11211'),
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': str(DATA_DIR.joinpath('tmp')),
   }
}

DEBUG = False

THUMBNAIL_DEBUG = DEBUG

CSRF_COOKIE_DOMAIN = '.alphageek.xyz'

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_HTTPONLY = True

USE_X_FORWARDED_HOST = True

HTML_MINIFY = True

STATIC_ROOT = str(DATA_DIR.joinpath('static'))

MEDIA_ROOT = str(DATA_DIR.joinpath('media'))
