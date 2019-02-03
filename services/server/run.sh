#!/bin/bash
set -e

if [ -f ./run-pre.sh ]; then
    ./run-pre.sh
fi

args=("$@")

case $1 in
    manage)
        # export DJANGO_SETTINGS_MODULE=conf.production
        exec python manage.py ${args[@]:1}
        ;;
    run)
        # export DJANGO_SETTINGS_MODULE=conf.production
        exec gunicorn conf.wsgi -b 0.0.0.0:8000 -w 4
        ;;
    develop-manage)
        # export DJANGO_SETTINGS_MODULE=conf.development
        exec python manage.py ${args[@]:1}
        ;;
    develop-run)
        # export DJANGO_SETTINGS_MODULE=conf.development
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    *)
        if [ -f ./run-extras.sh ]; then
            ./run-extras.sh ${args[@]}
        else
            exec "$@"
        fi
        ;;
esac