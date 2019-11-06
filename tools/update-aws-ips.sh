#!/bin/sh

DIR="$( dirname "$_" )"
curl https://ip-ranges.amazonaws.com/ip-ranges.json > "$DIR/../ScoutSuite/data/aws/ip-ranges/aws.json"
