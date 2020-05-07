#!/bin/bash
set -e
# This is run at ci, created an image that contains all the tools needed in
# databuild

ORG=${ORG:-opentransport}
DOCKER_IMAGE=gtfs-exporter

DOCKER_TAG="ci-${TRAVIS_COMMIT}"
# Set these environment variables
#DOCKER_USER=
#DOCKER_AUTH=

function tagandpush {
  docker tag $ORG/$1:$3$DOCKER_TAG $ORG/$1:$2
  docker push $ORG/$1:$2
}

function imagedeploy {
  if [ "$TRAVIS_PULL_REQUEST" = "false" ]; then

    docker login -u $DOCKER_USER -p $DOCKER_AUTH
    if [ "$TRAVIS_TAG" ];then
      echo "processing release $TRAVIS_TAG"
      #release do not rebuild, just tag
      docker pull $ORG/$1:$DOCKER_TAG
      tagandpush $1 "prod" ""
    else
      if [ "$TRAVIS_BRANCH" = "master" ]; then
        echo "processing master build $TRAVIS_COMMIT"
        #master branch, build and tag as latest
        docker build --tag="$ORG/$1:$DOCKER_TAG" .
        docker push $ORG/$1:$DOCKER_TAG
        tagandpush $1 "latest" ""
      elif [ "$TRAVIS_BRANCH" = "next" ]; then
        echo "processing master build $TRAVIS_COMMIT"
        #master branch, build and tag as latest
        docker build --tag="$ORG/$1:next-$DOCKER_TAG" .
        docker push $ORG/$1:next-$DOCKER_TAG
        tagandpush $1 "next" "next-"
      else
        #check if branch is greenkeeper branch
        echo Not Pushing greenkeeper to docker hub
        exit 0
      fi
    fi
  else
    echo "processing pr $TRAVIS_PULL_REQUEST"
    docker build --tag="$ORG/$1:$DOCKER_TAG" .
  fi
}

cd ${PWD} && imagedeploy "pfaedle"

echo Build completed