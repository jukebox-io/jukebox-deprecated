from jukebox.database import database


async def startup_hook() -> None:
    # Establish new connection pool
    await database.connect()


async def shutdown_hook() -> None:
    # Close current connection pool
    await database.disconnect()
