Installing
==========

For Users
-------------------

This software is not yet ready for production use.


For Developers
-------------------
.. note::
    In the following instructions, I am assuming that your OS is Ubuntu 10.04 or higher.

#. Install Python and Mercurial ::

    sudo apt-get install python mercurial

#. Install MySQL or PostgreSQL database along with headers. ::

    sudo apt-get install mysql-client mysql-server libmysqlclient-dev

    or

    sudo apt-get install postgresql-9.0  postgresql-server-dev-9.0

#. Install nginx webserver. ::

    sudo apt-get install nginx

#. Install supervisor. ::

    sudo apt-get install supervisor

#. Install pip. ::

    sudo easy_install setuptools pip

#. Install virtualenv. ::

    sudo pip install virtualenv virtualenvwrapper

#. Create directories for this project. ::

    sudo mkdir /virtualenvs
    sudo mkdir /projects

    sudo chmod 777 /virtualenvs
    sudo chmod 777 /projects

    mkdir /virtualenvs/download_cache


#. Add the following to your ~/.bashrc ::

    export WORKON_HOME=/virtualenvs
    export PIP_DOWNLOAD_CACHE=/virtualenvs/download_cache
    source /usr/local/bin/virtualenvwrapper.sh

#. Refresh your session to make the above changes visible. ::

    source ~/.bashrc

#. Create virtualenv. ::

    mkvirtualenv --no-site-packages pysis

#. Activate virtualenv. ::

    workon pysis

#. .. note ::
    From now on, I am assuming that you are inside the virtualenv. A Quick test : when you run "which python" and it should show "/virtualenvs/pysis/bin/python"

#. Clone pysis repository. ::

    hg clone http://bitbucket.org/sramana/pysis /projects/pysis

#. Add /projects to python path. ::

    add2virtualenv /projects

#. Install requirements. This will take some time. ::

    pip install -r /projects/pysis/requirements/requirements.txt

#. Add a shortcut to manage the project. Edit your ~/.bashrc and add this line. ::

    source /projects/pysis/scripts/shortcuts.sh

#. Refresh your session to make the above changes visible. ::

    source ~/.bashrc

#. Edit /projects/pysis/settings/production_settings.py and provide your database credentials under DATABASES.

#. Create tables. ::

    django-admin.py syncdb
    django-admin.py migrate core

#. Add the nginx configuration. ::

    sudo touch /etc/nginx/common_server_options.nginx.conf
    sudo ln -s /projects/pysis/deploy/pysis_nginx.conf /etc/nginx/sites-enabled/
    sudo ln -s /projects/pysis/media /var/www/pysis_media

#. Restart nginx. ::

    sudo service nginx restart

#. Add this project to supervisor. Edit /etc/supervisor/supervisord.conf and add the following lines to the bottom. ::

    [program:pysis]
    command=/virtualenvs/pysis/bin/python /projects/pysis/deploy/pysis_fcgi.py
    user=www-data

#. Reload supervisor. ::

    sudo supervisorctl reload

#. Run "pysis" and make sure that no errors are reported.

#. Add "127.0.1.1 pysis.localhost" to /etc/hosts.


#. Now point your browser to http://pysis.localhost and enjoy.
