#!/usr/bin/env bash

source environ.sh

if [[ $1 == '-d' ]]
then
	nohup python3 field_gateway/__main__.py </dev/null >/dev/null 2>&1 &
else
	python3 field_gateway/__main__.py 
fi
