#!/bin/bash

source ./env/bin/activate
flask run --host=0.0.0.0 --debug
source ./env/bin/deactivate