#!/bin/bash
# set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

function save() {
  catname="$1"
  leaf="$2"
  filename="data/jonworth/response/$leaf.1.html"
  wget --quiet "https://tacticalvoting.jonworth.eu/category/$catname/" -O "$filename"
  cat "$filename" | grep -E -o '/page/[0-9]+' | grep -E -o '[0-9]+' | sort | uniq | while read pageno; do
    filename="data/jonworth/response/$leaf.$pageno.html"
    wget --quiet "https://tacticalvoting.jonworth.eu/category/$catname/page/$pageno/" -O "$filename"
  done
}

save tactically-vote-labour-to-un-seat-a-conservative lab-unseat
save tactically-vote-labour-to-make-sure-labour-still-wins-the-seat lab-keep
save tactically-vote-lib-dem-to-un-seat-a-conservative ld-unseat
save tactically-vote-lib-dem-to-make-sure-lib-dems-still-win-the-seat ld-keep
save tactically-vote-snp-to-un-seat-a-conservative snp-unseat
save tactically-vote-snp-to-make-sure-snp-still-wins-the-seat snp-keep
save tactically-vote-lib-dem-to-not-split-the-remain-vote ld-nosplit
save unique-constituency unique
echo "done"
