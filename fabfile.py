from fabric.contrib import django
django.settings_module('pysis.settings.settings')

import os
import fabric
from fabric.api import env, local, sudo, cd, prefix
from django.conf import settings

env.hosts = [os.environ.get('MYSERVER')]

os.environ['PYTHONPATH'] = '.:..:%s/apps' %  settings.PROJECT_ROOT

env.master_repo = 'ssh://hg@bitbucket.org/sramana/pysis'
env.remote_env = '/work/virtualenvs/pysis/bin/'
env.project_root = '/work/pysis'


def run(cmd):
    with cd(env.project_root):
        with prefix('workon pysis'):
            fabric.api.run(cmd)


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
    django.settings_module('pysis.settings.test_settings')

    local('nosetests -v -d -x ' +
           '--with-doctest ' +
           '--with-django ' +
           '--with-djangoliveserver ' +
           '--with-selenium ' +
           'apps tests')


def test():
    run_pylint()
    run_nose()


def test_on_server():
    run('fab test')


def push():
    local('hg push %(master_repo)s' % env)
    run('hg fetch %(master_repo)s' % env)


def install_requirements():
    run('pip install -r requirements/requirements.txt -q')


def upgrade_db():
    run('./manage.py syncdb')
    run('./manage.py migrate accounts')


def deploy_static():
    run('./manage.py collectstatic -v0 --noinput')


def restart_webserver():
    sudo('supervisorctl restart pysis')


def docs():
    with cd('docs'):
        local('make html')

    with cd('docs/_build/html'):
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
    install_requirements()
    upgrade_db()
    deploy_static()
    restart_webserver()
    test_on_server()
