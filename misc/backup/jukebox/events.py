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

from jukebox.database import database


async def startup_hook() -> None:
    # Establish new connection pool
    await database.connect()


async def shutdown_hook() -> None:
    # Close current connection pool
    await database.disconnect()
