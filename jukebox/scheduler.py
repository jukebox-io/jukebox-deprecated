#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import os

import psutil
from rocketry import Rocketry

from jukebox.logger import get_logger

logger = get_logger('scheduler')

scheduler = Rocketry()


@scheduler.task('every 30 seconds')
async def example_task():
    if psutil.virtual_memory().percent > 90:
        logger.warning("Low memory alert !!!")


def run_scheduler() -> None:
    """
    Runs the job scheduler in the current thread.
    """
    logger.debug("Booting scheduler with pid: %d", os.getpid())
    try:
        scheduler.run()
    except KeyboardInterrupt:
        # Don't raise the keyboard interrupt, and exit gracefully
        pass
    logger.debug("Stopping scheduler with pid: %d", os.getpid())


if __name__ == '__main__':
    run_scheduler()
