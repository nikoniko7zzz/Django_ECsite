"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.24.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ # 追加
from pathlib import Path # 追加
from django.contrib import messages # 追加

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

root = environ.Path(BASE_DIR / 'secrets')

# ここはif文で出し分ける
# 本番環境用
# env.read_env(root('.env.prod'))

# 開発環境用
env.read_env(root('.env.dev'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '%i$$xt4l7qb_!*(3u4ada3c^+posa(5o#t6%^90bdc*e2w_5c('
SECRET_KEY = env.str('SECRET_KEY')  # 変更

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')  # 変更

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')  # 変更


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base', #追加
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], #追加
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'config.custom_context_processors.base',  # 追記
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja' #変更

TIME_ZONE = 'Asia/Tokyo' #変更

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] #追加

# 消費税率
TAX_RATE = 0.1

# Stripe API Key
STRIPE_API_SECRET_KEY = env.str('STRIPE_API_SECRET_KEY')

# スキーマ＆ドメイン
MY_URL = env.str('MY_URL')

# カスタムユーザーモデルを使うための設定
AUTH_USER_MODEL = 'base.User' # base.Userモデルを使う

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/' # ログインした後のページ指定

LOGOUT_URL = '/logout/'

LOGOUT_REDIRECT_URL = '/login/'

# messages
MESSAGE_TAGS = {
    messages.ERROR: 'rounded-0 alert alert-danger',
    messages.WARNING: 'rounded-0 alert alert-warning',
    messages.SUCCESS: 'rounded-0 alert alert-success',
    messages.INFO: 'rounded-0 alert alert-info',
    messages.DEBUG: 'rounded-0 alert alert-secondary',
}

# custom_context_processors
TITLE = 'VegeKet'




# 仮想空間
# source environment_3_9_7/bin/activate