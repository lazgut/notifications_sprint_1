"""Application definition для модуля settings."""

import os

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notification.apps.NotificationConfig',
]

if os.environ.get('DEBUG', False) == 'True':
    INSTALLED_APPS += ['debug_toolbar']
