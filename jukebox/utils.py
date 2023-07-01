#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from urllib.parse import quote

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
