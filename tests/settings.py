from agcs.settings import *

SECRET_KEY = 'fake-key'
SECURE_SSL_REDIRECT = False
ALLOWED_HOSTS.append('testserver')
INSTALLED_APPS += ["tests",]
