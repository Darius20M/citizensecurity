"""
Django settings for citizensecurity project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import datetime
from pathlib import Path
from environ import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dk-8%8-v%xfgh3h2van0x7^&zr#uu^te%5em-jpep992ii8pq)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'rest_framework_simplejwt',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'django_user_agents',
    'drf_api_logger_with_user',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'simple_history',
    'django_filters',
    'post_office',
    'django_phonenumbers',
    'django_otp',
    'django_otp.plugins.otp_email',
    'security',

]
SITE_ID = 1
USER_AGENTS_CACHE = 'default'



DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'citizen00'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
MEDIA_ROOT = "media/"
UPLOAD_ROOT = 'media/uploads'
MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)

from google.oauth2 import service_account
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, "citizensecurity/google_cloud/credentials.json")
)


EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = env.str('DJANGO_EMAIL_HOST', default='none')
EMAIL_USE_TLS = env.str('DJANGO_EMAIL_TLS', default='none')
EMAIL_PORT = env.str('DJANGO_EMAIL_PORT', default='none')
EMAIL_HOST_USER = env.str('DJANGO_EMAIL_USER', default='none')
DJANGO_FROM_EMAIL = env.str('DJANGO_FROM_EMAIL', default='none')
EMAIL_HOST_PASSWORD = env.str('DJANGO_EMAIL_PASSWORD', default='none')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'security.middleware.AppRequestMiddleware',
    'security.middleware.SessionUpdateMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'drf_api_logger_with_user.middleware.api_logger_middleware.APILoggerMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'citizensecurity.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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
    {
        'BACKEND': 'post_office.template.backends.post_office.PostOfficeTemplates',
        'APP_DIRS': True,
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
            ]
        }
    }
]

WSGI_APPLICATION = 'citizensecurity.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

USER_SESSION_EXPIRE_TIME = datetime.timedelta(days=3)  # Value expression days
ACCOUNT_ADAPTER = 'security.adapters.CustomAccountAdapter'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
REST_AUTH = {
    'USE_JWT': True,
    'JWT_SECRET_KEY': SECRET_KEY,
    'OLD_PASSWORD_FIELD_ENABLED': True,
    'JWT_AUTH_COOKIE': None,
    'JWT_AUTH_REFRESH_COOKIE': None,
    'JWT_AUTH_REFRESH_COOKIE_PATH': '/',
    'JWT_AUTH_SECURE': True,
    'JWT_AUTH_RETURN_EXPIRATION': True,
    'JWT_AUTH_COOKIE_USE_CSRF': False,
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': USER_SESSION_EXPIRE_TIME,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'REGISTER_SERIALIZER': 'security.serializers.RegisterSerializer',
    'LOGIN_SERIALIZER': 'security.serializers.LoginSerializer',

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": USER_SESSION_EXPIRE_TIME,
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
}
DRF_API_LOGGER_DATABASE = True

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# verification email
OTP_EMAIL_BODY_HTML_TEMPLATE_PATH = 'account/email/email_confirmation_signup_message.html'
OTP_EMAIL_SUBJECT = 'Email Confirmation'
OTP_EMAIL_TOKEN_VALIDITY = 300

# prevenir fuerza fruta
BRUTE_FORCE_THRESHOLD = 5
BRUTE_FORCE_TIMEOUT = 120

# two fator
OTP_EXPIRY_SECONDS = 300
TOKEN_EXPIRY_SECONDS = 300

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:4200',
    'https://localhost:4200',
    'http://localhost:4401',
    'http://localhost:4202',
]

CORS_ALLOW_HEADERS = [
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'x-app-key',
    'Accept-Encoding',
]

POST_OFFICE = {
    'TEMPLATE_ENGINE': 'post_office',
    'DEFAULT_PRIORITY': 'now',

}
