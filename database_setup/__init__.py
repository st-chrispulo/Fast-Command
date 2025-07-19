from .env_setup import EnvSetup
from .db_creator import DBCreator
from .migration_runner import MigrationRunner
from pathlib import Path
from logger import logger


def initialize_database():
    env_file = Path(".env")

    if not env_file.exists():
        env = EnvSetup(init_env_path=".env.init")
        creator = DBCreator(env)
        creator.create()
    else:
        logger.info(".env already exists, skipping DB and user creation.")


def initialize_migration_table(migrations_dir):
    env = EnvSetup(".env")
    runner = MigrationRunner(env, migrations_dir)
    runner.run()
