import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .utils import generate_password
from logger import logger


class DBCreator:
    def __init__(self, env_setup):
        self.env = env_setup
        self.app_name = str(self.env.get("APP_NAME")).lower()
        self.init_db = self.env.get("PG_INIT_DB_NAME")
        self.init_user = self.env.get("PG_INIT_DB_USER")
        self.init_password = self.env.get("PG_INIT_DB_PASSWORD")
        self.host = self.env.get("PG_INIT_DB_HOST")
        self.port = self.env.get("PG_INIT_DB_PORT")

        self.new_db = f"{self.app_name}_db"
        self.new_user = f"{self.app_name}_user"
        self.new_password = generate_password()

    def create(self):
        conn = None
        cur = None
        conn_new = None
        cur_new = None

        try:
            conn = psycopg2.connect(
                dbname=self.init_db,
                user=self.init_user,
                password=self.init_password,
                host=self.host,
                port=self.port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (self.new_db,))
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {self.new_db};")
                logger.info(f"Database '{self.new_db}' created.")
            else:
                logger.info(f"Database '{self.new_db}' already exists.")

            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (self.new_user,))
            if not cur.fetchone():
                cur.execute(
                    f"CREATE ROLE {self.new_user} WITH LOGIN PASSWORD %s;",
                    (self.new_password,)
                )
                logger.info(f"User '{self.new_user}' created.")
            else:
                logger.info(f"User '{self.new_user}' already exists.")

            cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {self.new_db} TO {self.new_user};")
            logger.info("Database privileges granted.")

            conn_new = psycopg2.connect(
                dbname=self.new_db,
                user=self.init_user,
                password=self.init_password,
                host=self.host,
                port=self.port
            )
            conn_new.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur_new = conn_new.cursor()

            cur_new.execute(f"GRANT USAGE, CREATE ON SCHEMA public TO {self.new_user};")
            logger.info("Schema privileges granted.")

            self.env.generate_app_env(
                self.new_db,
                self.new_user,
                self.new_password,
                self.host,
                self.port
            )

        except Exception as e:
            logger.error(f"Error during DB creation: {e}")
            raise

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
            if cur_new:
                cur_new.close()
            if conn_new:
                conn_new.close()
