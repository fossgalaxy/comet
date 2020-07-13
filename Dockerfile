FROM python:3
LABEL maintainer="joseph@webpigeon.me.uk"
ENV PYTHONUNBUFFERED 1

ARG BUILD_DATE
ARG BUILD_VERSION
ARG GIT_COMMIT=unspecified

# Label Schema
LABEL org.label-schema.schema-version=1.0
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="fossgalaxy/comet"
LABEL org.label-schema.description="website for running accademic competitions"
#LABEL org.label-schema.url="https://www.fossgalaxy.com/projects/comet"
LABEL org.label-schema.vcs-url="https://git.fossgalaxy.com/iggi/Comet/"
LABEL org.label-schema.vcs-ref=$GIT_COMMIT
LABEL org.label-schema.vendor="fossgalaxy"
LABEL org.label-schema.version=$BUILD_VERSION

# Setup webserver
RUN pip install uwsgi psycopg2 pipenv
#RUN apt-get update && apt-get install -y npm nodejs-legacy
#RUN npm install -g bower

# setup enviroment
RUN adduser --disabled-password --gecos "" django
RUN mkdir -p /home/django/website
RUN mkdir -p /home/django/website/var/static
RUN mkdir -p /home/django/website/var/uploads
RUN chown -R django:django /home/django/website

# install requirements
WORKDIR /home/django/website/
ADD Pipfile /home/django/website/
ADD Pipfile.lock /home/django/website/
RUN pipenv install --system

# Drop to non-root and setup django
USER django
ADD . /home/django/website/

EXPOSE 8000
CMD ["uwsgi", "--ini", "/home/django/website/.docker/uwsgi.ini"]
