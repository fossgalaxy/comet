#! /bin/bash
##
# build and push the docker image
#
# This is a modified version of the Hanabi reproducable build script.
##
set -e

VERSION=1.0.0
SUBJECT=webpigeon

IMAGE_NAME=fossgalaxy/comet

##
# Sanity Check: run pipenv checks to make sure we don't deploy broken stuff.
##
export DJANGO_SETTINGS_MODULE=comet.settings.local
#pipenv check # NO LONGER POSSIBLE
pipenv sync

##
# Sanity Check: run django checks to ensure we've not got issues with model versions
##
pipenv run ./manage.py check

##
# Sanity Check: figure out if we're running off a 'clean' repo
##
if [[ -n $(git status -s) ]]
then
	echo "[ERROR] working directory not clean, aborting build"
	exit 1
fi

##
# Build phase: figure out what build engine to use
##
BUILD_TYPE="unknown"

if [ -f /bin/buildah ]; then
	echo "we're building with buildah";
	BUILD_TYPE=buildah
elif [ -f /bin/docker ]; then
	echo "we're building with docker";
        BUILD_TYPE=docker
else
	echo "[ERROR] couldn't find a container builder, aborting.";
	exit 1;
fi

# grab the commit ID
GIT_COMMIT=$(git rev-parse HEAD)
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') 

# attempt the build
case $BUILD_TYPE in
	"buildah")
		buildah bud --label $IMAGE_NAME -t snapshot .
		;;
	"docker")
		systemctl start docker
		docker build -t comet-build --build-arg GIT_COMMIT=$GIT_COMMIT --build-arg BUILD_VERSION=$GIT_COMMIT --build-arg BUILD_DATE=$BUILD_DATE .
		docker tag comet-build docker.io/$IMAGE_NAME:snapshot
		;;
esac


if [ -f /bin/buildah ]; then
	buildah bud --label fossgalaxy/comet -t snapshot .
	#buildah push fossgalaxy/comet:snapshot docker://docker.io/fossgalaxy/comet:snapshot
else
	docker push docker.io/fossgalaxy/comet:snapshot
fi
