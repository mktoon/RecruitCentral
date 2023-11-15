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
    return connection
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL Database: {e}")
    raise
