#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

source config.sh

cd generated/
for RSYNC_LOCATION in "${RSYNC_LOCATIONS[@]}"; do
	rsync -rv --chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r . "${RSYNC_LOCATION}"
done
