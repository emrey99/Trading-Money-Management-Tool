import mysql.connector
from mysql.connector import Error
from threading import Lock
from decimal import Decimal


class CombinationDB:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Ensure that only one instance of CombinationDB is created."""
        if not cls._instance:
            with cls._lock:  # Thread-safe initialization
                if not cls._instance:  # Double-check locking
                    cls._instance = super(CombinationDB, cls).__new__(cls)
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

    def __execute_and_commit(self, query, params):
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

    def get_combination(self, technical_category, fundamental_category):
        query = "SELECT * FROM combinations WHERE technical_category = %s AND fundamental_category = %s"
        params = (technical_category, fundamental_category)
        return self.execute_query(query, params)

    def create_combination(self, technical_category, fundamental_category, initial_weight=0):
        query = "INSERT INTO combinations (technical_category, fundamental_category, weight) VALUES (%s, %s, %s)"
        params = (technical_category, fundamental_category, initial_weight)
        self.__execute_and_commit(query, params)

    def update_combination_weight(self, combination_id, trade_result):
        current_weight = self.__get_current_weight(combination_id)
        update_weight_method = {
            'win': self.__handle_win,
            'loss': self.__handle_loss
        }.get(trade_result, lambda weight: weight)

        new_weight = update_weight_method(current_weight)
        self.__update_weight(combination_id, new_weight)

    def __get_current_weight(self, combination_id):
        query = "SELECT weight FROM combinations WHERE combination_id = %s"
        params = (combination_id,)
        result = self.execute_query(query, params)
        return result[0] if result else 0.0

    @staticmethod
    def __handle_win(current_weight):
        return current_weight + Decimal('0.5')

    @staticmethod
    def __handle_loss(current_weight):
        if current_weight > 0:
            return 0.0
        elif current_weight <= 0:
            return Decimal('-0.5')
        return current_weight

    def __update_weight(self, combination_id, new_weight):
        update_query = "UPDATE combinations SET weight = %s WHERE combination_id = %s"
        params = (new_weight, combination_id)
        self.__execute_and_commit(update_query, params)

    @staticmethod
    def get_combination_id(combination):
        try:
            return combination[0]
        except (TypeError, IndexError):
            return None

    @staticmethod
    def get_combination_weight(combination):
        try:
            return combination[-1]
        except (TypeError, IndexError):
            return None
