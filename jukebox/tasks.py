import argparse
import itertools
import os
import subprocess

import psutil
import yoyo
from tabulate import tabulate
from yoyo.backends import DatabaseBackend
from yoyo.exceptions import BadMigration
from yoyo.migrations import topological_sort, MigrationList

from jukebox.settings import ROOT_DIR, MIGRATIONS_DIR, APP_URL, DATABASE_URL


# //-------------------- migrations --------------------

def make_migration_task():
    parser = argparse.ArgumentParser(description="Create a new db migration script")
    parser.add_argument("--message", "-m", dest="message", action="store",
                        help="Message or description of your migration")
    parser.add_argument("--scriptable", dest="scriptable", action="store_true",
                        help="Create file in scriptable format")
    args = parser.parse_args()

    # configure extras
    message = args.message
    if not message:
        message = input("Please describe your migration: ")

    extra_args = ["--no-config-file", "--batch", "--message", '"' + message + '"']
    if not args.scriptable:
        extra_args += ["--sql"]

    # create migration scripts
    os.makedirs(MIGRATIONS_DIR, exist_ok=True)
    execute(f"yoyo-migrate new {' '.join(extra_args)} {MIGRATIONS_DIR}")


def migrate_task():
    parser = argparse.ArgumentParser(description="Run pre-start tasks including db migrations")
    parser.add_argument("--develop", dest="develop", action="store_true",
                        help="Run in development mode")
    args = parser.parse_args()

    # Initialize Backend
    backend: DatabaseBackend = yoyo.get_backend(DATABASE_URL.__str__())
    migrations: MigrationList = yoyo.read_migrations(MIGRATIONS_DIR)

    print("Yoyo migrations", yoyo.__version__)
    print("Database:", DATABASE_URL.obscure_password)
    print(f"Successfully read {len(migrations)} migration script(s)")
    print()

    if not migrations:
        return

    # List Migrations
    with backend.lock():
        headers = ["Version", "Description", "Type", "State"]

        print("Migrations:")
        applied_migration_hashes = backend.get_applied_migration_hashes()
        table = (
            (m.id, m.module.__doc__, "SQL" if m.is_raw_sql() else "SCRIPT",
             "Success" if m.hash in applied_migration_hashes else "Pending")
            for m in topological_sort(migrations)
        )

        if migrations.post_apply:
            post_apply = (
                (m.id, m.module.__doc__, "SQL" if m.is_raw_sql() else "SCRIPT", "Post-apply")
                for m in topological_sort(migrations.post_apply)
            )
            table = itertools.chain(table, post_apply)

        print(tabulate(table, headers, tablefmt="simple_outline"))
        print()

    # Apply Migrations
    with backend.lock():
        def apply_migrations(migrations: MigrationList):  # noqa
            for m in migrations:
                print(f" - Migrating database to version '{m.id}'")
                try:
                    backend.apply_one(m)
                except BadMigration:
                    continue
            for m in migrations.post_apply:
                print(f" - Running post-apply script '{m.id}'")
                backend.apply_one(m, mark=False)
            print()
            print(f"Successfully applied {len(migrations)} migration(s) to database")
            print()

        def rollback_migrations(migrations: MigrationList):  # noqa
            for m in migrations:
                print(f" - Rolling back database from version '{m.id}'")
                try:
                    backend.rollback_one(m)
                except BadMigration:
                    continue

        unapplied_migrations = backend.to_apply(migrations)

        if unapplied_migrations:
            print(f"Applying {len(unapplied_migrations)} migration(s):")
            apply_migrations(unapplied_migrations)

        elif args.develop:
            n = 1

            print(f"Reapplying last {n} migration(s):")
            rollback_migrations(backend.to_rollback(migrations)[:n])

            unapplied_migrations = backend.to_apply(migrations)
            apply_migrations(unapplied_migrations)

        else:
            print("Database up-to-date, no migration needed")
            print()


# //-------------------- server --------------------

def run_server_task():
    parser = argparse.ArgumentParser(description="Starts the JukeBox API server")
    parser.add_argument("--prod", dest="prod", action="store_true",
                        help="run server in production mode")
    args = parser.parse_args()

    # configure server
    if args.prod and not psutil.WINDOWS:
        start_cmd = f"gunicorn {APP_URL} -c misc/gunicorn.conf.py"
    else:
        start_cmd = f"uvicorn {APP_URL} --reload"

    # run server
    execute(start_cmd)


# //-------------------- utils --------------------

def execute(command: str, *, working_dir=ROOT_DIR) -> None:
    """Execute shell commands"""
    subprocess.run(command, shell=True, check=True, cwd=working_dir)
