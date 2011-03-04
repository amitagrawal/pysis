import os
import sys

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.split(THIS_DIR)[0]
PROJECT_PARENT = os.path.split(PROJECT_ROOT)[0]
PROJECT_NAME = os.path.split(PROJECT_ROOT)[1]

sys.path.append(PROJECT_PARENT)

# Assuming that your settings.py is at PROJECT_NAME/settings/settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT_NAME + '.settings.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
