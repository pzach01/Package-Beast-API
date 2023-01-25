"""
Django settings for Package-Beast-API project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

if (os.getenv('ENVIRONMENT_TYPE') == 'PRODUCTION'):
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': os.getenv('DATABASE_USER'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD'),
            'HOST': os.getenv('DATABASE_HOST'),
            'PORT': '5432'
        }
    }
    ALLOWED_HOSTS = ['https://packagebeast.com', 'api.packagebeast.com', 'packageapp-env.pumdxt3sbe.us-east-1.elasticbeanstalk.com']
    #ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_WHITELIST = ['https://packagebeast.com']

   
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    os.environ['STRIPE_TAX_RATE_ID']='txr_1ICsUoJWFTMXIZUo9c5KbCFS'
    # Delete this line...
    # os.environ['SHIPPO_API_KEY']='shippo_test_41c916402deba95527751c894fd23fc03d7d8198'

else:
    SECRET_KEY = '05^q)gef3f(*a^u3-e2b4of@5uh^^#i@roi*54^c2kft*r+*sq'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ebdb',
            'USER': 'packageBeastDB',
            'PASSWORD': 'mNREQKk4oe4th1V76hRbiRRbYk6ugV9PinlAmJ2oNnaSvujh3NUGSTMkm1RaAH4nHVCMDO90np5r5LDKcQQIKTL5Rz9rLjsjZfaD',
            'HOST': 'aauh312xer0ff8.cg1crfkuftt1.us-east-1.rds.amazonaws.com',
            'PORT': '5432'
        }
    }
    ALLOWED_HOSTS = ['127.0.0.1', 'packageapp-development.us-east-1.elasticbeanstalk.com', 'developmentapi.packagebeast.com']
    CORS_ORIGIN_WHITELIST = ['http://localhost:4200', 'https://development.packagebeast.com']
    #ALLOWED_HOSTS = ['*']
    DEBUG = True

    # test keys
    os.environ['STRIPE_API_SECRET']='sk_test_51I76dqE5mpXPYa9nHYN046OuGpuQdNihI2JNfZHPYb05YbGtcr4EXDwytftg6MEgOk6SOvstWxMvFcFtyH67nrEN00xQKQQ6Jv'
    os.environ['STRIPE_WEBHOOK_SECRET']='whsec_sp9erCWYVqUqRZpj3Z99jFrWKtlJNKQO'
    os.environ['STRIPE_TAX_RATE_ID']='txr_1ICrg3E5mpXPYa9nYpguvzzc'
    os.environ['SHIPPO_CLIENT_ID']='bf2c8e4685b44c3dbf35b8aa3cb2df5e'
    os.environ['SHIPPO_CLIENT_SECRET']='LC9N-5-HnySDwsSGbG1PCSvuaTve1WMf0HyEXXu-t_g'
    os.environ['SHIPPO_API_KEY']='shippo_test_41c916402deba95527751c894fd23fc03d7d8198'
    os.environ['GOOGLE_CLIENT_ID']= '1085639833940-5rtpdadme2qql89234lc94jifv1lg30d.apps.googleusercontent.com'

# Lambda function / api gateway uri's
SHIPPO_API_INTERFACE_FETCH_MANY_SHIPMENTS_URI = 'https://z3k2o2uns4.execute-api.us-east-1.amazonaws.com/shippo-shipments/fetch-many'
SHIPPO_API_INTERFACE_CREATE_SHIPMENTS_URI = 'https://z3k2o2uns4.execute-api.us-east-1.amazonaws.com/shippo-shipments/create-many'

#CORS_ORIGIN_ALLOW_ALL = True

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_FROM_EMAIL = 'no-reply@packagebeast.com'

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',  # New-PZ
    'rest_auth',  # New-PZ
    'allauth',  # New-PZ
    'allauth.account',  # New-PZ
    'allauth.socialaccount',  # New-PZ 2-9-20
    'allauth.socialaccount.providers.google', # New PZ 3-6-21
    'rest_auth.registration',  # New-PZ
    'django.contrib.sites',  # New-PZ
    'drf_yasg',  # 2-7-20 New PZ
    'items',
    'containers',
    'shipments',
    'addresses',
    'quotes',
    'arrangements',
    'users',
    'subscription',
    'payment',
    'shipposervice',
    'safedelete'
]

# User registration errors out if you remove this. I think its used with django.contrib.sites
SITE_ID = 1

# auth settings to use email instead of username
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

# 6-18-20 PZ - CHANGED LINE BELOW TO SUPPORT USER PREFERENCES
REST_AUTH_SERIALIZERS = {'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer',
                         'LOGIN_SERIALIZER': 'users.serializers.LoginSerializer'}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer'}


# Following is added to enable registration with email instead of username
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
# REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        #   'Basic': {
        #         'type': 'basic'
        #   },

        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'

LOGIN_REDIRECT_URL = '/swagger/'

LOGOUT_URL = '/accounts/logout/'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Package-Beast-API.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Package-Beast-API.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

  

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

AUTH_USER_MODEL = 'users.User'
SOCIALACCOUNT_ADAPTER = 'Package-Beast-API.urls.CustomSocialAccountAdapter'