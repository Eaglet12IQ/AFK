"""
WSGI config for AFK project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os,sys
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/var/www/u2923516/data/www/afk.progfiks.ru/AFK/')
sys.path.insert(1, '/var/www/u2923516/data/www/afk.progfiks.ru/env/lib/python3.8/site-packages/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AFK.settings')

application = get_wsgi_application()