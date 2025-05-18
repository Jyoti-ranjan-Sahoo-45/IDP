#!/bin/bash

NAME="idp_project"
DIR=/path/to/idp_project
USER=user
GROUP=user
WORKERS=3
BIND=unix:/path/to/idp_project/run/gunicorn.sock
DJANGO_SETTINGS_MODULE=idp_project.settings
DJANGO_WSGI_MODULE=idp_project.wsgi
LOG_LEVEL=error

cd $DIR
source ../venv/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec ../venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=- 