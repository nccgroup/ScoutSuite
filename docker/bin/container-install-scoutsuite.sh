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
git clone https://github.com/TiiSysDev/ScoutSuite.git
cd ScoutSuite
virtualenv -p python3 scoutsuite
source ${WORKDIR}/scoutsuite/bin/activate
pip install -r requirements.txt
python -m pip install --upgrade awscli
python scout.py --help

# Install from your fork
git clone https://github.com/TiiSysDev/ScoutSuite.git
cd ScoutSuite
pip install -e .


echo -e "\n\nScoutsuite Installation Complete!\n\n"

