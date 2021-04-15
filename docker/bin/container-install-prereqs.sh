#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# =====================================
# install software packages needed for
# all the other components to run
# =====================================

WORKDIR=/root
TMPDIR=/tmp
cd ${TMPDIR}

echo -e "\n\nSoftware Pre-reqs Installation Starting...\n\n"

# =====================================
# set up the pre-reqs
# =====================================
apt-get update > /dev/null 2>&1
apt-get install -qy \
  apt-transport-https \
  apt-utils \
  ca-certificates \
  cmake \
  curl \
  dialog \
  gnupg \
  groff \
  jq \
  less \
  lsb-release \
  nano \
  python3 \
  python3-pip \
  tzdata \
  unzip \
  vim \
  virtualenv \
  virtualenvwrapper \
  wget

echo -e "\n\nSoftware Pre-reqs Installation Complete!\n\n"
