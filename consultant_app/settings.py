from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

# Cross origin/CSRF configurations

ALLOWED_HOSTS = ['localhost', 'lawyer-appointment-app.onrender.com']

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'https://lawyer-appointment-app.onrender.com']
CSRF_ALLOWED_ORIGINS = ['http://localhost:8000', 'https://lawyer-appointment-app.onrender.com']
CORS_ORIGINS_WHITELIST = ['http://localhost:8000', 'https://lawyer-appointment-app.onrender.com']

# The email sending mechanism configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_DEBUG = True

INSTALLED_APPS = [
    'daphne',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'base_app',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'fontawesomefree',
    'cloudinary'
]

ASGI_APPLICATION = "consultant_app.asgi.application"

# We use Redis for the channel layer only in production.

if DEBUG:
    CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
  }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(os.getenv('REDIS_HOST'))],
            },
        },
    }

AUTH_USER_MODEL = "base_app.User"

#Configurations needed for allauth

SITE_ID=3

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],
        "AUTH_PARAMS": {
                        "access_type": "online"
                        }
    }
}

LOGIN_REDIRECT_URL = "/examine-oauth/"
LOGOUT_REDIRECT_URL = "/"

#We set this to true to skip the default consent redirecting screen/

SOCIALACCOUNT_LOGIN_ON_GET=True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Uncomment in production

ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

ROOT_URLCONF = 'consultant_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'consultant_app.wsgi.application'


# Database Configurations
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL')

# The postgress sql database configuration
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

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

# Uncomment in development

# STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     BASE_DIR / 'static'
# ]


# Uncomment in production

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
)

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Cloudinary - django integration

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name= os.getenv('MEDIA_CLOUD_NAME'),
    api_key=os.getenv('MEDIA_API_KEY'),
    api_secret=os.getenv('MEDIA_API_SECRET')
)