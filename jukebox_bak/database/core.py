#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from databases import Database, DatabaseURL

from jukebox.globals import global_settings

db_uri: DatabaseURL = global_settings.get('DATABASE_URL', cast=DatabaseURL)

database = Database(db_uri)


async def init_db_conn() -> None:
    """Initialize the database connection"""
    await database.connect()


async def close_db_conn() -> None:
    """Close the database connection"""
    await database.disconnect()
