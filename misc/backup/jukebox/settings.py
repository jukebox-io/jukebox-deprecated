#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.

from starlette.config import Config

# The configuration will be read from different sources in the following order:
#   1. Environment Variables (mostly used during production)
#   2. development.conf (if available, sets development defaults for required configurations)
#   3. Default value (some of the configuration is optional and will be assigned default value automatically)

# read development config if present
settings = Config(env_file="misc/development.conf")
