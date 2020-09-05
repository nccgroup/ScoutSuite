#!/bin/bash

# =====================================
# install ScoutSuite into a virtual env
# =====================================
# AUTHOR: jason.ross@nccgroup.com
# VERSION: 0.1.0
# =====================================
export DEBIAN_FRONTEND=noninteractive

WORKDIR=/root
TMPDIR=/tmp

# =====================================
# install ScoutSuite
# =====================================
cd ${WORKDIR}
pip install scoutsuite

echo -e "\n"
scout --version

echo -e "Scoutsuite Installation Complete!\n\n"
