#!/bin/bash

# vars are stored in .env and config/base.env files
# note that the FROM used in the Dockerfile files
# needs to be updated to match the version in the env
# files in order for anything other than the base image
# to build correctly.
# TODO: fix this so that the FROM is set in the Dockerfile
# automatically by the env vars

SEP1="=============================="
SEP2="------------------------------"

echo -e "\n\n${SEP1}"
echo -e "BEGINNING BUILD..."

case $1 in

  "base")
    #####################
    #### BASE IMAGE  ####
    #####################
    echo -e "\n${SEP2}\nbuilding base image...\n"
    source ./config/base.env

    BUILD_CMD="docker build \
    -f Dockerfile-base \
    -t ${IMAGE_NAME} \
    --build-arg BUILD_DATE=${BUILD_DATE} \
    --build-arg NAME=${NAME} \
    --build-arg VCS_REF=${VCS_REF} \
    --build-arg VCS_URL=${VCS_URL} \
    --build-arg VENDOR=${VENDOR} \
    --build-arg VERSION=${VERSION} \
    --build-arg IMAGE_NAME=${IMAGE_NAME} \
    ."

    echo -e "\n\nbuilding image using:\n${BUILD_CMD}"
    exec ${BUILD_CMD}
    echo -e "\nbase image build complete!\n${SEP2}\n"
  ;;

  "aws")
    #####################
    ####  AWS IMAGE  ####
    #####################

    echo -e "\n${SEP2}\nbuilding aws image...\n"
    source ./config/base.env
    source ./config/aws.env

    BUILD_CMD="docker build \
    -f Dockerfile-aws \
    -t ${IMAGE_NAME} \
    --build-arg BUILD_DATE=${BUILD_DATE} \
    --build-arg NAME=${NAME} \
    --build-arg VCS_REF=${VCS_REF} \
    --build-arg VCS_URL=${VCS_URL} \
    --build-arg VENDOR=${VENDOR} \
    --build-arg VERSION=${VERSION} \
    --build-arg IMAGE_NAME=${IMAGE_NAME} \
    ."

    echo -e "\n\nbuilding image using:\n${BUILD_CMD}"
    exec ${BUILD_CMD}
    echo -e "\naws image build complete!\n${SEP2}\n"
  ;;

  "gcp")
    #####################
    ####  GCP IMAGE  ####
    #####################

    echo -e "\n${SEP2}\nbuilding gcp image...\n"
    source ./config/base.env
    source ./config/gcp.env

    BUILD_CMD="docker build \
    -f Dockerfile-gcp \
    -t ${IMAGE_NAME} \
    --build-arg BUILD_DATE=${BUILD_DATE} \
    --build-arg NAME=${NAME} \
    --build-arg VCS_REF=${VCS_REF} \
    --build-arg VCS_URL=${VCS_URL} \
    --build-arg VENDOR=${VENDOR} \
    --build-arg VERSION=${VERSION} \
    --build-arg IMAGE_NAME=${IMAGE_NAME} \
    ."

    echo -e "\n\nbuilding image using:\n${BUILD_CMD}"
    exec ${BUILD_CMD}
    echo -e "\ngcp image build complete!\n${SEP2}\n"
  ;;

  "azure")
    #####################
    #### AZURE IMAGE ####
    #####################
    echo -e "\n${SEP2}\nbuilding azure image...\n"
    source ./config/base.env
    source ./config/azure.env

    BUILD_CMD="docker build \
    -f Dockerfile-azure \
    -t ${IMAGE_NAME} \
    --build-arg BUILD_DATE=${BUILD_DATE} \
    --build-arg NAME=${NAME} \
    --build-arg VCS_REF=${VCS_REF} \
    --build-arg VCS_URL=${VCS_URL} \
    --build-arg VENDOR=${VENDOR} \
    --build-arg VERSION=${VERSION} \
    --build-arg IMAGE_NAME=${IMAGE_NAME} \
    ."

    echo -e "\n\nbuilding image using:\n${BUILD_CMD}"
    exec ${BUILD_CMD}
  ;;

  "combined")
    #####################
    ## COMBINED IMAGE  ##
    #####################
    echo -e "\n${SEP2}\nbuilding combined image...\n"
    source ./config/base.env
    source ./config/combined.env

    BUILD_CMD="docker build \
    -f Dockerfile \
    -t ${IMAGE_NAME} \
    --build-arg BUILD_DATE=${BUILD_DATE} \
    --build-arg NAME=${NAME} \
    --build-arg VCS_REF=${VCS_REF} \
    --build-arg VCS_URL=${VCS_URL} \
    --build-arg VENDOR=${VENDOR} \
    --build-arg VERSION=${VERSION} \
    --build-arg IMAGE_NAME=${IMAGE_NAME} \
    ."

    echo -e "\n\nbuilding image using:\n${BUILD_CMD}"
    exec ${BUILD_CMD}
    echo -e "\nbase image build complete!\n${SEP2}\n"
  ;;

  "all")
    $0 base
    $0 aws
    $0 gcp
    $0 azure
  ;;

  *)
    echo -e "\nBUILD TARGET NOT FOUND!"
    echo -e "\nUSAGE:\n  $0 [base | aws | gcp | azure | all ]"
    echo -e "${SEP1}"
    exit 1
    # echo -e "Using default: all\n"
    # $0 all
  ;;

esac

echo -e "\n${SEP1}\nBUILD COMPLETE!...\n"