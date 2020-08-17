#!/bin/bash

# =====================================
# install gCloud SDK CLI Tools
# =====================================
# AUTHOR: jason.ross@nccgroup.com
# VERSION: 0.1.0
# =====================================
export DEBIAN_FRONTEND=noninteractive

WORKDIR=/root
TMPDIR=/tmp
cd ${TMPDIR}

echo -e "\n\ngCloud SDK Installation Starting...\n\n"

# add the gcp repo to apt
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list

# add the gcp pubkey to apt
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# install the sdk + some extra python-related bits
apt-get update && apt-get install -y google-cloud-sdk google-cloud-sdk-app-engine-python google-cloud-sdk-app-engine-python-extras

# let folks know the install is done
echo -e "\n\ngCloud SDK Installation Complete!\n\n"
