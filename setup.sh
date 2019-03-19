#! /bin/bash
##
# Comet Local Setup Script
##
set -e

command -v pipenv || { echo "Couldn't find pipenv - do you have it installed and on your path?"; exit 1; }

# do the python stuff
export DJANGO_SETTINGS_MODULE=comet.settings.local
pipenv sync
pipenv run ./manage.py migrate

# tell the user we finished
if [ $# -ge 1 ]; then
	case "$1" in
		"serve") pipenv run ./manage.py runserver ;;
		"makemigrations") pipenv run ./manage.py makemigrations ;;
	esac
else
	echo ""
	echo "all done. If this is a new install, you'll need to create an admin account using:"
	echo ""
	echo "export DJANGO_SETTINGS_MODULE=comet.settings.local"
	echo "pipenv run ./manage.py createsuperuser"
	echo ""
fi
