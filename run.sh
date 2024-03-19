#!/bin/bash

#source ./env/bin/activate
flask run --host=0.0.0.0 --debug

#celery -A designerUL worker --loglevel=info -E

#source ./env/bin/deactivate