import pymysql
import pandas as pd
import json
from typing import Any, List, Optional
from ensure import ensure_annotations


class MySQLOperation:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def create_connection(self):
        """
        Establishes a connection to the MySQL database.
        """
        if not self.connection:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        return self.connection

    def execute_query(self, query: str, params: Optional[List[Any]] = None):
        """
        Executes a given SQL query.
        """
        connection = self.create_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()

    def fetch_query(self, query: str, params: Optional[List[Any]] = None) -> List[tuple]:
        """
        Executes a SELECT query and fetches results.
        """
        connection = self.create_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        return result

    def create_table(self, table_name: str, schema: str):
        """
        Creates a table with the given name and schema.
        Example schema: "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT"
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.execute_query(query)

    def insert_record(self, table_name: str, record: dict):
        """
        Inserts a single record into the specified table.
        """
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["%s"] * len(record))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, list(record.values()))

    def bulk_insert(self, table_name: str, datafile: str):
        """
        Performs a bulk insert from a CSV or Excel file.
        """
        # Read the datafile into a DataFrame
        if datafile.endswith('.csv'):
            dataframe = pd.read_csv(datafile)
        elif datafile.endswith('.xlsx'):
            dataframe = pd.read_excel(datafile)
        else:
            raise ValueError("Unsupported file format. Use .csv or .xlsx")

        # Convert DataFrame to list of tuples
        records = [tuple(x) for x in dataframe.to_records(index=False)]
        columns = ", ".join(dataframe.columns)
        placeholders = ", ".join(["%s"] * len(dataframe.columns))

        # Perform bulk insert
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        connection = self.create_connection()
        with connection.cursor() as cursor:
            cursor.executemany(query, records)
            connection.commit()

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
