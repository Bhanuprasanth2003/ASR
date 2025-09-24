#!/usr/bin/env bash
# wrapper to ensure the proper python interpreter / venv is used
# edit PYTHON to the python you want to use (system or virtualenv)
PYTHON="/usr/bin/python3"
exec "$PYTHON" "/home/bhanu2003/projects/ASR1/main.py" "$@"

