# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

print(socket.gethostname())

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

TEMPLATE_DEBUG = bool(os.environ.get('TEMPLATE_DEBUG', False))

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'bootstrap3',
    'registration',
    'django_summernote',
    'captcha',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fun.urls'

WSGI_APPLICATION = 'fun.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'CONN_MAX_AGE': 600,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'bg'

TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ACCOUNT_ACTIVATION_DAYS = 5
REGISTRATION_OPEN = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/profile/login/'

AUTH_USER_MODEL = 'core.Author'

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

SUMMERNOTE_CONFIG = {
    'iframe': False,
    'airMode': False,
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ('127.0.0.1')

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379",
        "OPTIONS": {
            "DB": 1,
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            "PARSER_CLASS": "redis.connection.HiredisParser",
        }
    }
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400

# These are used to send via gearman worker
MANDRILL_USER = os.environ['MANDRILL_USER']
MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY']
MANDRILL_HOST = os.environ['MANDRILL_HOST']

# These are for the default django email factory
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = MANDRILL_HOST
EMAIL_HOST_USER = MANDRILL_USER
EMAIL_HOST_PASSWORD = MANDRILL_API_KEY
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
SERVER_EMAIL = DEFAULT_FROM_EMAIL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/fun.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'core': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

BL_DOMAINS = os.path.join(BASE_DIR, 'blacklisted_domains.txt')

VERSION = os.environ['VERSION']
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
