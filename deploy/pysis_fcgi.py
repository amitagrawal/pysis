#!/usr/bin/env python

import pysis.scripts.bootstrap_django

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded",
           minspare="1",
           maxspare="1",
           host="127.0.0.1",
           port="9009",
          )
