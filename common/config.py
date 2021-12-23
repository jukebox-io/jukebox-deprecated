import configparser
from typing import final

from .utils import SingleInstanceMetaClass

_config = configparser.ConfigParser(
    interpolation=configparser.ExtendedInterpolation()
)
_config.read(r'..\config.ini')


class Config(object, metaclass=SingleInstanceMetaClass):
    def __init__(self, group_name: str):
        self._group_name = group_name

    @final
    def get_property_as_str(self, property_name: str, fallback: str = None) -> str:
        return _config.get(self._group_name, property_name, fallback=str(fallback))

    @final
    def get_property_as_int(self, property_name: str, fallback: int = None) -> int:
        return _config.getint(self._group_name, property_name, fallback=int(fallback))

    @final
    def get_property_as_float(self, property_name: str, fallback: float = None) -> float:
        return _config.getfloat(self._group_name, property_name, fallback=float(fallback))

    @final
    def get_property_as_bool(self, property_name: str, fallback: bool = None) -> bool:
        return _config.getboolean(self._group_name, property_name, fallback=bool(fallback))


@final
class AppConfig(Config):
    def __init__(self):
        super().__init__('APP')

    @property
    def environment(self) -> str:
        return self.get_property_as_str('ENVIRONMENT', 'dev')

    @property
    def debug(self) -> bool:
        return self.get_property_as_bool('DEBUG', False)

    @property
    def log_level(self) -> str:
        return self.get_property_as_str('LOG_LEVEL', 'warning')


@final
class ServerConfig(Config):
    def __init__(self):
        super().__init__('SERVER')

    @property
    def host(self) -> str:
        return self.get_property_as_str('HOST', '0.0.0.0')

    @property
    def port(self) -> int:
        return self.get_property_as_int('PORT', 8080)

    @property
    def router(self) -> str:
        return self.get_property_as_str('ROUTER', 'core:router')

    @property
    def worker_class(self) -> str:
        return self.get_property_as_str('WORKER_CLASS', 'uvicorn.workers.UvicornWorker')

    @property
    def worker_count(self) -> int:
        count = self.get_property_as_int('WORKER_COUNT', -1)

        # Start auto detection
        if count <= 0:
            from server.base import auto_detect_worker_count  # to avoid circular dependency
            count = auto_detect_worker_count()

        return count


@final
class DbConfig(Config):
    def __init__(self):
        super().__init__('DATABASE')
