import mysql.connector
from mysql.connector import Error
from threading import Lock
from datetime import datetime


class TradesDB:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradesDB, cls).__new__(cls)
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
        if self.connection and self.connection.is_connected():
            try:
                self.cursor.close()
                self.connection.close()
                print("Connection closed successfully!")
            except Error as err:
                print(f"Error closing the connection: {err}")

    def __execute_and_commit(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Error as err:
            print(f"Error executing query: {err}")
            self.__rollback()
            raise

    def __rollback(self):
        try:
            self.connection.rollback()
            print("Transaction rolled back.")
        except Error as err:
            print(f"Error rolling back transaction: {err}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Error as err:
            print(f"Error executing query: {err}")
            return None

    def get_open_trades(self):
        query = "SELECT * FROM trades WHERE status = 'open'"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as err:
            print(f"Error fetching open trades: {err}")

    def update_trade_status(self, trade_id, status, result):
        query = """
         UPDATE trades 
         SET status = %s, result = %s, end_time = %s 
         WHERE trade_id = %s
         """
        params = (status, result, datetime.now(), trade_id)
        self.__execute_and_commit(query, params)

    def insert_trade(self, combination_id, direction, result=None, status="open"):
        query = """
        INSERT INTO trades (direction, combination_id, result, start_time, status) 
        VALUES (%s, %s, %s, %s, %s)
        """
        current_time = datetime.now()
        self.__execute_and_commit(query, (direction, combination_id, result, current_time, status))
