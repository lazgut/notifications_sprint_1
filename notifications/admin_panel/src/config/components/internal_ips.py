"""INTERNAL_IPS для модуля settings."""

import os

if os.environ.get('DEBUG', False) == 'True':
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind('.')] + '.4' for ip in ips] + ['127.0.0.1', '10.0.2.2']
