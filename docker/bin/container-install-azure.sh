#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# =====================================
# install the Azure CLI Tools
# =====================================

WORKDIR=/root
TMPDIR=/tmp
cd ${TMPDIR}

echo -e "\n\nAzure CLI Installation Starting...\n\n"

# blackbox pipe a random URL directly to shell
# why? because MSFT
#curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# manual process

# add msft gpg key to apt
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.asc.gpg

# set the right repo name
CLI_REPO=$(lsb_release -cs)

# add the msft repo to apt
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ ${CLI_REPO} main" \
    > /etc/apt/sources.list.d/azure-cli.list

# install the software
apt-get update && apt-get install -y azure-cli

# Repo Azure is not most up to date client, run az upgrade to get latest copy
az upgrade -y

echo -e "\n\nAzure CLI Installation Complete!\n\n"
