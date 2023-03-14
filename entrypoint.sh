#!/bin/bash

while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do echo "En attente du demarrage de postgresql" && sleep 1; done
if ! PGPASSWORD=8Fny?aXEFkh9ePA3 psql -U postgres -h $POSTGRES_HOST -p $POSTGRES_PORT -lqt | cut -d \| -f 1 | cut -d ' ' -f 2 | grep -q "^pokedex$"; then
    PGPASSWORD=8Fny?aXEFkh9ePA3 createdb -U postgres -h $POSTGRES_HOST -p $POSTGRES_PORT pokedex
else
    echo "La database existe deja"
fi

mkdir -p /var/www/static && chown simadm:www-data /var/www/static
gosu simadm make migrate
gosu simadm ./manage.py collectstatic --noinput
exec gosu simadm uwsgi --http-socket :8030 --uid simadm --ini config_files/basic-docker.ini --processes 4 --threads 2 --wsgi-file pokedex-back/wsgi.py
