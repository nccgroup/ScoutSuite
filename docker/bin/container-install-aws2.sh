#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# =====================================
# install the AWS CLI Tools
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
unzip awscliv2.zip
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
EOF

# create the credentials template
cat <<'EOF' >${AWSDIR}/credentials
[default]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret key>
EOF

fi


echo -e "\n\nAWS2 CLI Installation Complete!\n\n"
