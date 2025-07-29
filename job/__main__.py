import os
import argparse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from job.executors.queue_executor import queue_executor_loop
from job.executors.scheduler_executor import scheduler_executor_loop


def build_db_session():
    load_dotenv()

    user = os.getenv("PG_DB_USER")
    password = os.getenv("PG_DB_PASSWORD")
    host = os.getenv("PG_DB_HOST")
    port = os.getenv("PG_DB_PORT")
    dbname = os.getenv("PG_DB_NAME")

    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(db_url, pool_pre_ping=True)
    return sessionmaker(bind=engine)


def main():
    parser = argparse.ArgumentParser(description="Run job executor")
    parser.add_argument("--mode", choices=["queue", "scheduler"], default="queue")
    args = parser.parse_args()

    db_session_factory = build_db_session()

    if args.mode == "queue":
        queue_executor_loop(db_session_factory)
    elif args.mode == "scheduler":
        scheduler_executor_loop(db_session_factory)


if __name__ == "__main__":
    main()
