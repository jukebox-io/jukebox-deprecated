#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from starlette.authentication import AuthenticationBackend, AuthCredentials, BaseUser
from starlette.requests import HTTPConnection


class JWTAuthBackend(AuthenticationBackend):
    """
    Implementation that provides authentication through JWT based authentication.

    Raises:
        Error if authentication fails.
    """

    async def authenticate(self, conn: HTTPConnection) -> None | tuple[AuthCredentials, BaseUser]:
        pass
