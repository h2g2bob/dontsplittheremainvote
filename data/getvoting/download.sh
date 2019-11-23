#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

cat data/getvoting/constituency-names.csv | while read line; do
  ourslug="$(echo "$line" | cut -d , -f 1)";
  theirslug="$(echo "$line" | cut -d , -f 2)";
  curl --location "https://tacticalvote.getvoting.org/${theirslug}/" >| "data/getvoting/response/${ourslug}.html";
done
