#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import shlex
import subprocess

from jukebox import utils
from jukebox.globals import root

DEFAULT_OPTS = ["--no-config-file", "--batch"]

logger = utils.get_logger('migration')
source: str = str(root / 'jukebox/database/revisions')


def make_migration(title: str = None, scriptable: bool = False) -> None:
    options: list[str] = DEFAULT_OPTS

    if title:  # if title is provided
        options += ["--message", title]

    if not scriptable:  # if not scriptable
        options += ["--sql"]

    cmd: str = shlex.join(["yoyo-migrate", "new", *options, source])
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    # Prompt for input
    title_input: str = input("Enter a suitable title for your migration: ")

    # Create a new migration script
    make_migration(title_input)
