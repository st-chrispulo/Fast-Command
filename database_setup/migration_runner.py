import psycopg2
from pathlib import Path
from logger import logger


class MigrationRunner:
    def __init__(self, env_setup, migrations_dir):
        self.env = env_setup
        self.migrations_dir = Path(migrations_dir)

        self.conn = psycopg2.connect(
            dbname=self.env.get("PG_DB_NAME"),
            user=self.env.get("PG_DB_USER"),
            password=self.env.get("PG_DB_PASSWORD"),
            host=self.env.get("PG_DB_HOST"),
            port=self.env.get("PG_DB_PORT"),
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def ensure_migration_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tbl_migration_history (
                id SERIAL PRIMARY KEY,
                filename TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT NOW()
            );
        """)
        logger.info("Ensured tbl_migration_history table exists.")

    def get_applied_migrations(self):
        self.cursor.execute("SELECT filename FROM tbl_migration_history;")
        return set(row[0] for row in self.cursor.fetchall())

    def run(self):
        self.ensure_migration_table()
        applied = self.get_applied_migrations()
        all_migrations = sorted(self.migrations_dir.glob("*.sql"))

        pending = [path for path in all_migrations if path.name not in applied]
        applied_count = 0

        for i, path in enumerate(pending, start=1):
            logger.info(f"[{i}/{len(pending)}] Applying migration: {path.name}")
            if path.name in applied:
                logger.info(f"Skipping already applied: {path.name}")
                continue

            logger.info(f"Applying migration: {path.name}")
            with open(path, "r") as f:
                sql = f.read()
                self.cursor.execute(sql)
                self.cursor.execute(
                    "INSERT INTO tbl_migration_history (filename) VALUES (%s);", (path.name,)
                )
                applied_count += 1
        logger.info(f"All migrations complete. Total applied: {applied_count}")
