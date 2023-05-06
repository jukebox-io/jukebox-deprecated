#!/bin/sh

#
# Copyright 2023 by JukeBox Developers. All rights reserved.
#
# This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package.
#

set -e

# activate our virtual environment here
. "$SETUP_HOME/.venv/bin/activate"

# You can put other setup logic here

# Evaluating passed command:
exec "$@"