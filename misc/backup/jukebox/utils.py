#  Copyright 2023 by JukeBox Developers. All rights reserved.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.

import pathlib
import subprocess

import psutil

# Project Directories
PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).parents[1]

# The number of physical CPU cores present in the host system. It is expected to have at least 1 core
NUM_CORES: int = psutil.cpu_count(logical=False) or 1


def run_shell_command(command: str, *, working_dir=PROJECT_ROOT):
    """Execute a shell command and wait for it to complete.

    Args:
        command (str): The command to execute.
        working_dir (path): The directory in which to run the command. Defaults to the project root directory.

    Raises:
        CalledProcessError: If the command returns a non-zero exit code.
    """

    subprocess.run(command, shell=True, check=True, cwd=working_dir)
