"""ALLOWED_HOSTS для модуля Settings."""


import os

allowed_host = os.environ.get('ALLOWED_HOSTS')
if not allowed_host:
    allowed_host = ''

ALLOWED_HOSTS = [
    host.strip() for host in allowed_host.split(',')
]
