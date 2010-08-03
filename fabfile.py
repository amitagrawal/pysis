import os
import sys
from fabric.api import env, local, run

from django.core.management import setup_environ
from settings import settings

setup_environ(settings)
os.environ['PYTHONPATH'] = '.:..:apps'

env.hosts = [os.environ['MYSERVER']]

def setup():
    # mkvirtualenv --no-site-packages pysis
    # pip install -r requirements/requirements.txt --download-cache=~/virtualenvs/download_cache
    
    local('pip install -E pysis -r requirements/requirements.txt --download-cache=~/virtualenvs/download_cache')

def test():
    local('pylint ' +
          '--reports=n ' +
          '--disable=C,R,W ' +
          settings.PROJECT_ROOT, capture=False)

    local('nosetests -v -d ' +
           '--with-doctest ' +
           '--with-django ' +
           '--with-djangoliveserver ' +
           '--with-selenium ', capture=False)
