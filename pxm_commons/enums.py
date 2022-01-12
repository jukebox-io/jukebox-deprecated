import enum


class ApiVersionEnum(str, enum.Enum):
    """Enum representing API versions."""
    V1 = "v1"


class Config:
    """PXM Configurations"""

    class APP(str, enum.Enum):
        """General Application Configuration"""
        HOME = 'pxm.home'
        VERSION = 'pxm.version'
        DEBUG = 'pxm.debug'
        LOG_LEVEL = 'pxm.log_level'

    class DATABASE(str, enum.Enum):
        """Configuration for the Database"""
        URL = 'database.url'

    class SERVER(str, enum.Enum):
        """Configuration for the server environment"""
        HOST = 'server.host'
        PORT = 'server.port'
        ROUTER = 'server.router'
        WORKER_COUNT = 'server.worker.count'
        WORKER_CLASS = 'server.worker.class'
