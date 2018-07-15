import os

from . import BASE_DIR

try:
    from .secret import Secret
except ImportError:
    raise ImportError(
        'Failed to import Secret values.'
    )

# SECURITY WARNING: Keep them secret!
SECRET_KEY = Secret.SECRET_KEY
ALLOWED_HOSTS = Secret.ALLOWED_HOSTS
DATABASES = Secret.DATABASES
ADMIN_URL = Secret.ADMIN_URL

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # appended
    'django.contrib.sitemaps',  # appended
]

INSTALLED_APPS += [
    'mptt',
    'crispy_forms',
    'easy_thumbnails',
    'rakmai',
    'help',
    'blog',
    'board',
    'book',
    'voca',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# django.contrib.sites settings for allauth
SITE_ID = 1

# crispy-form template
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Bleach sanitizing text fragments
BLEACH_ALLOWED_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'ol', 'ul', 'li', 'div', 'p', 'code', 'blockquote', 'pre', 'span', 'table', 'thead',
    'tbody', 'tr', 'th', 'td', 'a', 'em', 'strong', 'hr', 'img'
]

BLEACH_ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'rel'],
    'img': ['alt', 'src'],
}
