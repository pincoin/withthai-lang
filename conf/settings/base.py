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
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.kakao',
    # 'allauth.socialaccount.providers.naver',
]

INSTALLED_APPS += [
    'django_otp',
    'django_otp.plugins.otp_totp',
    'mptt',
    'crispy_forms',
    'easy_thumbnails',
    'rakmai',
    'member',
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
    'django_otp.middleware.OTPMiddleware',  # Google OTP
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Django default
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth
)

# django.contrib.sites settings for allauth
SITE_ID = 1

# django.contrib.auth settings for allauth
PASSWORD_RESET_TIMEOUT_DAYS = 1  # default=3
LOGIN_URL = '/accounts/login/'  # default=/accounts/login/
LOGOUT_URL = '/accounts/logout/'  # default=/accounts/logout/
LOGIN_REDIRECT_URL = '/'  # default=/accounts/profile/
# LOGOUT_REDIRECT_URL = '/'

# django-allauth
DEFAULT_FROM_EMAIL = Secret.EMAIL_NO_REPLY
# ACCOUNT_ADAPTER = 'member.adapters.MyAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# ACCOUNT_SIGNUP_FORM_CLASS = 'member.forms.MemberSignupForm'
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True  # default=False
SOCIALACCOUNT_AUTO_SIGNUP = False

# Social providers for django-allauth
# Each key has an empty dictionary value that will eventually contain provider specific configuration options by admin
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {},
    'google': {},
    'kakao': {},
    'naver': {},
}

# crispy-form template
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Bleach sanitizing text fragments
BLEACH_ALLOWED_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'ol', 'ul', 'li', 'div', 'p', 'code', 'blockquote', 'pre', 'span', 'table', 'thead',
    'tbody', 'tr', 'th', 'td', 'a', 'em', 'strong', 'hr', 'img', 'br',
]

BLEACH_ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'rel'],
    'img': ['alt', 'src'],
}

# Caching
CACHE_TIME_LONG = 3600
CACHE_TIME_SHORT = 300
CACHE_TIME_VERY_SHORT = 60

# Email Setup
EMAIL_HOST = Secret.EMAIL_HOST
EMAIL_HOST_USER = Secret.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = Secret.EMAIL_HOST_PASSWORD
EMAIL_PORT = Secret.EMAIL_PORT
EMAIL_USE_TLS = Secret.EMAIL_USE_TLS
EMAIL_NO_REPLY = Secret.EMAIL_NO_REPLY
EMAIL_CUSTOMER_SERVICE = Secret.EMAIL_CUSTOMER_SERVICE
