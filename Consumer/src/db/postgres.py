from typing import Any
from sqlalchemy import (
    create_engine,
    text,
    RowMapping,
    Sequence,
    URL
)


class DB:

    def __init__(
        self,
        driver_name: str,
        user_name: str,
        password: str,
        host: str,
        port: int,
        database: str
    ) -> None:
        self._engine = create_engine(
            URL.create(
                driver_name,
                username=user_name,
                password=password,
                host=host,
                port=port,
                database=database
            )
        )
        self._connection = self._engine.connect()

    def fetch_one(
        self,
        query: str,
        values: dict[str, Any]
    ) -> RowMapping:
        with self._connection.begin():
            return self._connection.execute(text(query), values).mappings().one()

    def fetch_all(
        self,
        query: str,
        values: dict[str, Any]
    ) -> Sequence[RowMapping]:
        with self._connection.begin():
            return self._connection.execute(text(query), values).mappings().all() # type: ignore

    def execute(
        self,
        query: str,
        values: dict[str, Any]
    ) -> None:
        with self._connection.begin():
            self._connection.execute(text(query), values)

