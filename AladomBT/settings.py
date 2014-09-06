"""
Django settings for AladomBT project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

try:
    from AladomBT import djenv
except ImportError:
    djenv = {}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = djenv.get('SECRET_KEY', '-8j@cxj^72z4ku=o1@hep1cr6&v^70421us$o-+)cs(36#y)hr')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = djenv.get('DEBUG', True)
TEMPLATE_DEBUG = djenv.get('TEMPLATE_DEBUG', DEBUG)

ALLOWED_HOSTS = djenv.get('ALLOWED_HOSTS', [])

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'AladomBT.urls'

WSGI_APPLICATION = 'AladomBT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aladom_bt',
        'USER': 'aladom',
        'PASSWORD': 'aladom',
        'HOST': ''
    }
}
DATABASES = djenv.get('DATABASES', DATABASES)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = djenv.get('LANGUAGE_CODE', 'fr-fr')

TIME_ZONE = djenv.get('TIMEZONE', 'Europe/Paris')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
