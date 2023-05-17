#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package
import itertools
import os
import textwrap
from functools import cache

import yoyo
from tabulate import tabulate
from yoyo.backends import DatabaseBackend
from yoyo.migrations import MigrationList, PostApplyHookMigration, topological_sort, Migration

from jukebox import utils
from jukebox.database.core import db_uri
from jukebox.globals import root

logger = utils.get_logger('migration')
source: str = str(root / 'jukebox/database/revisions')


@cache
def get_backend() -> DatabaseBackend:
    logger.info('Using database: %s', db_uri.obscure_password)
    return yoyo.get_backend(
        uri=str(db_uri),  # Accepts only string value
        migration_table='schema_version'
    )


@cache
def get_migrations() -> MigrationList:
    migrations = yoyo.read_migrations(source)

    if len(migrations) > 0:
        logger.info('Successfully read %d migration script(s) from %s', len(migrations), source)
    else:
        logger.warning('No migration script(s) found in %s', source)

    return migrations


def list_migrations() -> None:
    backend: DatabaseBackend = get_backend()
    migrations: MigrationList = get_migrations()

    headers: list = ["Version", "Description", "Type", "State"]
    table: list = []

    with backend.lock():
        history: list = backend.get_applied_migration_hashes()

        all_migrations = topological_sort(migrations)
        if migrations.post_apply:
            all_migrations = itertools.chain(all_migrations, topological_sort(migrations.post_apply))

        for migration in all_migrations:
            ref_id: str = textwrap.shorten(migration.id, width=50, placeholder='...')
            description: str = textwrap.shorten(
                migration.module.__doc__.splitlines()[0].strip(), width=70, placeholder='...',
            )
            script_type: str = "SQL" if migration.is_raw_sql() else "SCRIPT"
            if isinstance(migration, PostApplyHookMigration):
                status: str = "Post-apply"
            else:
                status: str = "Success" if migration.hash in history else "Pending"
            table.append([ref_id, description, script_type, status])

    grid: str = tabulate(table, headers, tablefmt="simple_outline")
    logger.debug(os.linesep + grid)


def perform_migrations(develop: bool = False) -> None:
    backend: DatabaseBackend = get_backend()
    migrations: MigrationList = get_migrations()

    if not migrations:
        return

    # Log current status
    list_migrations()

    # Perform migrations
    with backend.lock():
        unapplied: MigrationList = backend.to_apply(migrations)

        def apply_migrations(revisions: MigrationList) -> None:
            for revision in revisions:
                logger.debug("Migrating database to version '%s'", revision.id)
                backend.apply_one(revision)

            for revision in revisions.post_apply:
                logger.debug("Running post-apply script '%s'", revision.id)
                backend.apply_one(revision, mark=False)

        def rollback_revisions(revisions: MigrationList) -> None:
            for revision in revisions:
                logger.debug("Rolling back database from version '%s'", revision.id)
                backend.rollback_one(revision)

        if len(unapplied) > 0:
            # Apply any pending migrations
            logger.info("Applying pending migrations to database")
            apply_migrations(unapplied)
            logger.info("Successfully applied %d migrations to database", len(unapplied))

        elif develop:
            # Re-apply last migration
            logger.info("Re-applying last migration to database")
            last_migration = backend.to_rollback(migrations)[:1]
            rollback_revisions(last_migration)
            unapplied: MigrationList = backend.to_apply(migrations)
            apply_migrations(unapplied)
            logger.info("Successfully re-applied last migration to database")

        else:
            # Invalid Operation
            logger.info('Database up-to-date, no migration needed')


if __name__ == '__main__':
    perform_migrations()
