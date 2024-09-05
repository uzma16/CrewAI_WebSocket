from neomodel import config
from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = "123987"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django_neomodel',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'base.management.authentication.JWTAuthentication',
#     ],
# }

JWT_CONF = {
    'ACCESS_TOKEN_LIFETIME': 172800, # in seconds
    'REFRESH_TOKEN_LIFETIME': 604800, # in seconds
}

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

# WSGI_APPLICATION = 'base.wsgi.application'
ASGI_APPLICATION = 'base.asgi.application'
# AUTH_USER_MODEL = 'Profile.CustomUser'


# For channel layer
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': "channels.layers.InMemoryChannelLayer"
#     }
# }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],  # Redis server address
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

"""
Adding PostgreSQL as out defualt database. This one is for Local deployment
"""
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv('local_db_name'),
#         'USER': os.getenv('local_db_user'),
#         'PASSWORD': os.getenv('local_db_pass'),
#         'HOST': os.getenv('host'),
#         'PORT': '5432',
#         'CONN_MAX_AGE': 600,
#     }
# }

config.DATABASE_URL = f'bolt://{os.getenv("NEO_USERNAME")}:{os.getenv("NEO_PASS")}@{os.getenv("NEO_BOLT")}'
config.CONNECTION_ACQUISITION_TIMEOUT = 120.0
config.ENCRYPTED = True
config.CONNECTION_TIMEOUT = 120.0


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
STATIC_ROOT = "staticfiles/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Below begins the setup for celery
"""
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
timezone = 'Asia/Kolkata'

# result_backend = 'django-db'
broker_connection_retry_on_startup = True

# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CELERY_BEAT_SCHEDULE = {
#     'run-every-1-day': {
#         'task': 'api.tasks.listingSubscriptionActions',
#         'schedule': timedelta(days=1),
#     },
#     'run-every-60-seconds': {
#         'task': 'api.tasks.listingSubscriptionActions',
#         'schedule': timedelta(seconds=60),
#     }
# }

"""
Configuring Static and Media files directories for Django to locate and serve them properly.
"""
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'static')
STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'public/static')
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/static')
MEDIA_URL = '/media/'

# Configure the STATICFILES_STORAGE setting to use WhiteNoise.

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # compression with caching.
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'api.s3_storage_backend.MediaStorage'

"""
S3 Bucket Settings to use for files Storage [ StaticFiles | User Uploads | Media Files ].
"""
# AWS S3 settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_FILE_OVERWRITE = True
AWS_S3_CUSTOM_DOMAIN = 'ik.imagekit.io/ZX4/'

# Optional: Set the S3 URL to use HTTPS
AWS_S3_SECURE_URLS = True

# # Optional: Set custom cache control for your files
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # Cache for 1 day
}
