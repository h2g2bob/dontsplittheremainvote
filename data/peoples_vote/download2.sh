#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

( grep -l -F "Please check you've entered your postcode correctly" response/*.html || true ; grep -L -F 'on behalf of the People' response/*.html || true ) | while read filename; do
  echo $filename
  slug=`echo $filename | sed -nre 's/^.*response\/(.*)\.html$/\1/p'`
  pcode=`echo -e ".mode csv\nselect postcode from postcodes where slug = '$slug' order by random() limit 1;" | sqlite3 ../../generated/postcodes.sqlite3 | tr -d -c '[0-9A-Z]'`
  echo -e "${slug},${pcode}\r" >> ../../generated/example_postcodes.csv
  curl --location "https://tactical-vote.uk/results?postcode=${pcode}" >| "response/${slug}.html"
done
