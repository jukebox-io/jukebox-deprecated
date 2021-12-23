import uvicorn

from common import ServerConfig


def start_non_unix_server() -> None:
    """Start Uvicorn server Implementation for Non-Unix based OS"""
    config = ServerConfig()
    uvicorn.run(app=config.router,
                host=config.host,
                port=config.port,
                workers=config.worker_count,
                )
