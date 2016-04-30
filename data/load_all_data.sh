#!/usr/bin/env bash
# start shell script

# source environment

source ../env/bin/activate
./manage.py loaddata data/full.json
