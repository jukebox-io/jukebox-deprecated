#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

from jukebox.globals import global_settings

db_uri: str = global_settings.get('DATABASE_URL')

database: Database = AsyncIOMotorClient(db_uri).get_default_database()


async def init_db_conn() -> None:
    """Initialize the database connection"""
    await init_beanie(database=database)


async def close_db_conn() -> None:
    """Close the database connection"""
    database.client.close()
