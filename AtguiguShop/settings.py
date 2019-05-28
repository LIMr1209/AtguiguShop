"""
Django settings for AtguiguShop project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import datetime
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8#m_7g_9=u%mvi#o9ev-e)p+9198c#txjmvio9p5cy%^7*i_=$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 调试为True ，上线为false

ALLOWED_HOSTS = ['*']  # 允许的主机

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin.apps.XAdminConfig',  # xadmin注册
    'crispy_forms',  # 登陆校验
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig',
    'users.apps.UsersConfig',
    'DjangoUeditor',  # 富文本编辑器
    'rest_framework',  # 配置rest 框架
    'django_filters',  # django 过滤插件
    'corsheaders',  # 支持跨域请求
    'rest_framework.authtoken',  # Token认证  前后端一般用的认证方式
    'rest_framework_jwt',  # 基于token 的 json web token 认证
    'social_django',  # 第三方登录
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 支持跨域请求
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True  # 支持跨域请求
ROOT_URLCONF = 'AtguiguShop.urls'

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
                'django.template.context_processors.media',
                'social_django.context_processors.backends',  # 第三方登录模板引擎
                'social_django.context_processors.login_redirect',  # 第三方登录模板引擎
            ],
        },
    },
]

WSGI_APPLICATION = 'AtguiguShop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'atguigu_shop',
        'PROT': 3306,
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
    }
}
AUTH_USER_MODEL = 'users.UserProfile'  # 指定用户表
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
# 配置用户登录后台验证
AUTHENTICATION_BACKENDS = (
    'users.views.CustomModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.weibo.WeiboOAuth2',  # 微博登录认证
    'social_core.backends.qq.QQOAuth2',  # qq登录认证
    'social_core.backends.weixin.WeixinOAuth2',  # 微信登录认证
)

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

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': ('rest_framework.pagination.PageNumberpagination'), # 指定分页器
    # 'PAGE_SIZE':10,  # 每页数据
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),  # 指定 过滤器
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication', # 全局token认证
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    # drf的throttle设置api的访问速率
    # 全局 请求限制
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     # 未登录用户，根据ip判断限制
    #     'rest_framework.throttling.AnonRateThrottle',
    #     # 以登录用户 ，根据session或者token判断，限制
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '2/minute',  # 未登录 1分钟2次
        'user': '3/minute',  # 已登陆 1分钟3次
    }

}
# jwt 过期时间 ，以及jwt 前缀
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADERS_PREFIX': 'JWT',
}

# rest_framework 缓存机制过期时间
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 15 * 60  # 15分钟
}

# django-redis缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            "PASSWORD": "",
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

app_private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_key_2048.txt')
alipay_public_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_public_key.txt')

# 第三方登录配置

# 微博
SOCIAL_AUTH_WEIBO_KEY = os.environ.get('APPKEY')  # 微博 App Key
SOCIAL_AUTH_WEIBO_SECRET = os.environ.get('APPSECRET')  # 微博 App Secret
# qq
# SOCIAL_AUTH_QQ_KEY = ''
# SOCIAL_AUTH_QQ_SECRET = ''
# 微信
# SOCIAL_AUTH_WEIXIN_KEY = ''
# SOCIAL_AUTH_WEIXIN_SECRET = ''

# 第三方登录成功后的跳转页面
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'
