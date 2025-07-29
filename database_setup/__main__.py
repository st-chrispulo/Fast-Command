import argparse
import psycopg2
import os
from . import initialize_database, initialize_migration_table
from logger import logger
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize DB and run migrations.")
    parser.add_argument("--migrations-dir", default="migrations", help="Path to SQL migrations directory")
    args = parser.parse_args()

    if not os.path.exists(args.migrations_dir):
        logger.error(f"Migrations path '{args.migrations_dir}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(args.migrations_dir):
        logger.error(f"Path '{args.migrations_dir}' is not a directory.")
        sys.exit(1)

    migration_files = [f for f in os.listdir(args.migrations_dir) if f.endswith(".sql")]

    if not migration_files:
        logger.warning(f"No .sql migration files found in '{args.migrations_dir}'.")
    else:
        logger.info(f"Found {len(migration_files)} migration file(s):")
        for file in sorted(migration_files):
            logger.info(f"  - {file}")

    try:
        initialize_database()
        initialize_migration_table(migrations_dir=args.migrations_dir)
    except psycopg2.OperationalError as e:
        logger.error(f"PostgreSQL connection error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error during initialization:")
        sys.exit(1)
