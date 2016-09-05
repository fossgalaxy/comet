FROM python:3.5
ENV PYTHONUNBUFFERED 1

# Setup webserver
RUN pip install uwsgi psycopg2
#RUN apt-get update && apt-get install -y npm nodejs-legacy
#RUN npm install -g bower

# setup enviroment
RUN adduser --disabled-password --gecos "" django
RUN mkdir -p /home/django/website
RUN chown -R django:django /home/django/website

# install requirements
WORKDIR /home/django/website/
ADD requirements.txt /home/django/website/
RUN pip install -r requirements.txt

# Drop to non-root and setup django
USER django

WORKDIR /home/django/website/
RUN mkdir -p var/{static,uploads}
ADD . /home/django/website/

EXPOSE 8000
VOLUME ["/home/django/website/var/uploads", "/home/django/website/var/static"]
CMD ["uwsgi", "--ini", "/home/django/website/.docker/uwsgi.ini"]
