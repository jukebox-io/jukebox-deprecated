#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.

import itertools
import os
import pathlib
import textwrap

import click
import yoyo
from tabulate import tabulate
from yoyo.backends import DatabaseBackend
from yoyo.migrations import MigrationList, Migration, topological_sort

from jukebox.database import DATABASE_URL
from jukebox.utils import PROJECT_ROOT, run_shell_command

MIGRATIONS_ROOT: pathlib.Path = PROJECT_ROOT / "migrations"


@click.group()
def cli() -> None:
    """
    JukeBox is an Open Source Music Streaming App. This CLI interface acts as a management console for the server
    environment.
    """
    pass


# //-------------------- server --------------------

@cli.command()
@click.option("--mode", type=click.Choice(["development", "production"]), default="development",
              help="Run server in given mode", show_default=True)
def runserver(mode: str) -> None:
    """Starts the JukeBox API server"""

    # Note: currently windows does not support production mode
    match mode:
        case "production":
            # Run with multiple workers and load balancing
            run_shell_command("gunicorn jukebox.main:app -c misc/gunicorn.conf.py")

        case "development":
            # Run with single worker and hot-reloading
            run_shell_command("uvicorn jukebox.main:app --reload")

        case _:
            raise ValueError("Invalid mode selected for runserver command: " + mode)


# //-------------------- migrations --------------------

@cli.command()
@click.option("--develop", is_flag=True,
              help="Run in development mode i.e., if there are no unapplied migrations, rollback and reapply the most "
                   "recent migration")
def migrate(develop: bool) -> None:
    """Run pre-start tasks including db migrations"""

    # Initialize Backend
    backend: DatabaseBackend = yoyo.get_backend(f'{DATABASE_URL}')
    migrations: MigrationList = yoyo.read_migrations(f'{MIGRATIONS_ROOT}')

    click.echo("Yoyo migrations " + yoyo.__version__)
    click.echo("Database: " + DATABASE_URL.obscure_password)

    if migrations:
        click.echo(f"Successfully read {len(migrations)} migration script(s) from {MIGRATIONS_ROOT}")
        click.echo()

        # List Migrations
        list_migrations(backend, migrations)

        # Apply Migrations
        run_migrations(backend, migrations, develop)

    else:
        click.echo(f"No migration script(s) found in {MIGRATIONS_ROOT}", err=True)
        click.echo()


def list_migrations(backend: DatabaseBackend, migrations: MigrationList) -> None:
    """List the current state of database migration in a tabular form

    Args:
        backend (DatabaseBackend): The database backend to use.
        migrations (MigrationList): The list of all migrations read from files.
    """

    click.echo("Migrations:")

    with backend.lock():
        applied_migration_hashes = backend.get_applied_migration_hashes()

        def prepare_data(m: Migration, is_post_apply: bool = False) -> list[str]:
            # reference id
            ref_id: str = textwrap.shorten(m.id, width=50, placeholder='...')

            # description of migration
            description: str = textwrap.shorten(
                m.module.__doc__.splitlines()[0].strip(), width=70, placeholder='...')

            # type of migration
            script_type: str = "SQL" if m.is_raw_sql() else "SCRIPT"

            # status of migration
            status: str = "Post-apply"
            if not is_post_apply:
                status = "Success" if m.hash in applied_migration_hashes else "Pending"

            return [ref_id, description, script_type, status]

        headers = ["Version", "Description", "Type", "State"]
        data = [prepare_data(m) for m in topological_sort(migrations)]

        if migrations.post_apply:
            data = itertools.chain(data, [prepare_data(m) for m in topological_sort(migrations.post_apply)])

        click.echo(tabulate(data, headers, tablefmt="simple_outline"))
        click.echo()


def run_migrations(backend: DatabaseBackend, migrations: MigrationList, develop: bool = False) -> None:
    """Applies any unapplied migrations to the target database

    If running in development mode, and there are no unapplied migrations, rollback and reapply the most recent
    migration. This is preferred when writing migration scripts during development.

    Args:
        backend (DatabaseBackend): The database backend to use.
        migrations (MigrationList): The list of all migrations read from files.
        develop (bool): Should run in development mode. (default: false)
    """

    def apply_migrations(to_apply: MigrationList) -> None:
        # apply pending migrations
        for m in to_apply:
            click.echo(f" - Migrating database to version '{m.id}'")
            backend.apply_one(m)

        # apply post-apply migrations
        for m in to_apply.post_apply:
            click.echo(f" - Running post-apply script '{m.id}'")
            backend.apply_one(m, mark=False)

    def rollback_migrations(to_rollback: MigrationList) -> None:
        # rollback last n migrations
        for m in to_rollback:
            click.echo(f" - Rolling back database from version '{m.id}'")
            backend.rollback_one(m)

    # apply migrations
    with backend.lock():
        unapplied_migrations: MigrationList = backend.to_apply(migrations)
        if len(unapplied_migrations) > 0:
            # has some unapplied migrations
            click.echo(f"Applying {len(unapplied_migrations)} migration(s):")

            apply_migrations(unapplied_migrations)
            click.echo()

            click.echo(f"Successfully applied {len(unapplied_migrations)} migration(s) to database")
            click.echo()

        elif develop:
            # develop flag is set
            count = 1  # last 1 migration

            click.echo(f"Reapplying last {count} migration(s):")
            rollback_migrations(backend.to_rollback(migrations)[:count])

            unapplied_migrations: MigrationList = backend.to_apply(migrations)
            apply_migrations(unapplied_migrations)
            click.echo()

            click.echo(f"Successfully applied {len(migrations)} migration(s) to database")
            click.echo()

        else:
            click.echo("Database up-to-date, no migration needed")
            click.echo()


@cli.command()
@click.option("--message", "-m", prompt="Please describe your migration",
              help="Message or description of your migration")
@click.option("--scriptable", is_flag=True, help="Create migration file in scriptable format")
def make_migration(message: str, scriptable: bool):
    """Create a new db migration script"""

    # create migration scripts folder if not exist
    os.makedirs(MIGRATIONS_ROOT, exist_ok=True)

    # create migration file using the "yoyo-migrate new" command
    message = message.replace("\"", "\\\"")
    options = f"--no-config-file --batch --message \"{message}\""
    if not scriptable:
        options += " --sql"
    run_shell_command(f"yoyo-migrate new {options} {MIGRATIONS_ROOT}")


# //-------------------- docker --------------------

@cli.command()
def build_image():
    """Build docker image to be used by tools like kubernetes"""
    run_shell_command("docker build --force-rm -t jukebox:latest .")


@cli.command()
def compose_up():
    """Start the default docker compose server"""
    run_shell_command("docker-compose up --remove-orphans")


@cli.command()
def compose_down():
    """Stop the default docker compose server"""
    run_shell_command("docker-compose down --remove-orphans")


# //-------------------- main --------------------

if __name__ == '__main__':
    # Entrypoint for the cli
    cli()
