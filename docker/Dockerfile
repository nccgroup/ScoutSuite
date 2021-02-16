FROM python:3.8

LABEL maintainer="Jason Ross <jason.ross@nccgroup.com>"

ARG BUILD_DATE
ARG NAME
ARG DESCRIPTION
ARG VCS_REF
ARG VCS_URL
ARG VENDOR
ARG VERSION
ARG IMAGE_NAME

ENV DEBIAN_FRONTEND=${DEBIAN_FRONTEND}
ENV TERM=${TERM}
ENV IBMCLOUD_COLOR=${IBMCLOUD_COLOR}

# Build-time metadata as defined at http://label-schema.org
LABEL \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date="${BUILD_DATE}" \
    org.label-schema.name="${NAME}" \
    org.label-schema.description="${DESCRIPTION}" \
    org.label-schema.vcs-ref="${VCS_REF}" \
    org.label-schema.vcs-url="${VCS_URL}" \
    org.label-schema.vendor="${VENDOR}" \
    org.label-schema.version="${VERSION}" \
    org.label.image-name="${IMAGE_NAME}"

# Copy helper scripts to container
ADD bin /root/bin

# Install required software
RUN ["/bin/bash", "-c", "/root/bin/container-install-prereqs.sh"]

# Install AWS CLI
RUN ["/bin/bash", "-c", "/root/bin/container-install-aws2.sh"]

# Install Azure CLI
RUN ["/bin/bash", "-c", "/root/bin/container-install-azure.sh"]

# Install gCloud SDK
RUN ["/bin/bash", "-c", "/root/bin/container-install-gcp.sh"]

# Install ScoutSuite
RUN ["/bin/bash", "-c", "/root/bin/container-install-scoutsuite.sh"]

# Set a nice message
RUN ["/bin/bash", "-c", "/root/bin/container-set-init.sh"]

# Remove scripts
RUN ["rm", "-rf", "/root/bin"]

# Command
CMD ["/bin/bash"]
