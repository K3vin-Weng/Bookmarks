import logging
import mysql.connector
from mysql.connector import Error
from db_credentials import db_hostname, db_password, db_username

def create_server_connection(host_name=db_hostname, user_name=db_username,
                             user_password=db_password, db_name="books"):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        return connection
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as err:
        print(query)
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        table = []
        results = cursor.fetchall()
        for result in results:
            result = list(result)
            table.append(result)
        return table
    except Error as err:
        print(query)
        print(f"Error: '{err}'")


