#!/bin/sh

#
# Copyright (c) 2023 JukeBox Developers - All Rights Reserved
# This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
# Please see the LICENSE file that should have been included as part of this package
#

set -e

# activate our virtual environment here
. /pyenv/bin/activate

# You can put other setup logic here

# Evaluating passed command:
exec "$@"
