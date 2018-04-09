#! /bin/bash
# build and push the docker image
set -e

docker build -t docker.io/fossgalaxy/comet .
docker push docker.io/fossgalaxy/comet
