from dbutils import DbUtils
import dbw, ukr_avg_comparator, os


def main():
    """
    Entry point.
    """
    # Initializing db_utils
    DbUtils.initialize(host=os.environ["POSTGRES_HOST"],
                       port=os.environ["POSTGRES_PORT"],
                       dbname=os.environ["POSTGRES_DB"],
                       user=os.environ["POSTGRES_USER"],
                       password=os.environ["POSTGRES_PASSWORD"],
                       dberror_sleep_time=int(os.environ["APP_DBERR_SLEEP"]))

    # Running database data population
    dbw.run(os.environ["APP_INPUT_DIR"],
            os.environ["APP_TX_DIR"],
            os.environ["APP_TX_VNAME"],
            int(os.environ["APP_TRANSACTION_SIZE"]))

    # Comparing
    ukr_avg_comparator.run(os.environ["APP_OUTPUT_DIR"])

    # Closing connection
    DbUtils.get_instance().close_connection()


if __name__ == '__main__':
    main()