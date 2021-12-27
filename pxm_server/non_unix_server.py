import uvicorn

from pxm_server.server import (SERVER_ROUTER, SERVER_HOST, SERVER_PORT, SERVER_WORKER_COUNT)


def start_non_unix_server() -> None:
    """Start Uvicorn server Implementation for Non-Unix based OS"""
    uvicorn.run(app=SERVER_ROUTER,
                host=SERVER_HOST,
                port=int(SERVER_PORT),  # Expects integer value
                workers=SERVER_WORKER_COUNT,
                )
