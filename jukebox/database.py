from databases import Database, DatabaseURL

from jukebox.settings import settings
from jukebox.utils import NUM_CORES

DATABASE_URL: DatabaseURL = settings.get('DATABASE_URL', cast=DatabaseURL)

# the maximum number of connections the database can accept
max_pool_size: int = 2 * NUM_CORES + 1
if max_pool_size > 99:
    # limit to a maximum of 99 connections (just in case)
    max_pool_size = 99

# Configure database connection
database = Database(
    url=DATABASE_URL,
    min_size=0,  # initialize with zero connections
    max_size=max_pool_size,
    ssl="prefer",
)
