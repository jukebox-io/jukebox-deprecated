#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from databases import Database, DatabaseURL

from jukebox.globals import settings

db_uri: DatabaseURL = settings.get('DATABASE_URL', cast=DatabaseURL)

database = Database(db_uri)


async def init_db() -> None:
    await database.connect()


async def close_db() -> None:
    await database.disconnect()
