from databases import Database

from jukebox.settings import DATABASE_URL, MIN_POOL_SIZE, MAX_POOL_SIZE, SSL_MODE

database = Database(DATABASE_URL, min_size=MIN_POOL_SIZE, max_size=MAX_POOL_SIZE, ssl=SSL_MODE)
