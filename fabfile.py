from pysis.scripts import bootstrap_django
bootstrap_django.main()

import os
import sys
import fabric
from fabric.api import env
from django.conf import settings

env.hosts = [os.environ.get('MYSERVER')]

os.environ['DJANGO_SETTINGS_MODULE'] = 'pysis.settings.settings'
os.environ['PYTHONPATH'] = '.:..:%s/apps' %  settings.PROJECT_ROOT

env.master_repo = 'ssh://hg@bitbucket.org/sramana/pysis'
env.remote_repo = '/projects/pysis'
env.remote_env = '/work/virtualenvs/pysis/bin/'
env.django_settings = os.environ['DJANGO_SETTINGS_MODULE']

def local(cmd):
    fabric.api.local(cmd, capture=False)

def run(cmd):
    env.cmd = cmd
    fabric.api.run('source %(remote_env)s/activate && '
                   'export DJANGO_SETTINGS_MODULE=%(django_settings)s && '
                   'cd %(remote_repo)s && '
                   '%(cmd)s' % env
                  )

def run_pylint():
    local('pylint ' +
          # E1101 is a very useful message.
          # But I have to disable it because
          # pylint can not understand django's dynamic structure.
          # Should enable it back when pylint becomes more django friendly in future.
          '-d E1101 ' +
          '--reports=n ' +
          '--disable=C,R,W ' +
          settings.PROJECT_ROOT)


def run_nose():
    # use test settings, not actual settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'pysis.settings.test_settings'

    local('nosetests -v -d -x ' +
           '--with-doctest ' +
           '--with-django ' +
           '--with-djangoliveserver ' +
           '--with-selenium ')

def test():
    run_pylint()
    run_nose()

def test_on_server():
    run('fab -f scripts/fabfile.py test')

def push():
    local('hg push %(master_repo)s' % env)
    run('hg fetch %(master_repo)s' % env)

def install_requirements():
    run('pip install -r requirements/requirements.txt -q')

def upgrade_db():
    run('django-admin.py syncdb')
    run('django-admin.py migrate accounts')

def restart_webserver():
    run('sudo supervisorctl restart pysis')


def docs():
    with fabric.api.cd('docs'):
        local('make html')

    with fabric.api.cd('docs/_build/html'):
        if not os.path.exists('.git'):
            local('git init')
            local('git symbolic-ref HEAD refs/heads/gh-pages')
            local('touch .nojekyll')

        local('git add .')
        local('git commit -a -m "Auto-commit from fabfile" || echo')
        local('git push -f git@github.com:sramana/pysis.git gh-pages')


def deploy(skip_tests='no'):
    if skip_tests != 'yes':
        test()

    push()
    upgrade_db()
    install_requirements()
    restart_webserver()
    test_on_server()
