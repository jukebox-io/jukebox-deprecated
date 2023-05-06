#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from rocketry import Rocketry

from jukebox import utils

logger = utils.build_logger('jukebox.service')

rocketry = Rocketry()


@rocketry.task('every 1 seconds')
def do_ping():
    logger.info('Ping')


if __name__ == '__main__':
    logger.info('Starting scheduler service')
    rocketry.run()
