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
mkvirtualenv comp-server
activate comp-server
pip install -r

# Create the database
./manage.py migrate

# Create your super user account
./manage.py createsuperuser

# Start server and setup oauth applications
./manage.py runserver 0.0.0.0:8000
# go to http://localhost:8000/admin
```

### Deploying in production
For deployment in production, Docker is recommended. This will be provided once the application is ready for deployment.
