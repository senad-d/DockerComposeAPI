#!/bin/sh

nginx
exec gunicorn -c ./gunicorn.conf.py app:app
