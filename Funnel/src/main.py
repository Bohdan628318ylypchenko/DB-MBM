from dbconn import DbConnection
from funnel import ZNOFunnel
import os


def main():
    DbConnection.initialize(host=os.environ["POSTGRES_HOST"],
                            port=int(os.environ["POSTGRES_PORT"]),
                            dbname=os.environ["POSTGRES_DB"],
                            user=os.environ["POSTGRES_USER"],
                            password=os.environ["POSTGRES_PASSWORD"],
                            dberror_sleep_time=int(os.environ["APP_DBERR_SLEEP"]))

    zno_funnel = ZNOFunnel(DbConnection.get_instance(),
                           os.environ["APP_INPUT_DIR"],
                           int(os.environ["APP_TX_SIZE"]))

    zno_funnel.execute()

    DbConnection.get_instance().close_connection()


if __name__ == "__main__":
    main()