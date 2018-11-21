#! /bin/bash
# build and push the docker image
set -e

if [ -f /bin/buildah ]; then
	buildah bud --label fossgalaxy/comet -t snapshot .
	#buildah push fossgalaxy/comet:snapshot docker://docker.io/fossgalaxy/comet:snapshot
else
	docker build -t docker.io/fossgalaxy/comet .
	docker push docker.io/fossgalaxy/comet
fi
