#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=True
export FLASK_RUN_CERT=./Certificates/mycert.pem
export FLASK_RUN_KEY=./Certificates/mykey.pem

nohup flask run >> Logs/nohup.out 2>&1 &
