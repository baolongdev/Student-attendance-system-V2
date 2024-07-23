import sqlite3
import os
import threading

class DatabaseHandler:
    _local = threading.local()

    def __init__(self, db_name):
        self.db_name = os.path.abspath(db_name)
        self.db_directory = os.path.dirname(self.db_name)

    def _get_connection(self):
        if not hasattr(DatabaseHandler._local, "connection"):
            if not os.path.exists(self.db_directory):
                os.makedirs(self.db_directory)
            DatabaseHandler._local.connection = sqlite3.connect(self.db_name)
            print(f"Connected to database: {self.db_name}")
        return DatabaseHandler._local.connection

    def _close_connection(self):
        if hasattr(DatabaseHandler._local, "connection"):
            DatabaseHandler._local.connection.close()
            delattr(DatabaseHandler._local, "connection")
            print("Disconnected from database")

    def connect(self):
        self._get_connection()

    def disconnect(self):
        self._close_connection()

    def create_table(self, table_name, columns):
        try:
            with self._get_connection() as conn:
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
                conn.execute(query)
                print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name, data):
        if data is None or data[0] is None:
            print("Invalid data or 'id' is None. Nothing to insert.")
            return
        try:
            with self._get_connection() as conn:
                query = f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in data])})"
                conn.execute(query, data)
                print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def update_data(self, table_name, data, id_value):
        try:
            with self._get_connection() as conn:
                set_values = ", ".join([f"{column} = ?" for column in data.keys()])
                query = f"UPDATE {table_name} SET {set_values} WHERE id = ?"
                conn.execute(query, list(data.values()) + [id_value])
                print("Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def select_data(self, table_name, columns="*", condition=None):
        try:
            with self._get_connection() as conn:
                query = f"SELECT {columns} FROM {table_name}"
                if condition:
                    query += f" WHERE {condition}"
                cursor = conn.execute(query)
                rows = cursor.fetchall()
                return rows
        except sqlite3.Error as e:
            print(f"Error selecting data: {e}")
            return None
    def check_status(self, id_value):
        try:
            with self._get_connection() as conn:
                query = f"SELECT status FROM students WHERE id = ?"
                cursor = conn.execute(query, [id_value])
                status = cursor.fetchone()
                if status is not None:
                    return bool(status[0])  # Convert to boolean
                else:
                    return False  # Return False if the id is not found in the database
        except sqlite3.Error as e:
            print(f"Error checking status: {e}")
            return False  # Return False if there's any error in the query or connection