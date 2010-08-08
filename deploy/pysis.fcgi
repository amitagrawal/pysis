#!/usr/bin/env python

import os
import sys

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../")))
sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "settings.settings"

sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded",
           daemonize="false",
           minspare="1",
           maxspare="1",
           host="127.0.0.1",
           port="9009",
          )
