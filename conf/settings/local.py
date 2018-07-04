from django.utils.translation import ugettext_lazy as _

from .base import *

DEBUG = True

INSTALLED_APPS += [
    'rakmai',
]

# Internationalization
LANGUAGE_CODE = 'ko-kr'
LANGUAGES = [
    ('ko', _('Korean')),
    ('en', _('English')),
    ('th', _('Thai')),
]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_DIRS = [
]

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
