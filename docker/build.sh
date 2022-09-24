#!/bin/bash

SEP1="=============================="
SEP2="------------------------------"

echo -e "\n\n${SEP1}\n"
echo -e "\nBEGINNING BUILD...\n"

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

  "all")
    $0 base
    $0 aws
    $0 gcp
    $0 azure
  ;;

  *)
    echo -e "\nUsage: $0 [base | aws | gcp | azure | all ]"
    echo -e "Using default: base\n"
    $0 base
  ;;

esac

echo -e "\n${SEP1}\nBUILD COMPLETE!...\n"