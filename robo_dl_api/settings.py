"""
Django settings for robo_dl_api project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
import ast

from datetime import datetime

from .config.common import *
from .config.dev import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a1=6ab6ikt^+siyww^#!j0ee8sion_+4v^62^jibs3m=g=rpt8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
# ==============================================================================
# APP 运行环境配置信息
# ==============================================================================
# 此处WSGI_ENV设置用于正式环境部署
WSGI_ENV = os.environ.get("ROBO_DEPLOY_MODE", "")
# 运行模式， DEVELOP(开发模式)， TEST(测试模式)， PRODUCT(正式产品模式)
RUN_MODE = 'DEVELOP'  # DEVELOP TEST PRODUCT
if WSGI_ENV.endswith("production"):
    RUN_MODE = "PRODUCT"
    DEBUG = False
# elif WSGI_ENV.endswith("testing"):
#     RUN_MODE = "TEST"
#     DEBUG = False
else:
    RUN_MODE = "DEVELOP"
    DEBUG = True

if os.environ.get('DEBUG'):
    DEBUG = ast.literal_eval(os.environ.get('DEBUG'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'robo_dl',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'robo_dl_api.urls'

# 跨域配置
CORS_ORIGIN_ALLOW_ALL = True

CORS_EXPOSE_HEADERS = ['X-Content-Range', 'X-Content-Total']

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

WSGI_APPLICATION = 'robo_dl_api.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# rest framework 的配置参数
REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'EXCEPTION_HANDLER': 'utils.exceptions.robo_exception_handler',

    'NON_FIELD_ERRORS_KEY': ''
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    # 'rest_framework.authentication.BasicAuthentication',
    # 'rest_framework.authentication.SessionAuthentication',
    # 'rest_framework.authentication.TokenAuthentication',
    # ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #                                   # 'rest_framework.permissions.IsAuthenticated',
    #                               ),

}

# 日志器的配置
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')

if RUN_MODE == "DEVELOP":
    LOG_LEVEL = LOG_LEVEL_DEVELOP
    LOG_CLASS = 'logging.handlers.RotatingFileHandler'
elif RUN_MODE == "TEST":
    # LOGGING_DIR = LOGGING_DIR_ENV  # 使用环境相关的LOGGING_DIR
    LOG_CLASS = 'logging.handlers.RotatingFileHandler'
    LOG_LEVEL = LOG_LEVEL_TEST
elif RUN_MODE == "PRODUCT":
    # LOGGING_DIR = LOGGING_DIR_ENV  # 使用环境相关的LOGGING_DIR
    LOG_LEVEL = LOG_LEVEL_PRODUCT
    LOG_CLASS = 'logging.handlers.RotatingFileHandler'

if not os.path.exists(LOGGING_DIR):
    try:
        os.makedirs(LOGGING_DIR)
    except:
        pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d \n \t %(message)s \n',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s \n'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'root': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, '%s.log' % datetime.now().strftime('%Y-%m-%d')),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5
        },
        'component': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, 'component.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5
        },
        'wb_mysql': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, 'wb_mysql.log'),
            'maxBytes': 1024 * 1024 * 4,
            'backupCount': 5
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        # the root logger ,用于整个project的logger
        'root': {
            'handlers': ['root'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        # 组件调用日志
        'component': {
            'handlers': ['component'],
            'level': 'WARN',
            'propagate': True,
        },
        # other loggers...
        'django.db.backends': {
            'handlers': ['wb_mysql'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}