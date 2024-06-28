#!/bin/bash

service nginx start
exec gunicorn -c ./gunicorn.conf.py app:app