#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from databases import Database, DatabaseURL

from jukebox.globals import NUM_CORES
from jukebox.settings import settings

DATABASE_URL: DatabaseURL = settings.get('DATABASE_URL', cast=DatabaseURL)

max_pool_size: int = settings.get(
    'DB_CONCURRENCY', cast=int, default=2 * NUM_CORES + 1
)
if max_pool_size > 99:
    # limit to a maximum of 99 connections
    max_pool_size = 99

# Database connection object
database = Database(
    url=DATABASE_URL,
    min_size=0,  # initialize with zero connections
    max_size=max_pool_size,
    ssl="prefer",
)
