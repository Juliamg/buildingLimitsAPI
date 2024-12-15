#!/bin/bash
set -e
cd "${0%/*}"

# Env variables that can be set in a github action workflow
TAG="latest"
IMAGE="building-limits-service"
BUILDER_VER="0.4.160"

echo "Building image $IMAGE:$TAG"

  pack build "$IMAGE:$TAG" --buildpack paketo-buildpacks/python \
                           --builder paketobuildpacks/builder-jammy-base:$BUILDER_VER \
                           --buildpack paketo-buildpacks/source-removal \
                           --env BPE_APPEND_LD_LIBRARY_PATH=:/workspace/libs \
                           --path  app/ \
                           --env "DB_CONNECTION_STRING" # Get this from a key vault or github secrets in the ci github workflow
