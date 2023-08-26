#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from jukebox.utils.logger import getLogger

logger = getLogger()


def test(a):
    try:
        b = 5 / a
        logger.info("Result = {}", b)
    except:
        logger.exception("Exception in test")


if __name__ == '__main__':
    for i in [1, 2, 3, None, 4, 5, 6, 'Text']:
        test(i)
