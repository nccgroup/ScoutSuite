#!/bin/bash
cat <<'EOF' >> /root/.bashrc
cd ${HOME}
source ${HOME}/scoutsuite/bin/activate
echo -e "Welcome to ScoutSuite!\nTo run ScoutSuite, just type \`scout -h\` to see the help documentation.\nHave fun!\n\n"
EOF