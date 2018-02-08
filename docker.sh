#! /bin/bash
# build and push the docker image

docker build -t docker.io/fossgalaxy/comet .
docker push docker.io/fossgalaxy/comet
