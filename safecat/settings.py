#-*- coding: GBK -*-
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

ATTACK_CLI_PATH = 'E:/School_of_software/information_security/holiday-learning/python/django/safecat/libs/attack_framework/safecatcli.py'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),'static')

UPLOAD_ROOT = os.path.join(os.path.dirname(BASE_DIR),'product')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'se3n26ohkhup6dl_54q4qw7#qkv*hzv&nah+as@0#_9kldn&vz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hostcrawler',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'safecat.urls'

WSGI_APPLICATION = 'safecat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'safecat',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'localhost',
        'PORT':'3306'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    ("css", os.path.join(STATIC_ROOT,'css')),
    ("js", os.path.join(STATIC_ROOT,'js')),
    ("images", os.path.join(STATIC_ROOT,'images')),
    ("reports",os.path.join(STATIC_ROOT,'reports'))
)

#Here are templates
TEMPLATE_DIRS = (
    'E:/School_of_software/information_security/holiday-learning/python/django/safecat/static/template',
)
