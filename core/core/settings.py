"""
Django settings for core project.
Generated for Docker/PostgreSQL/Nginx Environment.
Architect: IRONKAGE
"""

import os
from pathlib import Path

# ==========================================
# 1. Визначаємо базову директорію проекту
# ==========================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# 2. Безпека: Секретний ключ та Debug
# ==========================================
# Краще тримати в .env, але додамо fallback для розробки
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-debug-key-12345')

# Режим відладки (Читаємо з .env, за замовчуванням увімкнено для тестів)
DEBUG = int(os.environ.get('DEBUG', 1))

# Дозволені хости (Критично важливо для Nginx та Gunicorn всередині Docker)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,django').split(',')

# ==========================================
# 3. Додатки та Middleware
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Тут можна додати свої додатки
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# ==========================================
# 4. Конфігурація Бази Даних (PostgreSQL)
# ==========================================
# Дані автоматично підтягуються з вашого файлу .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'django_db'),
        'USER': os.environ.get('POSTGRES_USER', 'db_admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'strong_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# ==========================================
# 5. Валідація паролів та Локалізація
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Налаштування української мови та часового поясу
LANGUAGE_CODE = 'uk-ua'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================================
# 6. СТАТИЧНІ ФАЙЛИ (Налаштування для Nginx)
# ==========================================
STATIC_URL = 'static/'

# Папка, куди Django збере всі файли для Nginx під час команди collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
