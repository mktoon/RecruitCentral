# db_utils.py
import mysql.connector
# Establish a connection to the MySQL database
def establish_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sesat@26535102020",
        database="recruitcentral"
    )
