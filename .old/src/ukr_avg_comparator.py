from queries import Query, QueryTemplates
from dbutils import DbUtils
from loguru import logger
import datetime, csv


def run(output_dir_path: str):
    """
    Compare ukr average score 2019 vs 2020 for all those passed.
    """
    def convert_decimal_or_not(x):
        if not isinstance(x, str):
            return str(round(x, 2))
        else:
            return x

    # Getting data from db
    q = Query(QueryTemplates.AVG_UKR_PASSED_BY_REGION, (), True)
    result = DbUtils.get_instance().execute_commit_or_wait((q,))

    # Saving
    logger.debug(result)
    with open(output_dir_path + '/' + f"compare{datetime.datetime.now()}.csv", mode = "w") as file:
        writer = csv.writer(file)
        writer.writerow(("Регіон", "Середній бал укр.мова/укр.літ (зараховано) 2019", 
                                   "Середній бал укр.мова/укр.літ (зараховано) 2020"))
        converted = map(lambda row: map(convert_decimal_or_not, row), result[0])
        writer.writerows(converted)