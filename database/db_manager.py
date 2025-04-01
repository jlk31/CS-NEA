#===============================================================================
#Modules being imported
#===============================================================================

import sqlite3
from sqlite3 import Error

#================================================================================
#database manager class
#================================================================================

class DBManager:
    def __init__(self, db_file):
        #Initialise the database manager with a database file
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        #Create a database connection to the SQLite database
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Connection to {self.db_file} established.")
        except Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        #Close the database connection
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def execute_query(self, query, params=None):
        #Execute a single query
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error: {e}")

    def fetch_all(self, query, params=None):
        #Fetch all results from a query
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error: {e}")
            return None
