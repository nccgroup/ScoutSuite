FROM ubuntu:20.04 AS builder

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

COPY ./bin /root/bin

# install the software pre-reqs
RUN ["/bin/bash", "-c","/root/bin/container-install-prereqs.sh"]

# install AWS2
FROM builder AS aws2
RUN ["/bin/bash", "-c", "/root/bin/container-install-aws2.sh"]

# install Azure CLI
FROM aws2 AS azure
RUN ["/bin/bash", "-c", "/root/bin/container-install-azure.sh"]

# install gCloud SDK
FROM azure AS gcloud
RUN ["/bin/bash", "-c", "/root/bin/container-install-gcp.sh"]

# install ScoutsuiteA
FROM gcloud AS scoutsuite
RUN ["/bin/bash", "-c", "/root/bin/container-install-scoutsuite.sh"]

# Add container security checks to make sure we're solid
# This currently fails in the autobuild, so leaving it out for now
# FROM scoutsuite as secscan
# ADD https://get.aquasec.com/microscanner .
# RUN chmod +x microscanner
# RUN ["./microscanner NTM2NTEzM2RkYjU2"]

# set up the venv and leave users with a helpful login message
FROM scoutsuite AS final
RUN ["/bin/bash", "-c", "/root/bin/container-set-motd.sh"]

# entrypoint
CMD ["/bin/bash"]
