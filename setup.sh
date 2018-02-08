#! /bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=comet.settings.local

./manage.py migrate
