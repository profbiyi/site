import os
from agcs.settings import *

SECRET_KEY = 'fake-key'
SECURE_SSL_REDIRECT = False
ALLOWED_HOSTS.append('testserver')
INSTALLED_APPS += ["tests",]
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'

if (os.environ.get('TRAVIS_CL_TEST') or not
    locals().get('DATABASES')
): DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_db',
     },
}

if locals().get('LOGGING'):
    del(LOGGING)

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp'
