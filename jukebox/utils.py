#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import logging
import logging.config
from urllib.parse import quote

import yaml
from fastapi import FastAPI, Request, Response
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


class AccessLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.logger = get_logger('access')

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        await self.log_access(request, response)
        return response

    async def log_access(self, request: Request, response: Response) -> None:
        self.logger.info(
            '%s - "%s %s HTTP/%s" %d',
            self.get_client_addr(request.scope) or 'unknown',
            request.method,
            self.get_path_with_query_string(request.scope),
            request.get('http_version'),
            response.status_code
        )

    @classmethod
    def get_client_addr(cls, scope: Scope) -> str:
        client = scope.get("client")
        if not client:
            return ""
        return "%s:%d" % client

    @classmethod
    def get_path_with_query_string(cls, scope: Scope) -> str:
        path_with_query_string = quote(scope["path"])
        if scope["query_string"]:
            path_with_query_string = "{}?{}".format(
                path_with_query_string, scope["query_string"].decode("ascii")
            )
        return path_with_query_string
