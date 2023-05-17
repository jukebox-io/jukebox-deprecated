#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from functools import cache
from pathlib import Path

import yoyo
from yoyo.backends import DatabaseBackend
from yoyo.migrations import MigrationList

from jukebox.database import DATABASE_URL
from jukebox.globals import ROOT_DIR

MIGRATION_TABLE: str = 'schema_version'
MIGRATION_SOURCE: Path = ROOT_DIR / 'migrations'


@cache
def get_backend() -> DatabaseBackend:
    """
    Returns a database backend connection object for the given database URL.
    """
    return yoyo.get_backend(f'{DATABASE_URL}', MIGRATION_TABLE)


@cache
def read_migrations() -> MigrationList:
    """
    Reads and returns the list of all migrations available at the given migration source directory.
    """
    return yoyo.read_migrations(f'{MIGRATION_SOURCE}')


def get_status() -> str:
    pass
