import os
from machina import (
    get_apps as get_machina_apps,
    MACHINA_MAIN_TEMPLATE_DIR,
    MACHINA_MAIN_STATIC_DIR
)

HTML_MINIFY             = False
DEBUG                   = False
TESTING                 = False
USE_X_FORWARDED_HOST    = True
SECURE_SSL_REDIRECT     = True
CSRF_COOKIE_DOMAIN      = '.alphageek.xyz'
SESSION_COOKIE_SECURE   = True
CSRF_COOKIE_SECURE      = True
CSRF_COOKIE_HTTPONLY    = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
PROJECT_NAME            = 'agcs'
LOG_DIR          = '/var/local/agcs/log/django'
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
MEDIA_ROOT       = os.path.join('/srv', PROJECT_NAME, 'public', 'media')
MEDIA_URL        = '/media/'

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

STATICFILES_DIRS = [
    ('assets', os.path.join(BASE_DIR, PROJECT_NAME, 'static')),
    MACHINA_MAIN_STATIC_DIR,
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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
    'mptt',
    'haystack',
    'whoosh',
    'widget_tweaks',
    'pagedown',
    'pytz',
    'community',
] + get_machina_apps([
    'community.apps.forum_conversation',
    'community.apps.forum_member',
])

COMPRESS_CSS_FILTERS=[
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter',
]

COMPRESS_JS_FILTERS=[
    'compressor.filters.jsmin.JSMinFilter',
    'compressor.filters.jsmin.SlimItFilter',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'debug': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
         'info': {
            'format': '%(levelname)s %(asctime)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, os.getenv('DJANGO_LOG_LEVEL', 'INFO').lower() + '.log'),
            'formatter': 'debug',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
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


try:
    from .local_settings import *
except ImportError:
    pass

COMPANY = {
    'phone'      : '(972) 656-9338',
    'email'      : 'root@alphageek.xyz',
    'addr'       : ['1727 Nest Pl.', 'Plano, TX 75093'],
    'long_name'  : 'Alpha Geek Computer Services',
    'short_name' : 'Alpha Geeks',
    'links' : {
        'social' : {
            'facebook'    : 'https://facebook.com/alphageekcs',
            'google_plus' : 'https://plus.google.com/+Ntxcomputerservices/about',
            'google_maps' : 'https://maps.google.com?daddr=Alpha+Geek+Computer+Services+1727+Nest+Place+Plano+TX+75093',
            'yelp'        : 'https://www.yelp.com/biz/alpha-geek-computer-services-plano',
            'github'      : 'https://github.com/alphageek-xyz',
        },
    },
}

if os.environ.get('DJANGO_DEBUG_OVERRIDE'):
    DEBUG = True
    SECURE_SSL_REDIRECT = False
    del(ALLOWED_HOSTS,
        LOGGING,
        CSRF_COOKIE_DOMAIN,
        SESSION_COOKIE_SECURE,
        CSRF_COOKIE_SECURE,
        CSRF_COOKIE_HTTPONLY,
        SECURE_PROXY_SSL_HEADER
    )
    RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
