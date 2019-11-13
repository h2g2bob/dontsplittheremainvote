#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

cat generated/example_postcodes.csv | while read line; do
  slug=$(echo "$line" | cut -d , -f 1 | tr -d '\r')
  pcode=$(echo "$line" | cut -d , -f 2 | tr -d '\r')
  curl --location "https://tactical-vote.uk/results?postcode=${pcode}" >| "data/peoples_vote/response/${slug}.html"
done
