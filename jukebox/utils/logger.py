#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import sys
from typing import Any

from loguru import logger as root_logger

from jukebox.core.constants import LOG_LEVEL, LOG_FORMAT

root_logger.configure(handlers=[
    {
        'sink': sys.stdout,
        'level': LOG_LEVEL,
        'format': LOG_FORMAT,
        'enqueue': True,
        'diagnose': True,
    },
])


def getLogger(scope: str = 'default') -> Any:
    return root_logger.bind(scope=scope)
