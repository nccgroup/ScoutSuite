#!/bin/bash

# =====================================
# container-scoutsuite-install.sh
# =====================================
# AUTHOR: jason.ross@nccgroup.com
# VERSION: 0.1.0
# =====================================
WORKDIR=/root
TMPDIR=/tmp
AWSDIR=/root/.aws

echo -e "\n\nAWS2 CLI Installation Starting...\n\n"

# =====================================
# install AWS CLI v2
# =====================================
cd ${TMPDIR}
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
./aws/install --update

# =====================================
# clean up install artifacts
# =====================================
rm ${TMPDIR}/awscliv2.zip
rm -rf ${TMPDIR}/aws

# =====================================
# Setup AWS configuration templates
# =====================================

# if the aws config directory already exists
# then we do nothing and leave it alone
if [ ! -d ${AWSDIR} ]; then
    mkdir ${AWSDIR}

    # create the config template
    cat <<'EOF' >${AWSDIR}/config
    [default]
    region = us-east-1
    output = json
    aws_access_key_id = <access-key>
    aws_secret_access_key = <secret key>
EOF
fi

# check that aws was installed successfully
echo -e "\n"
aws --version

echo -e "AWS2 CLI Installation Complete!\n\n"
