import os
import environ
from pathlib import Path
from datetime import timedelta

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, [])
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "unfold",    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'rest_framework',
    'rest_framework_simplejwt',

    'api',
    'apps.accounts',
    'apps.todo',
    'apps.Profile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL     = 'accounts.Account'
LOGIN_URL           = 'login_view'
ROOT_URLCONF        = 'tasko.urls'


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


WSGI_APPLICATION = 'tasko.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_FILES = BASE_DIR / "plugins/static"
STATIC_ROOT = BASE_DIR / "plugins/assets"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
# "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "JTI_CLAIM"                 : "jti",    
    "UPDATE_LAST_LOGIN"         : True,
    "BLACKLIST_AFTER_ROTATION"  : False,
    "ROTATE_REFRESH_TOKENS"     : False,
    "ALGORITHM"                 : "HS256",
    'USER_ID_FIELD'             : 'id',
    "SIGNING_KEY"               : SECRET_KEY,
    "AUTH_HEADER_TYPES"         : ("Bearer",),
    "AUTH_HEADER_NAME"          : "HTTP_AUTHORIZATION",

    "REFRESH_TOKEN_LIFETIME"    : timedelta(days=2),
    "ACCESS_TOKEN_LIFETIME"     : timedelta(days=1, minutes=30),
    "TOKEN_TYPE_CLAIM"          : "token_type",
    "TOKEN_USER_CLASS"          : "rest_framework_simplejwt.models.TokenUser",
    "AUTH_TOKEN_CLASSES"        : ("rest_framework_simplejwt.tokens.AccessToken",),
    "USER_AUTHENTICATION_RULE"  : "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}
DJOSER = {    
    "SET_USERNAME_RETYPE"                   : True,
    "SET_PASSWORD_RETYPE"                   : True,
    "SEND_ACTIVATION_EMAIL"                 : True,
    "SEND_CONFIRMATION_EMAIL"               : True,
    "USER_CREATE_PASSWORD_RETYPE"           : True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION"   : True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION"   : True,    
    "LOGIN_FIELD"                           : "email",
    "USER_ID_FIELD"                         : "user_id,",
    "ACTIVATION_URL"                        : "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL"            : "password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL"            : "email/reset/confirm/{uid}/{token}",
    
    "SERIALIZERS": {
        'user_create'   : 'apps.accounts.api.serializers.UserRegistrationSerializer',
        'user'          : 'apps.accounts.api.serializers.UserProfileSerializer',
        'user_delete'   : 'djoser.serializers.UserDeleteSerializer',
    },
}

CORS_ALLOW_HEADERS = (
    "accept",
    "Authorization",
    "content-Type",
)

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Tasko API',
    'DESCRIPTION': 'Project tasks management tool',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'COMPONENT_SPLIT_REQUEST': True
}

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS