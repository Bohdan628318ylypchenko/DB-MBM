import psycopg2
from psycopg2.extensions import connection
from time import sleep
from loguru import logger


class DbUtils:
    """
    Class to simplify bd connection management,
    implement wait-until done functionality, etc.
    """
    # Singleton holder
    _instance = None

    def __init__(self, host: str, port: int, dbname: str,
                 user: str, password: str,
                 dberror_sleep_time: int):
        """
        Default constructor.
        Don't call it directly, use initialize instead.
        """
        # Connection properties
        self._host = host
        self._port = port
        self._dbname = dbname
        self._user = user
        self._password = password

        # Time to wait between connection attempts
        self._sleep_time = dberror_sleep_time

        # Create connection
        self._connection = self._get_db_connection_or_wait()

    @classmethod
    def initialize(cls,
                   host: str, port: int, dbname: str,
                   user: str, password: str,
                   dberror_sleep_time: int) -> None:
        """
        Initializes singleton instance.
        """
        # Initializing singleton instance
        cls._instance = DbUtils(host=host,
                                port=port,
                                dbname=dbname,
                                user=user,
                                password=password,
                                dberror_sleep_time=dberror_sleep_time)
        # Logging
        logger.debug("Connection initialized.")

    @classmethod
    def get_instance(cls):
        """
        Singleton instance getter.
        """
        return cls._instance

    def _get_db_connection_or_wait(self) -> connection:
        """
        Creates connection to db.
        Warning: method waits for db until connected.
        """
        # Cycle until connect
        while (True):
            try:
                # Attempt to connect
                logger.info("Connection attempt.")
                return psycopg2.connect(host=self._host,
                                        port=self._port,
                                        dbname=self._dbname,
                                        user=self._user,
                                        password=self._password)
            except psycopg2.DatabaseError as e:
                # Logging error
                logger.error(e)

                # Sleeping between attempts
                sleep(self._sleep_time)

    def execute_commit_or_wait(self, queries) -> list:
        """
        Tries to execute and commit tuple of queries until done.
        """
        while (True):
            try:
                # Creating cursor
                cursor = self._connection.cursor()

                # Executing
                result = []
                for q in queries:
                    cursor.execute(q.get_template(), q.get_q_args())
                    if q.expect_return():
                        result.append(cursor.fetchall())

                # Committing
                self._connection.commit()

                # Returning
                return result

            except psycopg2.Error as e:
                # Logging error
                logger.error(f"Failed to commit transaction. Error: {e}")

                # Closing current connection
                self.close_connection()

                # Reconnecting
                self._connection = self._get_db_connection_or_wait()

    def close_connection(self) -> None:
        """
        Closes current open connection, makes field None.
        """
        # Closing connection
        self._connection.close()

        # Reassign None
        self._connection = None

        # Logging
        logger.debug("Connection closed.")