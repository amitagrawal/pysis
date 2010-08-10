import os
import sys
from fabric.api import env, local, run

import pysis.scripts.bootstrap_django
from django.conf import settings

env.hosts = [os.environ['MYSERVER']]

def test():
    #local('pylint ' +
          #'--reports=n ' +
          #'--disable=C,R,W ' +
          #settings.PROJECT_ROOT, capture=False)

    local('nosetests -v -d ' +
           '--with-doctest ' +
           '--with-django ' +
           '--with-djangoliveserver ' +
           '--with-selenium ', capture=False)
