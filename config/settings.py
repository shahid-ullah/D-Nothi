# config/settings
import os
from datetime import datetime

import environ
from django.conf import settings
from django.db.models import Q

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'az895+kp%@b8ab=8yit+vek9vson88l005l!nq^_tv*i2l-d*r'
SECRET_KEY = env('SECRET_KEY')
REDIS_HOST = env('REDIS_HOST')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # third party app
    'rest_framework',
    'django_extensions',
    'crispy_forms',
    'debug_toolbar',
    # local apps
    # 'monthly_report.apps.MonthlyReportConfig',
    'users.apps.UsersConfig',
    'automate_process.apps.AutomateProcessConfig',
    'dashboard_generate.apps.DashboardGenerateConfig',
    'dashboard_ui.apps.DashboardUIConfig',
    'backup_source_db.apps.BackupSourceDbConfig',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'dashboard_generate.context_processors.get_last_dashboard_update_time',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASE_ROUTERS = [
    'automate_process.db_router.AutomateProcessDBRouter',
    'backup_source_db.db_router.BackupSourceDBRouter',
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {'charset': 'utf8mb4'},
    },
    'source_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('SOURCE_DB_NAME'),
        'USER': env('SOURCE_DB_USER'),
        'PASSWORD': env('SOURCE_DB_PASSWORD'),
        'HOST': env('SOURCE_DB_HOST'),
        'PORT': env('SOURCE_DB_PORT'),
        'OPTIONS': {'charset': 'utf8mb4'},
    },
    'backup_source_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('BACKUP_SOURCE_DB_NAME'),
        'USER': env('BACKUP_SOURCE_DB_USER'),
        'PASSWORD': env('BACKUP_SOURCE_DB_PASSWORD'),
        'HOST': env('BACKUP_SOURCE_DB_HOST'),
        'PORT': env('BACKUP_SOURCE_DB_PORT'),
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}

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

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Add these new lines
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

DATA_BASE_DIR_PATH = os.path.join(BASE_DIR, 'Data')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SYSTEM_UPDATE_RUNNING = False

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'users.custom_backends.NdoptorAuthenticationBackend',
)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_RATES': {'anon': '1/day', 'user': '1/day'},
}

LOGOUT_REDIRECT_URL = 'dashboard_home'

SSO_LOGIN_URL = 'https://n-doptor-accounts-stage.nothi.gov.bd/login'
SSO_LOGOUT_URL = 'https://n-doptor-accounts-stage.nothi.gov.bd/logout'

QUERY_CREATED_DATE = Q(created__gte=datetime(2013, 11, 1, 0, 0, 0)) | Q(created__isnull=True)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_HOST,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

CACHE_TTL = 60 * 10 * 60

if settings.DEBUG:
    CACHE_TTL = 60


if settings.DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.history.HistoryPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
