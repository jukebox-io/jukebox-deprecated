#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import random
import string
from urllib.parse import quote, urlparse

from starlette.types import Scope


def extract_client_address(scope: Scope) -> str:
    """
    Extracts the client address from the request scope.

    Args:
        scope (Scope): The request scope to extract the client address from.

    Returns:
        str: The client address as a string.
    """
    client = scope.get("client")
    if not client:
        return ""
    return "%s:%d" % client


def extract_path_with_query_string(scope: Scope) -> str:
    """
    Extracts the path along with the query parameters from the given request scope.

    For Example, if the request url is "http://example.com/query?foo=bar" then this function will return
    "/query?foo=bar" as output.

    Args:
        scope (Scope): The request scope to extract the path from.

    Returns:
        str: The path along with the query parameters as a string.
    """
    path_with_query_string = quote(scope["path"])
    if scope["query_string"]:
        path_with_query_string = "{}?{}".format(
            path_with_query_string, scope["query_string"].decode("ascii")
        )
    return path_with_query_string


def obscure_password(url: str) -> str:
    """
    Replace the password in a given url with ****.

    Args:
        url (str): The given url to replace the password.

    Returns:
        str: The url after the password was replaced.
    """
    url_parts = urlparse(url)
    netloc = url_parts.netloc

    if '@' in netloc:
        auth, host = netloc.rsplit('@', 1)
        if ':' in auth:
            user, _ = auth.split(':', 1)
            auth = "{user}:{password}".format(user=user, password='*****')
        netloc = f"{auth}@{host}".format(auth=auth, host=host)

    return url_parts._replace(netloc=netloc).geturl()


def get_random_string(length: int = 10, population: str = None):
    """
    Return a random string of ``length`` characters
    """
    if not population:
        population = string.ascii_letters + string.digits  # use alphanumeric by default

    return "".join(random.choices(population=population, k=length))
