"""
Django settings for SpMarket project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import sys

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TTT 添加的
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ae^bcd#9v*au45wnl1axj8_f7m4+8^m$@&+39(vx0lb^og!$$i'

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
    'haystack',  # 全文检索框架
    # 添加子应用
    'cart.apps.CartConfig',
    'goods.apps.GoodsConfig',
    'order.apps.OrderConfig',
    'user.apps.UserConfig',
    'ckeditor',  # 添加ckeditor富文本编辑器
    'ckeditor_uploader',  # 添加ckeditor富文本编辑器文件上传部件
]

MIDDLEWARE = [ # 中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'utils.TestMiddleware.TestMiddleware',# 注册 自己的中间键
]

ROOT_URLCONF = 'SpMarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # 添加渲染 MEDIA_URL 变量
            ],
        },
    },
]

WSGI_APPLICATION = 'SpMarket.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {  # sqlite3
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS为上线前需要删除的内容
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# 设置静态文件根目录  上线的时候使用
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# 添加django中的缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # redis启动起来，使用的1号数据库（0-15）
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# 修改默认 session的存储引擎
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# 短信发送的key
# ACCESS_KEY_ID = "LTAI2qSiJdWP87em"
# ACCESS_KEY_SECRET = "FzORQ587PgGBoOAdmxzCjaxQi8klUi"

# 这部分需要阿里的AccessKey
ACCESS_KEY_ID = "NUll"
ACCESS_KEY_SECRET = "NUll"

# 配置上传图片

# MEDIA_URL = os.path.join(STATIC_URL, '/media/')
MEDIA_URL = "/media/"  # 访问路径

# 配置该url对应的物理目录存储地址
# MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')    # 上传路径
# 获得上传文件的url地址,上传文件放在MEDIA_ROOT中,返回的地址前面加上MEDIA_URL.

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')  # 设置静态文件路径为主目录下的media文件夹

# 富文本框
# 设置ckeditor的上传目录
CKEDITOR_UPLOAD_PATH = "uploads/"  # 这个目录是相对目录，相对与 MEDIA_ROOT

# 编辑器样式配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}


# 配置搜索引擎
# 全文检索框架的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 配置搜索引擎
        'ENGINE': 'utils.whoosh_cn_backend.WhooshEngine',
        # 配置索引文件目录
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
#当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'