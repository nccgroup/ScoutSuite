#!/bin/bash
source .env
#echo ${VERSION}
docker tag nccgroup/scoutsuite-aws:${VERSION} rossja/scoutsuite-aws:${VERSION}
docker tag nccgroup/scoutsuite-azure:${VERSION} rossja/scoutsuite-azure:${VERSION}
docker tag nccgroup/scoutsuite-gcp:${VERSION} rossja/scoutsuite-gcp:${VERSION}
docker tag nccgroup/scoutsuite-base:${VERSION} rossja/scoutsuite-base:${VERSION}

docker tag rossja/scoutsuite-aws:${VERSION} rossja/scoutsuite-aws:latest
docker tag rossja/scoutsuite-azure:${VERSION} rossja/scoutsuite-azure:latest
docker tag rossja/scoutsuite-gcp:${VERSION} rossja/scoutsuite-gcp:latest
docker tag rossja/scoutsuite-base:${VERSION} rossja/scoutsuite-base:latest

docker push rossja/scoutsuite-aws:${VERSION}
docker push rossja/scoutsuite-azure:${VERSION}
docker push rossja/scoutsuite-gcp:${VERSION}
docker push rossja/scoutsuite-base:${VERSION}

docker push rossja/scoutsuite-aws:latest
docker push rossja/scoutsuite-azure:latest
docker push rossja/scoutsuite-gcp:latest
docker push rossja/scoutsuite-base:latest
