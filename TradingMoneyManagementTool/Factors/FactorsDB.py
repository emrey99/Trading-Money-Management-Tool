from threading import Lock
import mysql.connector
from mysql.connector import Error


class FactorsDB:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Ensure that only one instance of FactorsDB is created."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(FactorsDB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'connection'):
            self.connection = None
            self.cursor = None
            self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                database="trading_system",
                password="Password"
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully!")
        except Error as err:
            print(f"Error connecting to the database: {err}")
            self.close_connection()
            raise

    def close_connection(self):
        """Close the database connection and cursor."""
        if self.connection and self.connection.is_connected():
            try:
                self.cursor.close()
                self.connection.close()
                print("Connection closed successfully!")
            except Error as err:
                print(f"Error closing the connection: {err}")

    def __execute_and_commit(self, query, values):
        """Execute a query and commit changes."""
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except Error as err:
            print(f"Error executing query: {err}")
            self.__rollback()
            raise

    def __rollback(self):
        """Rollback the transaction in case of failure."""
        try:
            self.connection.rollback()
            print("Transaction rolled back.")
        except Error as err:
            print(f"Error rolling back transaction: {err}")

    def insert_technicals(self, trade_id, technical_values):
        """Insert technical factors into the database."""
        query = """
        INSERT INTO technicals (
            trade_id,
            volume, 
            overall_trend, 
            liquidity_sweep, 
            reaction_zone, 
            ote_level, 
            extra_setup, 
            good_attack_point
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            trade_id,
            technical_values["volume"],
            technical_values["overall_trend"],
            technical_values["liquidity_sweep"],
            technical_values["reaction_zone"],
            technical_values["ote_level"],
            technical_values["extra_setup"],
            technical_values["good_attack_point"]
        )
        self.__execute_and_commit(query, values)

    def insert_fundamentals(self, trade_id, fundamental_values):
        """Insert fundamental factors into the database."""
        query = """
        INSERT INTO fundamentals (
            trade_id,
            vix, 
            geopolitical_sector_situation, 
            daily_news_result
        )
        VALUES (%s, %s, %s, %s)
        """
        values = (
            trade_id,
            fundamental_values["vix"],
            fundamental_values["geopolitical_sector_situation"],
            fundamental_values["daily_news_result"]
        )
        self.__execute_and_commit(query, values)
