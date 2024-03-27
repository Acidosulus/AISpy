#!/bin/bash

#source ./env/bin/activate
#flask run --host=0.0.0.0 --debug
export FLASK_RUN_DEBUG=0
export FLASK_RUN_RELOAD=1
flask run --host=0.0.0.0

#celery -A main.celery worker --loglevel=info -E


#source ./env/bin/deactivate