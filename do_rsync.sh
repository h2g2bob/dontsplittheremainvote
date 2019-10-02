#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

source config.sh

cd generated/
rsync -rvv --chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r . "${RSYNC_LOCATION}"
