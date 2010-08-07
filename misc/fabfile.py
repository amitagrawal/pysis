import os
import sys
from fabric.api import env, local, run


from os.path import abspath, dirname, join
from site import addsitedir

os.environ['PYTHONPATH'] = '.;..;..;..;../apps;../settings'

sys.path.insert(0, abspath(join(dirname(__file__), "../")))
sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "settings.settings"

sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

#from settings import settings
#from django.core.management import setup_environ
#setup_environ(settings)

env.hosts = [os.environ['MYSERVER']]

def setup():
    # mkvirtualenv --no-site-packages pysis
    # pip install -r requirements/requirements.txt --download-cache=~/virtualenvs/download_cache

    #local('pip install -E pysis -r requirements/requirements.txt --download-cache=~/virtualenvs/download_cache')
    pass

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
