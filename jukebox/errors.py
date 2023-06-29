#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from fastapi.exceptions import HTTPException
from starlette import status


class ServiceError(HTTPException):
    def __init__(self, msg: str, *, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, **kwargs):
        super().__init__(status_code, msg, **kwargs)


class NoSuchItemFoundError(ServiceError):
    def __init__(self, msg: str, **kwargs):
        super().__init__(msg, status_code=status.HTTP_404_NOT_FOUND, **kwargs)
