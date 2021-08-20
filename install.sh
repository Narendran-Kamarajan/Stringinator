#!/bin/bash

# This assumes you have python3 installed.  If not you will need it!

python3 -m venv venv
source venv/bin/activate && python3 -m pip install --upgrade pip && pip install -r requirements.txt
