#!/usr/bin/env python

from pysis.scripts import bootstrap_django
bootstrap_django.main()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line()
