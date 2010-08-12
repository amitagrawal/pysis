
from pysis.scripts import bootstrap_django
bootstrap_django.main()

import os
import sys
from fabric.api import env, local, run
from django.conf import settings

env.hosts = [os.environ.get('MYSERVER')]

def test():
    # use test settings, not actual settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'pysis.settings.test_settings'
    os.environ['PYTHONPATH'] = '.:..:%s/apps' %  settings.PROJECT_ROOT

    local('pylint ' +
          # E1101 is a very useful message.
          # But I have to disable it because
          # pylint can not understand django's dynamic structure.
          # Should enable it back when pylint becomes more django friendly in future.
          '-d E1101 ' +
          '--reports=n ' +
          '--disable=C,R,W ' +
          settings.PROJECT_ROOT, capture=False)

    local('nosetests -v -d -x ' +
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
    run('source %s/activate && pip install -r %s/requirements/requirements.txt -q' % (remote_env, remote_repo))
    run('%s/python %s/manage.py migrate myprofile' % (remote_env, remote_repo))
    run('source %s/activate && cd %s && fab -f %s/scripts/fabfile.py test ' % (remote_env, remote_repo, remote_repo))
    run('source %s/activate && %s/scripts/restart_webserver.sh' % (remote_env, remote_repo))



