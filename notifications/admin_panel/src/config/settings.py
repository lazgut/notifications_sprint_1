"""Django settings for config project."""

import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/allowed_hosts.py',
    'components/auth_password_validators.py',
    'components/database.py',
    'components/installed_apps.py',
    'components/internal_ips.py',
    'components/logging.py',
    'components/middleware.py',
    'components/templates.py',
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = './static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
