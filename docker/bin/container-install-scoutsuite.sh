#!/bin/bash

# =====================================
# install ScoutSuite into a virtual env
# =====================================

WORKDIR=/root
TMPDIR=/tmp

# =====================================
# install ScoutSuite
# =====================================
cd ${WORKDIR}
virtualenv -p python3 scoutsuite
source ${WORKDIR}/scoutsuite/bin/activate

# Install from your fork
git clone https://github.com/TiiSysDev/ScoutSuite.git
cd ScoutSuite
pip install -e .


echo -e "\n\nScoutsuite Installation Complete!\n\n"
