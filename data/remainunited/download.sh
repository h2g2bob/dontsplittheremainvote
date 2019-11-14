#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

cat generated/example_postcodes.csv | while read line; do
  slug=$(echo "$line" | cut -d , -f 1 | tr -d '\r')
  pcode=$(echo "$line" | cut -d , -f 2 | tr -d '\r')
  while ! curl 'https://www.remainunited.org/' --data "form_type=postcode-search&hid_form=Postcode+Search+Form&action=search&f_search_text_postcode=${pcode}&submit=submit" >| "data/remainunited/response/${slug}.html" ; do
    sleep 120;
  done

# -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-GB,en;q=0.5' --compressed -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://www.remainunited.org' -H 'Connection: keep-alive' -H 'Referer: https://www.remainunited.org/' -H 'Cookie: PHPSESSID=1jjurneq387ktevu7mm4qtm0u6; _fbp=fb.1.1573391464135.20395060' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'TE: Trailers' 
done
