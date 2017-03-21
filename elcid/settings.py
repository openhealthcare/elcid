# Django settings for elcid project.
import commands
import os
import sys

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
ON_HEROKU = False
ON_TEST = 'test' in sys.argv

try:
    import dj_database_url
    ON_HEROKU = True

    DATABASES = {
        'default': dj_database_url.config(default='sqlite:///' + PROJECT_PATH + '/opal.sqlite')
    }
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_PATH, 'opal.sqlite'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Support', 'support@openhealthcare.org.uk',),
)

MANAGERS = ADMINS


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'localhost',
    '.herokuapp.com'
    ]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/assets/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
# if ON_TEST
#     STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hq6wg27$1pnjvuesa-1%-wiqrpnms_kx+w4g&&o^wr$5@stjbu'

# This should be over written by local settings in the development environment
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        )),
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'opal.middleware.AngularCSRFRename',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'opal.middleware.DjangoReversionWorkaround',
    'reversion.middleware.RevisionMiddleware',
    'axes.middleware.FailedLoginMiddleware',
    'elcid.middleware.SessionMiddleware',
    'elcid.middleware.LoggingMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'elcid.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'elcid.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS= (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'opal.context_processors.settings',
    'opal.context_processors.models'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'reversion',
    'opal',
    'rest_framework',
    'rest_framework.authtoken',
    'compressor',
    'opal.core.search',
    'elcid',
    'obs',
    'django.contrib.admin',
    'opat',
    'walkin',
    'research',
    'wardround',
    'microhaem',
    'infectiousdiseases',
    'referral',
    'dashboard',
    'guidelines',
    'dischargesummary',
    'djcelery',
)

if ON_TEST:
    INSTALLED_APPS += ('opal.tests',)
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    MIGRATION_MODULES = {
        'opal': 'opal.nomigrations',
        'elcid': 'elcid.nomigrations',
        'guidelines': 'guidelines.nomigrations',
        'walkin': 'walkin.nomigrations',
        'research': 'research.nomigrations',
        'opat': 'opat.nomigrations',
        'microhaem': 'microhaem.nomigrations',
        'infectiousdiseases': 'infectiousdiseases.nomigrations',
        'obs': 'obs.nomigrations'
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'elcid.log.ConfidentialEmailer'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'elcid.requestLogger': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'elcid.sessionLogger': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

if not ON_TEST and not ON_HEROKU:
    # lets not log to files on travis
    LOGGING["handlers"]["session"] = {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': os.path.join(
            PROJECT_PATH, "..", "..", "log", "session.log"
        )
    }
    LOGGING["loggers"]["elcid.sessionLogger"]["handlers"] = ['session']



# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# (Heroku requirement)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y']
DATETIME_FORMAT = 'd/m/Y H:i:s'
DATETIME_INPUT_FORMATS = ['%d/%m/%Y %H:%M:%S']

CSRF_COOKIE_NAME = 'XSRF-TOKEN'
APPEND_SLASH = False

AXES_LOCK_OUT_AT_FAILURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# New modular settings!
# !!! TODO: Are these how we want to discover these ?
OPAL_OPTIONS_MODULE = 'elcid.options'
OPAL_BRAND_NAME = 'elCID'
OPAL_LOG_OUT_MINUTES = 15
OPAL_LOG_OUT_DURATION = OPAL_LOG_OUT_MINUTES*60*1000
OPAL_FLOW_SERVICE = 'elCIDFlow'

# Do we need this at all ?
OPAL_EXTRA_HEADER = 'elcid/print_header.html'

# ANALYTICS Settings
OPAL_ANALYTICS_ID = 'UA-XXXXXXX'
OPAL_ANALYTICS_NODOMAIN = True

CONTACT_EMAIL = ['michael.marks@uclh.nhs.uk', 'david@openhealthcare.org.uk']
DEFAULT_FROM_EMAIL = 'elcid@openhealthcare.org.uk'
DEFAULT_DOMAIN = 'http://ELCIDL/'

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
if not DEBUG:
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
    EMAIL_HOST= 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')
else:
    EMAIL_PORT = 1025
    EMAIL_HOST = 'localhost'


VERSION_NUMBER = '0.6.4'

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
#TEST_RUNNER = 'django_test_coverage.runner.CoverageTestSuiteRunner'

COVERAGE_EXCLUDE_MODULES = ('elcid.migrations', 'elcid.tests',
                            'elcid.settings',
                            'elcid.local_settings',
                            'opal.migrations', 'opal.tests',
                            'opal.wsgi')


INTEGRATING = False
GLOSSOLALIA_URL = 'http://localhost:5000/'
GLOSSOLALIA_NAME = 'elcid'


GLOSS_ENABLED = False

if GLOSS_ENABLED:
    OPAL_SEARCH_BACKEND = "elcid.search.GlossQuery"
    GLOSS_URL_BASE = "http://0.0.0.0:6767"
    GLOSS_USERNAME = "override_this"
    GLOSS_PASSWORD = "and_override_this"

EXTRACT_ASYNC = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

if not ON_TEST:
    try:
        from local_settings import *
    except ImportError:
        pass

# #DEBUG_TOOLBAR_PATCH_SETTINGS = False
# MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
# #INTERNAL_IPS = ('127.0.0.1',)
