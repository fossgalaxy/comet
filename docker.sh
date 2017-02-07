#! /bin/bash
# build and push the docker image

docker build -t fossgalaxy/comet .
docker push fossgalaxy/comet
