from typing import Sequence, Iterator
from sqlalchemy import URL, RowMapping
from sqlalchemy import create_engine, text, Row
from loguru import logger
import queries


class ServiceWorker:

    def __init__(self,
                 batch_size: int,
                 driver_name: str, user_name: str, password: str,
                 host: str, port: int, database: str):
        self._tx_size = batch_size
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

    def execute(self) -> None:
        already_completed_tx_count, is_done = self._get_service_worker_status()

        if is_done:
            logger.info(f"Service worker is already done; completed_tx_count = {already_completed_tx_count}")
            return
        logger.info(f"Service worker is not done; completed_tx_count = {already_completed_tx_count}")

        offset = already_completed_tx_count * self._tx_size
        logger.info(f"Offset = {offset}")
        for txi, tx_rows in enumerate(self._get_txed_rows(offset, self._tx_size)):
            logger.info(f"Processing tx {already_completed_tx_count + txi}")
            with self._connection.begin():
                for dict_row in tx_rows:
                    self._connection.execute(text(queries.NOTHING_IS_MORE_CONSTANT_THAN_TEMPORARY), dict_row)
                self._connection.execute(text(queries.INCREMENT_COMPLETED_TRANSACTION_COUNT))

        self._set_service_worker_status_done()
        total_tx_count = self._fetch_total_tx_count()
        logger.info(f"Service worker is done, total tx count = {total_tx_count}")

    def _get_service_worker_status(self) -> Row:
        with self._connection.begin():
            return self._connection.execute(text(queries.GET_SERVICE_WORKER_STATUS)).one()

    def _get_txed_rows(self, offset: int, tx_size: int) -> Iterator[Sequence[RowMapping]]:
        with (self._connection.begin()):
            return self._connection.execute(text(queries.GET_ZNO), {"n": offset}).mappings().partitions(size=tx_size)

    def _set_service_worker_status_done(self) -> None:
        with self._connection.begin():
            self._connection.execute(text(queries.SET_SERVICE_WORKER_STATUS_DONE))

    def _fetch_total_tx_count(self) -> int:
        with self._connection.begin():
            return self._connection.execute(text(queries.GET_COMPLETED_TX_COUNT)).scalar_one()