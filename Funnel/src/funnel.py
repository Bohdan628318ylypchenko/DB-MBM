from dbconn import DbConnection
from queries import QueryFactory
from loguru import logger
from itertools import chain, batched, islice
import os
import csv
import re


DECIMAL_PATTERN = re.compile("\\d+,\\d+")
INTEGER_PATTERN = re.compile("\\d+")
CSV_SUFFIX = ".csv"
ZNO_HEADER = [
    'OUTID', 'Birth', 'SEXTYPENAME', 'REGNAME', 'AREANAME',
    'TERNAME', 'REGTYPENAME', 'TerTypeName',
    'ClassProfileNAME', 'ClassLangName',
    'EONAME', 'EOTYPENAME', 'EORegName', 'EOAreaName', 'EOTerName', 'EOParent',
    'UkrTest', 'UkrTestStatus', 'UkrBall100', 'UkrBall12', 'UkrBall', 'UkrAdaptScale', 'UkrPTName', 'UkrPTRegName', 'UkrPTAreaName', 'UkrPTTerName',
    'histTest', 'HistLang', 'histTestStatus', 'histBall100', 'histBall12', 'histBall', 'histPTName', 'histPTRegName', 'histPTAreaName', 'histPTTerName',
    'mathTest', 'mathLang', 'mathTestStatus', 'mathBall100', 'mathBall12', 'mathBall', 'mathPTName', 'mathPTRegName', 'mathPTAreaName', 'mathPTTerName',
    'physTest', 'physLang', 'physTestStatus', 'physBall100', 'physBall12', 'physBall', 'physPTName', 'physPTRegName', 'physPTAreaName', 'physPTTerName',
    'chemTest', 'chemLang', 'chemTestStatus', 'chemBall100', 'chemBall12', 'chemBall', 'chemPTName', 'chemPTRegName', 'chemPTAreaName', 'chemPTTerName',
    'bioTest', 'bioLang', 'bioTestStatus', 'bioBall100', 'bioBall12', 'bioBall', 'bioPTName', 'bioPTRegName', 'bioPTAreaName', 'bioPTTerName',
    'geoTest', 'geoLang', 'geoTestStatus', 'geoBall100', 'geoBall12', 'geoBall', 'geoPTName', 'geoPTRegName', 'geoPTAreaName', 'geoPTTerName',
    'engTest', 'engTestStatus', 'engBall100', 'engBall12', 'engDPALevel', 'engBall', 'engPTName', 'engPTRegName', 'engPTAreaName', 'engPTTerName',
    'fraTest', 'fraTestStatus', 'fraBall100', 'fraBall12', 'fraDPALevel', 'fraBall', 'fraPTName', 'fraPTRegName', 'fraPTAreaName', 'fraPTTerName',
    'deuTest', 'deuTestStatus', 'deuBall100', 'deuBall12', 'deuDPALevel', 'deuBall', 'deuPTName', 'deuPTRegName', 'deuPTAreaName', 'deuPTTerName',
    'spaTest', 'spaTestStatus', 'spaBall100', 'spaBall12', 'spaDPALevel', 'spaBall', 'spaPTName', 'spaPTRegName', 'spaPTAreaName', 'spaPTTerName',
    'YearOfAttempt'
]
ZNO_DELIMITER = ';'
ZNO_NEWLINE = '\n'


class ZNOFunnel:
    """
    Reads zno data from all csv files in dir by chunks, writes data to db.
    """

    def __init__(self, db_conn: DbConnection, dir_path: str, batch_size: int):
        self._db_conn = db_conn
        self._dir_path = dir_path
        self._batch_size = batch_size

    def execute(self) -> None:
        already_completed_tx_count, is_done = self._get_funnel_status()

        if is_done:
            logger.info(f"Funnel is already done; completed_tx_count = {already_completed_tx_count}; end execution")
            return
        logger.info(f"Funnel is not done; completed_tx_count = {already_completed_tx_count}")

        files, readers = self._prepare_files_readers()
        rows = chain.from_iterable(readers)
        for txi, tx_rows in enumerate(islice(batched(rows, n=self._batch_size), already_completed_tx_count, None)):
            logger.info(f"Processing tx {already_completed_tx_count + txi}")
            self._process_tx(tx_rows)

        self._set_funnel_status_done()
        total_tx_count = self._fetch_total_tx_count()
        logger.info(f"Funnel is done, total tx count = {total_tx_count}")

        for file in files:
            file.close()

    def _get_funnel_status(self) -> tuple:
        get_funnel_status_query = QueryFactory.get_funnel_status()
        return self._db_conn.execute_commit_or_wait((get_funnel_status_query,))[get_funnel_status_query][0]

    def _prepare_files_readers(self) -> tuple:
        files = []
        readers = []
        for zno_relative_path in filter(lambda path: path.endswith(CSV_SUFFIX), os.listdir(self._dir_path)):
            file = open(os.path.join(self._dir_path, zno_relative_path), newline=ZNO_NEWLINE)
            reader = csv.reader(file, delimiter=ZNO_DELIMITER)
            if next(reader) == ZNO_HEADER:
                logger.info(f"ZNO file '{file.name}' has valid header, include for processing")
                files.append(file)
                readers.append(reader)
            else:
                logger.info(f"ZNO file '{file.name}' has invalid header, skip file")
                file.close()
        return files, readers

    def _process_tx(self, tx_rows) -> None:
        tx_queries = []
        for row in tx_rows:
            for k in range(len(row)):
                if row[k] == "null":
                    row[k] = None
                    continue
                if not (DECIMAL_PATTERN.fullmatch(row[k]) is None):
                    row[k] = float(row[k].replace(',', '.'))
                    continue
                if not (INTEGER_PATTERN.fullmatch(row[k]) is None):
                    row[k] = int(row[k])
                    continue
            tx_queries.append(QueryFactory.insert_zno(row))
        tx_queries.append(QueryFactory.increment_completed_transaction_count())
        self._db_conn.execute_commit_or_wait(tx_queries)

    def _set_funnel_status_done(self) -> None:
        set_funnel_status_query = QueryFactory.set_funnel_status_done()
        self._db_conn.execute_commit_or_wait((set_funnel_status_query,))

    def _fetch_total_tx_count(self) -> int:
        get_completed_tx_count_query = QueryFactory.get_completed_tx_count()
        return self._db_conn.execute_commit_or_wait((get_completed_tx_count_query,))[get_completed_tx_count_query][0][0]
