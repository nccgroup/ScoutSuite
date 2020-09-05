#!/bin/bash
cat <<'EOF' >> /root/.bashrc
cd ${HOME}
echo -e "Welcome to ScoutSuite!\nTo run ScoutSuite, just type \`scout -h\` to see the help documentation.\nHave fun!\n\n"
EOF