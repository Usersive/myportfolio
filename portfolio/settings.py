"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 4.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from django.contrib import messages
import environ
import cloudinary.uploader
import cloudinary.api


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-#gn3*n(00jqd!!8)6*b#r7g)10e*-!g5g0qtvbmpj&6xsly0z_'
SECRET_KEY =('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True')=="True"
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1', 'https://lawalportfolio.onrender.com']

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'accounts',

    'django.contrib.sites',
    'django.contrib.sitemaps',
    # 'compressor',
    # 'corsheaders',
    
    # 'admin_honeypot',
    'cloudinary_storage',
    'cloudinary',
]

# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'compressor.finders.CompressorFinder'
# ]

SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portfolio.date.current_year',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }






# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=BASE_DIR /'static'
STATICFILES_DIRS=[
    'portfolio/static',
]
# STATICFILES_DIR     = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from django.contrib.messages import constants as messages
MESSAGE_TAGS ={
    messages.ERROR: 'danger',
}

EMAIL_BACKEND       = config('EMAIL_BACKEND')   
EMAIL_HOST          = config('EMAIL_HOST')  
EMAIL_PORT          = config('EMAIL_PORT', cast=int) 
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')    
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')    
EMAIL_USE_TLS       = config('EMAIL_USE_TLS', cast=bool)

#CLOUDINARY SETUP 
CLOUDINARY_URL = config('CLOUDINARY_URL') 

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME'),
    'API_KEY': config('API_KEY'),
    'API_SECRET': config('API_SECRET'),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'), 
        'USER': config('USER'),  
        'PASSWORD': config('PASSWORD'),  
        'HOST': config('HOST'),  
        'PORT': config('PORT', "8000"),  
    }
}

# CLOUDINARY SETUP FOR MEDIA
DEFAULT_FILE_STORAGE ='cloudinary_storage.storage.RawMediaCloudinaryStorage'

#Load barcode user image from cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

JAZZMIN_SETTINGS ={
    "site_header": "MY PORTFOLIO",
    "site_brand": "HOREN",
    "site_title": "Horen Dashboard",
    "welcome_sign": "Welcome to Horen Technologies",
    "copyright": "  Horen Technologies",
    "site_logo":"img/loder.png"
}