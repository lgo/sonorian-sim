#!/bin/bash

# Python scripts cannot be executed directly in a Makefile and have the
# venv be set within the Makefile.

python src/main.py $@
