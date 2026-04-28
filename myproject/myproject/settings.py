import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

# Подключаем приложение users (Часть 1.3)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # наше приложение
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

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'users' / 'templates'],
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

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кастомная модель пользователя (Часть 1)
AUTH_USER_MODEL = 'users.CustomUser'

# Маршруты для логина и переадресаций (Часть 2.2)
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Email backend для восстановления пароля (Часть 6)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

# Media files (для загрузки аватаров)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Создаем директорию для логов если её нет
LOGS_DIR = BASE_DIR / 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Настройка логгеров для каждого модуля (Часть 2)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'standard': {
            'format': '{asctime} [{levelname}] {name}: {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
        },
        'file_rotate': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': str(LOGS_DIR / 'app.log'),
            'maxBytes': 10485760,
            'backupCount': 5,
            'encoding': 'utf-8',
        },
        'timed_rotate': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'verbose',
            'filename': str(LOGS_DIR / 'app_timed.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'encoding': 'utf-8',
            'delay': True,
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',  # Только ERROR и выше
            'formatter': 'verbose',
            'filename': str(LOGS_DIR / 'errors.log'),
            'maxBytes': 5242880,
            'backupCount': 3,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'users': {
            # ДОБАВИТЬ error_file в handlers!
            'handlers': ['console', 'file_rotate', 'timed_rotate', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'users.views': {
            # ДОБАВИТЬ error_file в handlers!
            'handlers': ['console', 'file_rotate', 'timed_rotate', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'users.forms': {
            # ДОБАВИТЬ error_file в handlers!
            'handlers': ['console', 'file_rotate', 'timed_rotate', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file_rotate', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'error_file'],
        'level': 'WARNING',
    },
}