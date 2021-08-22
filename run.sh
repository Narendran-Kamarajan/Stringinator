#!/bin/bash

# Set environmental variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=True
export FLASK_RUN_CERT=./Certificates/mycert.pem
export FLASK_RUN_KEY=./Certificates/mykey.pem

cd $(dirname "$1")

# Verify the availability of application

runCheck=$(lsof -i :$FLASK_RUN_PORT > /dev/null; echo $?)
if [[ $runCheck -eq 0 ]]
then
    echo "INFO::Stringinator App is available"
    grep "Running on" ./Logs/nohup.out | awk -F'(' '{print $1}'
    exit 0
fi

# Intall/verify package pre-requisites in virtual environment

. ./install.sh >> ./Logs/nohup.out 2>&1
sed -i 's/Running\ on/\Started\ on/g' ./Logs/nohup.out
nohup flask run >> ./Logs/nohup.out 2>&1 & # Start the application

sleep 5 # Allow process to allocate resources
runCheck=$(lsof -i :$FLASK_RUN_PORT > /dev/null; echo $?)
if [[ $runCheck -eq 0 ]]
then
    echo "INFO::Stringinator App is started"
    grep "Running on" ./Logs/nohup.out | awk -F'(' '{print $1}'
    pytest ./test.py >> ./Logs/nohup.out
else
    echo "ERROR::Unable to start Stringinator App"
    exit 1
fi
