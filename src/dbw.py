from dbutils import DbUtils
from queries import QueryTemplates, Query
from loguru import logger
import os, csv, re, itertools


class TxValidator:
    """
    Implements tx cache validation.
    """
    def __init__(self, tx_v: str):
        self._tx_v = tx_v

    def validate_tx_cache(self) -> bool:
        """
        Checks if transaction split was done.
        """
        if os.path.isfile(self._tx_v):
            logger.info("Tx cache is valid :)")
            return True
        else:
            logger.info("Tx cache is INVALID.")
            return False


class DataFilter:
    """
    Implements data validation, split of original data
    into separate files (1 file = 1 transaction).
    """
    def __init__(self,
                 data_dir_path: str):
        # Expected data scheme
        self._DATA_SCHEME = ['OUTID', 'Birth', 'SEXTYPENAME', 'REGNAME', 'AREANAME', 'TERNAME', 'REGTYPENAME', 'TerTypeName', 'ClassProfileNAME', 'ClassLangName', 'EONAME', 'EOTYPENAME', 'EORegName', 'EOAreaName', 'EOTerName', 'EOParent',
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
                             'spaTest', 'spaTestStatus', 'spaBall100', 'spaBall12', 'spaDPALevel', 'spaBall', 'spaPTName', 'spaPTRegName', 'spaPTAreaName', 'spaPTTerName']

        # Paths to input files
        self._input_paths = self._get_data_paths_in_dir(data_dir_path)

        # Input name regex
        self._input_name_pattern = re.compile("d\d{2}.csv")

    def _get_data_paths_in_dir(self, data_dir_path: str) -> list[str]:
        """
        Returns list of all .csv paths in data directory.
        """
        # List to append paths to
        result = []

        # Iterating though paths in data dir
        for current_input_path in os.listdir(data_dir_path):
            if current_input_path.endswith(".csv"):
                # Getting full path
                current = os.path.join(data_dir_path, current_input_path)

                # Adding
                result.append(current)

                # Logging
                logger.debug(f"Added input file: {current}")
        
        # Returning
        return result

    def filter_valid_data(self) -> list[str]:
        """
        Validates input data:
        For each csv file in input dir checks if columns are correspond to data scheme.
        Returns list of paths to valid files in input directory.
        Copies all invalid files to path_to_invalid dir
        """
        # List to store paths to valid input
        result = []

        # Iterating though input files
        for current_input_path in self._input_paths:
            # Logging
            logger.info(f"Validating file: {current_input_path}")

            # Opening current file
            with open(current_input_path, newline = '') as current_input_file:
                # csv reader for current file
                reader = csv.reader(current_input_file, delimiter = ";")

                # Reading header
                header = next(reader)

                # Checking
                if ((header == self._DATA_SCHEME) 
                    and 
                    (self._input_name_pattern.fullmatch(current_input_path.split('/')[-1]))):
                    # Appending to result
                    result.append(current_input_path)

                    # Logging
                    logger.info(f"File {current_input_path} is valid.")
                else:
                    # Logging
                    logger.error(f"File {current_input_path} is invalid.")

        # Returning
        return result


class TxPreprocessor:
    """
    Implements mapping (data from list of files -> transaction list)
    """
    def __init__(self, 
                 data_paths: list[str],          
                 tx_path: str,
                 tx_v: str,
                 tx_size: int):
        self._data_paths = data_paths
        self._tx_path = tx_path
        self._tx_v = tx_v
        self._tx_size = tx_size

    def split_data_into_tx(self) -> None:
        """
        Returns transaction list
        """
        # Iterating though paths
        tx_counter = 0
        for data_path in self._data_paths:
            # Opening current path
            with open(data_path, newline='') as data:
                # Create reader
                reader = csv.reader(data, delimiter=';')

                # Skipping header
                next(reader)

                # Creating txs
                year = data_path.split('/')[-1][1:3]
                for j, batch in enumerate(iter(lambda: list(itertools.islice(reader, self._tx_size)), [])):
                    # Output filename
                    output_filename = self._tx_path + f"/tx-{year}-{tx_counter}.csv"

                    # Writing
                    with open(output_filename, 'w', newline='') as outfile:
                        writer = csv.writer(outfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                        writer.writerows(batch)

                    # Logging
                    logger.info(f"Created tx{tx_counter}")

                    # Incrementing global tx counter
                    tx_counter += 1
        
        # Finishing with verification
        v = open(self._tx_v, "x")
        v.close()

        # Logging
        logger.info("Finished creating transactions.")


class DbWriter:
    """
    Implements data population of database.
    """
    def __init__(self,
                 utils: DbUtils,
                 tx_vname: str, tx_path: str):
        self._utils = utils
        self._tx_path = tx_path
        self._tx_vname = tx_vname
        self._decimal_pattern = re.compile("\d+,\d+")
        self._integer_pattern = re.compile("\d+")

    def write(self) -> None:
        """
        Data population entry point.
        """
        # Get completed transaction count
        completed_count = self._utils.execute_commit_or_wait((Query(QueryTemplates.COMPLETED_TRANSACTION_COUNT, (), True),))[0][0][0]
        logger.info(f"Completed before: {completed_count}")

        # Getting transaction list
        tx_list = [f for f in os.listdir(self._tx_path)]
        tx_list.remove(self._tx_vname)

        # Running transactions
        for i in range(completed_count, len(tx_list)):
            # Opening data for current transaction
            with open(self._tx_path + '/' + tx_list[i], newline = '') as tx:
                # Creating reader
                reader = csv.reader(tx, delimiter = ';')

                # Reading rows into tx data
                tx_data = []
                for row in reader:
                    # Converting
                    for k in range(len(row)):
                        if row[k] == "null":
                            row[k] = None
                            continue
                        if self._decimal_pattern.fullmatch(row[k]) != None:
                            row[k] = float(row[k].replace(',', '.'))
                            continue
                        if self._integer_pattern.fullmatch(row[k]) != None:
                            row[k] = int(row[k])
                            continue

                    # Adding year
                    row.append(2000 + int(tx_list[i].split('-')[1]))

                    # Adding to tx data
                    tx_data.append(tuple(row))
                
                # Execute transaction
                tx_queries = list(map(lambda q_args: Query(QueryTemplates.INSERT_ZNO, q_args, False), tx_data))
                tx_queries.append(Query(QueryTemplates.INCREMENT_COMPLETED_TRANSACTION_COUNT, (), False))
                self._utils.execute_commit_or_wait(tx_queries)
            
                # Logging
                logger.info(f"Finished transaction #{i}")


def run(input_dir_path: str, 
        tx_path: str, 
        tx_vname: str,
        tx_size: int) -> None:
    """
    Runs dbw functionality
    """
    # Tx validation flag path
    tx_v = tx_path + '/' + tx_vname

    # Check if there is need to load and split data
    if not TxValidator(tx_v).validate_tx_cache():
        # Filter data
        valid_data = DataFilter(input_dir_path).filter_valid_data()

        # Transaction split
        TxPreprocessor(valid_data, tx_path, tx_v, tx_size).split_data_into_tx()

    # Writing
    DbWriter(DbUtils.get_instance(), tx_vname, tx_path).write()