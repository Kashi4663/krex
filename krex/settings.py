"""
Django settings for krex project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ==========================================================
# BASE DIRECTORY
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# SECURITY
# ==========================================================
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-dev-key")

DEBUG = False  # ⚠️ Change to False in production

ALLOWED_HOSTS = ['.onrender.com']

# ==========================================================
# APPLICATIONS
# ==========================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your App
    'krexapp',
]

# ==========================================================
# MIDDLEWARE
# ==========================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'krex.urls'

# ==========================================================
# TEMPLATES
# ==========================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required for navbar admin button
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'krexapp.context_processors.admin_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'krex.wsgi.application'

# ==========================================================
# DATABASE
# ==========================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================================================
# PASSWORD VALIDATION
# ==========================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================================================
# INTERNATIONALIZATION
# ==========================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # 🔥 Set to India (better for KREX)
USE_I18N = True
USE_TZ = True

# ==========================================================
# STATIC FILES
# ==========================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # if you create static folder
STATIC_ROOT = BASE_DIR / 'staticfiles'    # for production collectstatic

# ==========================================================
# MEDIA FILES (Movies, Posters, Episodes)
# ==========================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================================================
# DEFAULT PRIMARY KEY
# ==========================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================================
# OPENAI KEY (Optional Future AI Features)
# ==========================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LOGIN_URL = 'select_role'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'select_role'

import os

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'