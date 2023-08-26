#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from pathlib import Path


def resolve_path(path: str | Path) -> Path:
    return Path(__file__).parents[2] / path
