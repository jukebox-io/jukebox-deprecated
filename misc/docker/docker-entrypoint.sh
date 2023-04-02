#!/bin/sh

set -e

# activate our virtual environment here
. "$SETUP_HOME/.venv/bin/activate"

# You can put other setup logic here

# Evaluating passed command:
exec "$@"