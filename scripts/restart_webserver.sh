#!/usr/bin/env bash

PROJECT_ROOT=`python -c 'from pysis.settings import settings; print settings.PROJECT_ROOT'`

echo 'Stopping pysis_fcgi.py'
pkill -f pysis_fcgi.py

sleep 1

echo 'Starting pysis_fcgi.py'
python ${PROJECT_ROOT}/deploy/pysis_fcgi.py

