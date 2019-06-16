#!/usr/bin/env bash

source environ.sh

nohup python3 field_gateway/__main__.py </dev/null >/dev/null 2>&1 &
