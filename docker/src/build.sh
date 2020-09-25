#!/bin/bash
echo -e "\n\nbuild running...\n"
source ../config/build.env

BUILD_CMD="docker build \
  -t ${IMAGE_NAME} \
  -t ${VENDOR}/${NAME}:${VERSION} \
  --build-arg VCS_REF=${VCS_REF} \
  --build-arg VCS_URL=${VCS_URL} \
  --build-arg VERSION=${VERSION} \
  --build-arg BUILD_DATE=${BUILD_DATE} \
  --build-arg NAME=${NAME} \
  --build-arg VENDOR=${VENDOR} \
  --build-arg IMAGE_NAME=${IMAGE_NAME} \
  ."
  # --build-arg DESCRIPTION=${DESCRIPTION} \
  
echo -e "\n\nbuilding image using:\n${BUILD_CMD}"
exec ${BUILD_CMD}