#!/usr/bin/env bash

echo $DJANGO_SETTINGS_MODULE

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=4
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=8000
fi

if [ -z "${GUNICORN_TIMEOUT}" ]; then
    GUNICORN_TIMEOUT=120
fi

if [ "${GUNICORN_RELOAD}" ]; then
    GUNICORN_RELOAD="--reload"
else
    GUNICORN_RELOAD=""
fi

set -x

python manage.py migrate

if [ "${CACHE_BACKEND:-""}" == "django.core.cache.backends.db.DatabaseCache" ]; then
    echo "Database cache set; creating cache table"
    python manage.py createcachetable
fi

if [ -z "${IS_CRON_POD}" ]; then
    if [ "${PTVSD_ENABLE:-"False"}" == "False" ]; then
        # Start Gunicorn processes
        echo Starting Gunicorn for production

        # application pod
        exec gunicorn student_explorer.wsgi:application \
            --bind 0.0.0.0:${GUNICORN_PORT} \
            --workers="${GUNICORN_WORKERS}" \
            --timeout="${GUNICORN_TIMEOUT}" \
            ${GUNICORN_RELOAD}
    else
        # Currently ptvsd doesn't work with gunicorn
        # https://github.com/Microsoft/vscode-python/issues/2138
        echo Starting Runserver for development
        export PYTHONPATH="/usr/src/app:$PYTHONPATH"
        export DJANGO_SETTINGS_MODULE=student_explorer.settings
        exec django-admin runserver --ptvsd 0.0.0.0:${GUNICORN_PORT}
    fi
else
    if [ -z "${CRONTAB_SCHEDULE}" ]; then
        echo "CRONTAB_SCHEDULE environment variable not set, crontab cannot be started. Please set this to a crontab acceptable format."
    else
        # in cron pod
        echo Running cron job pod
        echo "CRONTAB_SCHEDULE is ${CRONTAB_SCHEDULE}, RUN_AT_TIMES is ${RUN_AT_TIMES}"

        # Make the log file available
        touch /var/log/cron.log

        # Get the environment from docker saved
        # https://ypereirareis.github.io/blog/2016/02/29/docker-crontab-environment-variables/
        printenv | sed "s/^\([a-zA-Z0-9_]*\)=\(.*\)$/export \1='\2'/g" >> $HOME/.profile

        echo "${CRONTAB_SCHEDULE} . $HOME/.profile; python /usr/src/app/manage.py runcrons >> /var/log/cron.log 2>&1" | crontab
        crontab -l && cron -L 15 && tail -f /var/log/cron.log
    fi
fi
