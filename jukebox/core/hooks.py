#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from typing import Callable, TypeVar, Any

# ------------------------------------------
# Registry
# ------------------------------------------

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
event_registry: dict[str, list[DecoratedCallable]] = {}


def startup(func: DecoratedCallable) -> DecoratedCallable:
    add_event_handler("startup", func)
    return func


def shutdown(func: DecoratedCallable) -> DecoratedCallable:
    add_event_handler("shutdown", func)
    return func


def add_event_handler(event_type: str, func: Callable) -> None:
    if event_type in event_registry:
        event_registry[event_type].append(func)
    else:
        event_registry[event_type] = [func]


# ------------------------------------------
# Events
# ------------------------------------------

@startup
async def intro() -> None:
    print("Starting Application")
