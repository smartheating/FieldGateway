#!/usr/bin/env bash

export PYTHONPATH=$(pwd)/field_gateway:$(pwd)/tests:$PYTHONPATH
export CONFIG=$(pwd)/config.yaml

python3 field_gateway/__main__.py