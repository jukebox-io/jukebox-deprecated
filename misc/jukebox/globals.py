#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from pathlib import Path

import psutil

from jukebox import utils

logger = utils.getLogger('jukebox.main')

ID_VERSION: str = '0.2.1'

ROOT_DIR: Path = Path(__file__).parents[1]
NUM_CORES: int = psutil.cpu_count(logical=False) or 1
