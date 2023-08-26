#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import logging
import logging.config

import yaml
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from jukebox.globals import project_root
from jukebox.utils import extract_client_address, extract_path_with_query_string

with open(project_root / 'jukebox/config/logging.yaml') as file:
    # Configure logging

    default_log_config: dict = yaml.safe_load(file)
    logging.config.dictConfig(default_log_config)  # load default


def get_logger(scope: str = 'default') -> logging.Logger:
    """
    Get a logger for the given scope.

    Args:
        scope (str) : scope of the logger (default: 'default')

    Returns:
        An instance of logger with the given scope.
    """

    return logging.getLogger(f'jukebox.{scope}')


# ----------------------------------------------------------------
# ACCESS LOGGER CLASS
# ----------------------------------------------------------------

class AccessLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware that handles access log messages from the application.
    """

    logger: logging.Logger = get_logger('access')
    log_fmt: str = '[ %(state)5s ] %(address)s - "%(method)s %(path)s HTTP/%(version)s" %(status_code)s'

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        details: dict = {
            'address': extract_client_address(request.scope) or 'anonymous',
            'method': request.method,
            'path': extract_path_with_query_string(scope=request.scope),
            'version': request.get('http_version') or 'nil',
        }

        try:
            # log request
            self.logger.info(self.log_fmt, {**details, 'state': 'BEGIN', 'status_code': ''})

            # perform request
            response: Response = await call_next(request)

            # log response
            self.logger.info(self.log_fmt, {**details, 'state': 'END', 'status_code': response.status_code})

        except BaseException as ex:
            # log exception
            status_code: int = getattr(ex, 'status_code', 500)
            self.logger.info(self.log_fmt, {**details, 'state': 'END', 'status_code': status_code}, exc_info=ex)
            raise ex

        return response
