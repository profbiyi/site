import os
from machina import (
    get_apps as get_machina_apps,
    MACHINA_MAIN_TEMPLATE_DIR,
    MACHINA_MAIN_STATIC_DIR
)

HTML_MINIFY             = False
DEBUG                   = False
TESTING                 = False
SECURE_SSL_REDIRECT     = True
SECURE_SSL_HOST         = 'alphageek.xyz'
SESSION_COOKIE_SECURE   = True
CSRF_COOKIE_SECURE      = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
PROJECT_NAME            = 'agcs'
ALLOWED_HOSTS           = [
    'alphageekcs.com',
    'www.alphageekcs.com',
    'secure.alphageekcs.com',
    'www.secure.alphageekcs.com',
    'alphageek.xyz',
    'www.alphageek.xyz',
    'secure.alphageek.xyz',
    'www.secure.alphageek.xyz',
    'community.alphageek.xyz',
]
BASE_DIR         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF     = PROJECT_NAME + '.urls'
EMAIL_USE_TLS    = True
ADMINS           = (('Ryan Kaiser', 'ryank@alphageek.xyz'),)
ADMIN_URL        = 'admin/'
MANAGERS         = ADMINS
WSGI_APPLICATION = PROJECT_NAME +'.wsgi.application'
LANGUAGE_CODE    = 'en-us'
TIME_ZONE        = 'America/Chicago'
USE_I18N         = True
USE_L10N         = True
USE_TZ           = True
EMAIL_USE_TLS    = True
EMAIL_HOST       = 'smtp.zoho.com'
EMAIL_PORT       = '587'
STATIC_URL       = '/static/'
STATIC_ROOT      = os.path.join('/srv', PROJECT_NAME, 'assets', 'static')
MEDIA_ROOT       = os.path.join('/home/django', 'public', 'media')
MEDIA_URL        = '/media/'

STATICFILES_DIRS = [
    ('assets', os.path.join(BASE_DIR, PROJECT_NAME, 'static')),
    MACHINA_MAIN_STATIC_DIR,
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'compressor.finders.CompressorFinder',
]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
   }
}

INSTALLED_APPS = [
    'landing.apps.LandingConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'snowpenguin.django.recaptcha2',
    'favicon',
    'bootstrap3',
    'django_assets',
    'compressor',
    'mptt',
    'haystack',
    'whoosh',
    'widget_tweaks',
    'pagedown',
    'django_markdown',
    'pytz',
    'community',
] + get_machina_apps([
    'community.apps.forum_conversation',
    'community.apps.forum_member',
])


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, PROJECT_NAME, 'templates'),
            os.path.join(BASE_DIR, 'community', 'templates'),
            MACHINA_MAIN_TEMPLATE_DIR,
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'machina.core.context_processors.metadata',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

MIGRATION_MODULES = {
    'forum_conversation': 'machina.apps.forum_conversation.migrations',
    'forum_member': 'machina.apps.forum_member.migrations',
}

HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
    'PATH': '/var/local/agcs/idx/whoosh_index',
  },
}

MACHINA_FORUM_NAME = 'Alpha Geeks Forum'

MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_edit_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_download_file',
]

MARKDOWN_EDITOR_SKIN = 'simple'

#SECRET_KEY = ''
#GOOGLE_API_KEY = ''
#RECAPTCHA_PRIVATE_KEY = ''
#RECAPTCHA_PUBLIC_KEY = ''
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#DATABASES = {}

try:
    from .local_settings import *
except ImportError:
    pass

COMPANY = {
    'phone'      : '(972) 656-9338',
    'email'      : 'root@alphageek.xyz',
    'addr'       : ['1727 Nest Pl.', 'Plano, TX 75093'],
    'long_name'  : 'Alpha Geek Computer Services',
    'short_name' : 'Alpha Geek Services',
    'links' : {
        'social' : {
            'facebook'    : 'https://facebook.com/alphageekcs',
            'google_plus' : 'https://plus.google.com/+Ntxcomputerservices',
            'google_maps' : 'https://maps.google.com?daddr=Alpha+Geek+Computer+Services+1727+Nest+Place+Plano+TX+75093',
            'yelp'        : 'https://www.yelp.com/biz/alpha-geek-computer-services-plano',
            'github'      : 'https://github.com/alphageek-xyz',
        },
    },
}

if TESTING:
    SECRET_KEY = '^sp+qc8lmvr^jnj0#hpr!ueg%=yoi1d=6h6jg@530o-7)csrcd'
    SECURE_SSL_REDIRECT     = False
    SECURE_SSL_HOST         = None
    SECURE_PROXY_SSL_HEADER = None
    SESSION_COOKIE_SECURE   = False
    CSRF_COOKIE_SECURE      = False
    ALLOWED_HOSTS           = ['localhost', 'rdkpc.dk.lan', '192.168.92.27']

    ALLOWED_HOSTS = [
        'localhost:8000',
    ]

    INTERNAL_IPS = (
        '127.0.0.1',
    )
