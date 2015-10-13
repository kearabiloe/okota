"""
Django settings for okota project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1a8byer)(tqmpe8db9-1&@^p+u=nv3p==ca=vbqvo2sez3x$bz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['okota-kearabiloe.rhcloud.com','www.okota.co.za']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'okota',
    'django.contrib.humanize',
    'tastypie',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'okota_website.urls'

WSGI_APPLICATION = 'okota_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'okota',
        'USER': 'admin8qse9tv',
        'PASSWORD': 'fhqWmZL4iTth',
        'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-za'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'static/')
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

UPLOADS_DIRECTORY = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'uploads/')

MEDIA_ROOT = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'media/')
MEDIA_URL = '/media/'


#Site-wide logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'okota-django.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'INFO',
        },
        'okota': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
}
SESSION_SAVE_EVERY_REQUEST = True
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'kea@okota.co.za'
EMAIL_HOST_PASSWORD = '19691969-mom'