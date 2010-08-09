""" This module sets up django environment so that other scripts need not worry about these mundane tasks.

"""

try:
    from pysis.settings import settings
except ImportError:
    try:
        from pysis import settings
    except ImportError:
        import sys
        sys.stderr.write('Can not find settings module. \n Aborting...')
        sys.exit(1)

from django.core.management import setup_environ
setup_environ(settings)
