#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

function download() {
  grep="$1"
  cat generated/example_postcodes.csv | grep -E "${grep}" | while read line; do
    slug=$(echo "$line" | cut -d , -f 1 | tr -d '\r')
    pcode=$(echo "$line" | cut -d , -f 2 | tr -d '\r')
    echo "$slug"
    curl 'https://www.remainunited.org/' \
      --data "form_type=postcode-search&hid_form=Postcode+Search+Form&action=search&f_search_text_postcode=${pcode}&submit=submit" \
      --silent \
      --retry 10 --retry-delay 30 \
      >| "data/remainunited/response/${slug}.html"
  done
}

# remain united is super slow, so
# * re-use a connection instead of making a new ssl connection each time
# * do lots in paralell
download '^[ab]'  &
download '^[cd]'  &
download '^[e]'  &
download '^[fghijklm]'  &
download '^[n]'  &
download '^[opqr]'  &
download '^[s]'  &
download '^[tuvwxyz]'  &
download '^[w]'  &
jobs
wait $(jobs -p)
