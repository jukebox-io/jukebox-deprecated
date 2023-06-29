#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import logging
import logging.config
from urllib.parse import quote

import yaml
from fastapi import FastAPI, Request, Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import Scope

from jukebox.globals import root

# ------------------------------------------------------------------------------------
# Logging Utilities
# ------------------------------------------------------------------------------------

# Configure logging
with open(root / 'jukebox/config/logging.yaml') as file:
    logging_config: dict = yaml.safe_load(file)
    logging.config.dictConfig(logging_config)


def get_logger(scope: str = 'default'):
    """
    Get a logger for the given scope.
    """
    return logging.getLogger(f'jukebox.{scope}')


def get_client_addr(scope: Scope) -> str:
    client = scope.get("client")
    if not client:
        return ""
    return "%s:%d" % client


def get_path_with_query_string(scope: Scope) -> str:
    path_with_query_string = quote(scope["path"])
    if scope["query_string"]:
        path_with_query_string = "{}?{}".format(
            path_with_query_string, scope["query_string"].decode("ascii")
        )
    return path_with_query_string


class AccessLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.logger = get_logger('access')

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        msg: str = '[ %(state)5s ] %(address)s - "%(method)s %(path)s HTTP/%(version)s" %(status_code)s'
        details: dict = {
            'address': get_client_addr(request.scope) or 'anonymous',
            'method': request.method,
            'path': get_path_with_query_string(scope=request.scope),
            'version': request.get('http_version') or 'nil',
        }

        # log the request
        self.logger.info(msg, {**details, 'state': 'BEGIN', 'status_code': ''})

        # perform the operation and log the response
        try:
            response: Response = await call_next(request)

            self.logger.info(msg, {**details, 'state': 'END', 'status_code': response.status_code})
            return response

        except BaseException as exc_info:
            # log the exception
            status_code: int = 500
            if isinstance(exc_info, StarletteHTTPException):
                status_code = exc_info.status_code

            self.logger.error(msg, {**details, 'state': 'END', 'status_code': status_code}, exc_info=exc_info)
            raise exc_info      # re-raise exception
