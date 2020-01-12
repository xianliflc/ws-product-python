#!/usr/bin/env bash

pip3 install flask-cors==3.0.7
# for dev
FLASK_APP=app.py FLASK_DEBUG=1 FLASK_ENV=development flask run
# for prod
# gunicorn app:app --log-file -
