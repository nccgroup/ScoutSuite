FROM python:3.8

LABEL maintainer="Jason Ross <jason.ross@nccgroup.com>"

ARG VCS_REF
ARG VCS_URL
ARG VERSION
ARG BUILD_DATE
ARG VENDOR
ARG NAME
ARG DESCRIPTION

# Build-time metadata as defined at http://label-schema.org
LABEL \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name=$NAME \
    org.label-schema.description=$DESCRIPTION \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url=$VCS_URL \
    org.label-schema.vendor=$VENDOR \
    org.label-schema.version=$VERSION

# Copy helper scripts to container
COPY bin /root/bin

# Install any additional software
RUN ["/bin/bash", "-c", "/root/bin/container-install-additional.sh"]

# Set a nice message
RUN ["/bin/bash", "-c", "/root/bin/container-set-motd.sh"]

# Install AWS CLI
RUN ["/bin/bash", "-c", "/root/bin/container-install-aws2.sh"]

# Install Azure CLI
RUN ["/bin/bash", "-c", "/root/bin/container-install-azure.sh"]

# Install gCloud SDK
RUN ["/bin/bash", "-c", "/root/bin/container-install-gcp.sh"]

# Install ScoutSuite
RUN ["/bin/bash", "-c", "/root/bin/container-install-scoutsuite.sh"]

# Remove scripts
RUN ["rm", "-rf", "/root/bin"]

# Command
CMD ["/bin/bash"]