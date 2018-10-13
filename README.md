# Comet Competition Server

## Aims
1. Provide a way for users to enter competitions and get feedback on their submissions
2. Provide a means for competition organisers to collect submissions easily
3. Provide a publiclly accessable ranking system and API

## Requirements
* Django
* Django REST framework

## Getting Started
There are two supported methods for getting the app running, development mode with sqlite and staging/production mode with docker+postgresql.

### Development Setup
Assuming you have python and virtualenvwrapper installed:

```bash
# Setup your envrioment
pipenv install
pipenv shell

# export DJANGO_SETTINGS_MODULE=comet.settings.local or add --settings to the end of the command
# Create the database
./manage.py migrate --settings=comet.settings.local

# Create your super user account
./manage.py createsuperuser --settings=comet.settings.local

# Start server and setup oauth applications
./manage.py runserver 0.0.0.0:8000 --settings=comet.settings.local
# go to http://localhost:8000/admin and add your github, facebook and google tokens
```

### Deploying in production
For deployment in production, Docker is recommended. This will be provided once the application is ready for deployment.

#### Building the docker container
``` bash
docker build . -t webpigeon/comet:latest
docker push webpigeon/comet:latest
```

#### Running the docker container
TODO - just hints for now

* need to run ./manage.py collectstatic and ./manage.py migrate on first instance.
* need to create at least one admin using cli: ./manage.py createsuperuser
* expose /home/django/website/var/static to nginx for static files
* uploads are stored in /home/django/website/var/uploads by default (so should expose this to competition managers)
* before first "user" use, login to admin area and populate oauth logins for github, google+ and facebook.

#### Envrioment Variables
* SECRET_KEY - Django Secret key, required
* ALLOWED_HOSTS - hosts allowed to access the django server, required
* SSL_ONLY - set to True switch on SSL only mode (only send cookies over https)

#### Database envrioment variables
* DB_ENV_DB - database name (defaults to postgres)
* DB_ENV_POSTGRES_USER - postgres user (defaults to postgres)
* DB_ENV_POSTGRES_PASSWORD - postgres user password (defaults to blank)
* DB_ENV_HOST - postgres database hosename (defaults to DB)
