#!/bin/sh

python cats/manage.py migrate
python cats/manage.py runserver 0.0.0.0:8000
tail -f /dev/null &
wait
