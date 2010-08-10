
import pysis.scripts.bootstrap_django

import os
import sys
from fabric.api import env, local, run
from django.conf import settings

env.hosts = [os.environ['MYSERVER']]

def test():
    # use test settings, not actual settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'pysis.settings.test_settings'
    os.environ['PYTHONPATH'] = '.:..:%s/apps' %  settings.PROJECT_ROOT
        
#    local('pylint ' +
#          '--reports=n ' +
#          '--disable=C,R,W ' +
#          settings.PROJECT_ROOT, capture=False)

    local('nosetests -v -d ' +
           '--with-doctest ' +
           '--with-django ' +
           '--with-djangoliveserver ' +
           '--with-selenium ', capture=False)

def deploy(skip_tests='no'):
    if skip_tests != 'yes':
        test()    
        
    master_repo = 'ssh://hg@bitbucket.org/dkmurthy/pysis'
    remote_repo = '/var/www/pysis'
    remote_env = '~/virtualenvs/pysis/bin/'
        
    local('hg push %s' % master_repo, capture=False)

    run('hg fetch -R %s %s' % (remote_repo, master_repo))
    run('%s/python %s/manage.py migrate myprofile' % (remote_env, remote_repo))
    run('source %s/activate && %s/scripts/restart_webserver.sh' % (remote_env, remote_repo))
    
    
    
    