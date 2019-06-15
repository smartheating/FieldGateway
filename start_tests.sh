#!/usr/bin/env bash

export PYTHONPATH=$(pwd)/field_gateway:$(pwd)/tests:$PYTHONPATH
py.test-3 --capture=no tests
