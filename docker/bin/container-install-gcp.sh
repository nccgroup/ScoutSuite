#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# =====================================
# install gCloud SDK CLI Tools
# =====================================

WORKDIR=/root
TMPDIR=/tmp
cd ${TMPDIR}

echo -e "\n\ngCloud SDK Installation Starting...\n\n"

# add the gcp repo to apt
echo "deb [signed-by=/etc/apt/trusted.gpg.d/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list

# add the gcp pubkey to apt
curl https://packages.cloud.google.com./apt/doc/apt-key.gpg > /etc/apt/trusted.gpg.d/cloud.google.gpg

# install the sdk + kubectl + some extra python-related bits
apt-get update && apt-get install -y google-cloud-sdk google-cloud-sdk-app-engine-python google-cloud-sdk-app-engine-python-extras kubectl

# let folks know the install is done
echo -e "\n\ngCloud SDK Installation Complete!\n\n"
