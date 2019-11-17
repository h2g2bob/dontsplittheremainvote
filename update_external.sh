#!/bin/bash
set -o errexit
set -o noclobber
set -o pipefail
set -o nounset

if [ -z "$( find data/tacticalvote/ -name recommendations.json -cmin -120 )" ]; then
    wget https://tacticalvote.co.uk/data/recommendations.json -O data/tacticalvote/recommendations.json ;
fi

if [ -z "$( find data/tactical_dot_vote/ -name all.html -cmin -120 )" ]; then
    wget 'https://tactical.vote/all' -O data/tactical_dot_vote/all.html ;
fi

if [ -z "$( find data/getvoting/ -name NewData.json -cmin -120 )" ]; then
    wget 'https://getvoting.org/NewData.json' -O data/getvoting/NewData.json ;
fi

if [ -z "$( find data/democlub-candidates/ -name candidates-parl.2019-12-12.csv -cmin -3000 )" ]; then
    wget 'https://candidates.democracyclub.org.uk/media/candidates-parl.2019-12-12.csv' -O data/democlub-candidates/candidates-parl.2019-12-12.csv ;
fi
