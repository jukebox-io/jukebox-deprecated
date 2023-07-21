#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package
import glob
import itertools
import os
import textwrap
from datetime import date
from functools import cache

import yoyo
from slugify import slugify
from tabulate import tabulate
from yoyo.backends import DatabaseBackend
from yoyo.migrations import MigrationList, PostApplyHookMigration, topological_sort

from jukebox.database.core import db_uri
from jukebox.globals import project_root
from jukebox.logger import get_logger
from jukebox.utils import obscure_password, get_random_string

logger = get_logger('migration')
source: str = str(project_root / 'jukebox/database/revisions')

MIGRATION_TEMPLATE: str = textwrap.dedent(
    '''\
    """
    {description}
    """
    
    
    class Forward:
        ...
    
    
    class Backward:
        ...
    '''
)


@cache
def create_db_manager() -> DatabaseBackend:
    """
    Create a new database manager and caches it.
    """
    logger.info('Using database: %s', obscure_password(db_uri))
    return yoyo.get_backend(
        uri=db_uri,
        migration_table='schema_version'
    )


@cache
def read_migrations() -> MigrationList:
    """
    Reads all migration scripts and returns the list of migrations.
    """
    migrations = yoyo.read_migrations(source)

    if len(migrations) > 0:
        logger.info('Successfully read %d migration script(s) from %s', len(migrations), source)
    else:
        logger.warning('No migration script(s) found in %s', source)

    return migrations


def list_migrations() -> None:
    """
    List all migrations
    """
    db_manager: DatabaseBackend = create_db_manager()
    migrations: MigrationList = read_migrations()

    headers: list = ["Version", "Description", "Type", "State"]
    table: list = []

    with db_manager.lock():
        history: list = db_manager.get_applied_migration_hashes()

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
    """
    Apply all pending migrations to the database. If no pending migrations found and is in development mode,
    it reapplies the last applied migration.

    Args:
        develop (bool): Whether to run the migrations in development mode (default: False)
    """
    db_manager: DatabaseBackend = create_db_manager()
    migrations: MigrationList = read_migrations()

    if not migrations:
        return

    # Log current status
    list_migrations()

    # Perform migrations
    with db_manager.lock():
        unapplied: MigrationList = db_manager.to_apply(migrations)

        def apply_migrations(revisions: MigrationList) -> None:
            for revision in revisions:
                logger.debug("Migrating database to version '%s'", revision.id)
                db_manager.apply_one(revision)

            for revision in revisions.post_apply:
                logger.debug("Running post-apply script '%s'", revision.id)
                db_manager.apply_one(revision, mark=False)

        def rollback_revisions(revisions: MigrationList) -> None:
            for revision in revisions:
                logger.debug("Rolling back database from version '%s'", revision.id)
                db_manager.rollback_one(revision)

        if len(unapplied) > 0:
            # Apply any pending migrations
            logger.info("Applying pending migrations to database")
            apply_migrations(unapplied)
            logger.info("Successfully applied %d migrations to database", len(unapplied))

        elif develop:
            # Re-apply last migration
            logger.info("Re-applying last migration to database")
            last_migration = db_manager.to_rollback(migrations)[:1]
            rollback_revisions(last_migration)
            unapplied: MigrationList = db_manager.to_apply(migrations)
            apply_migrations(unapplied)
            logger.info("Successfully re-applied last migration to database")

        else:
            # No migration needed
            logger.info('Database up-to-date, no migration needed')


# ----------------------------------------------------------------
# Generate New Migration Script
# ----------------------------------------------------------------

def new_migration(message: str) -> None:
    """
    Creates a new migration script with the given message.

    Args:
        message (str): The given message denoting the migration script.
    """
    if not message:
        raise ValueError('Message for migration can not be empty')

    file_name: str = _make_filename(message)
    full_path: str = os.path.join(source, file_name)
    content: str = MIGRATION_TEMPLATE.format(message=message)

    with open(full_path, 'w', encoding='UTF-8') as f:
        f.write(content)
        print(f"Created file {os.path.relpath(full_path, project_root)}")


def _make_filename(message: str) -> str:
    message = message.strip().split('\n', 1)[0]  # get first line
    message = message.strip()  # strip extra whitespace

    if message:
        slug = "-" + slugify(message)
    else:
        slug = ""

    date_str = date.today().strftime("%Y%m%d")
    number = "01"
    rand = get_random_string(5)

    for path in glob.glob(os.path.join(source, date_str + "_*")):
        try:
            fn_parts = os.path.basename(path).split('_', 2)
            if len(fn_parts) > 1 and number <= fn_parts[1]:  # lexicographical comparison
                number = str(int(fn_parts[1]) + 1).zfill(2)
        except ValueError:
            ...

    return os.path.join(source, f"{date_str}_{number}_{rand}{slug}.py")


if __name__ == '__main__':
    # Run pending migrations (if any)
    perform_migrations()
