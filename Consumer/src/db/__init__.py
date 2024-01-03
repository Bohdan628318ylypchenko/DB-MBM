import os
from .postgres import DB


def _create_database() -> DB:
    return DB(
       driver_name="postgresql+psycopg2",
       user_name=os.environ["POSTGRES_USER"],
       password=os.environ["POSTGRES_PASSWORD"],
       host=os.environ["POSTGRES_HOST"],
       port=int(os.environ["POSTGRES_PORT"]),
       database=os.environ["POSTGRES_DB"]
    )


_db = _create_database()


def get_db() -> DB:
    return _db
