#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

cat generated/example_postcodes.csv | while read line; do
  slug=$(echo "$line" | cut -d , -f 1 | tr -d '\r')
  pcode=$(echo "$line" | cut -d , -f 2 | tr -d '\r')
  out="data/peoples_vote/response/${slug}.html"
  if ! ( ! [ -z $( find "$out" -cmin -60 ) ] > /dev/null && grep -F '</html>' "$out" > /dev/null ); then
    curl --location "https://tactical-vote.uk/results?postcode=${pcode}" >| "${out}"
  fi
done
