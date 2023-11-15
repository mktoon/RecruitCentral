# registration.py
import mysql.connector
from db_utils import establish_database_connection

def create_student_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_athletes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            sport VARCHAR(255),
            times VARCHAR(255),
            eligibility_status VARCHAR(255),
            bio TEXT
        )
    """)

def register_student(username, password, sport, times, eligibility_status, bio):
    conn = establish_database_connection()
    cursor = conn.cursor()

    create_student_table(cursor)  # Ensure the table exists

    try:
        cursor.execute("""
            INSERT INTO student_athletes (username, password, sport, times, eligibility_status, bio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password, sport, times, eligibility_status, bio))
        conn.commit()
        print("Student registration successful!")
        return 'success'
    except mysql.connector.IntegrityError:
        print("Username already exists. Please choose a different username.")
        return 'failure'
    except Exception as e:
        print(f"Error during student registration: {e}")
        return 'failure'
    finally:
        cursor.close()
        conn.close()

def create_coach_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coaches (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            specialization VARCHAR(255)
        )
    """)

def create_coach_account(username, password, specialization):
    conn = establish_database_connection()
    cursor = conn.cursor()

    create_coach_table(cursor)  # Ensure the table exists

    try:
        cursor.execute("""
            INSERT INTO coaches (username, password, specialization)
            VALUES (%s, %s, %s)
        """, (username, password, specialization))
        conn.commit()
        print("Coach registration successful!")
        return 'success'
    except mysql.connector.IntegrityError:
        print("Username already exists. Please choose a different username.")
        return 'failure'
    except Exception as e:
        print(f"Error during coach registration: {e}")
        return 'failure'
    finally:
        cursor.close()
        conn.close()

def get_user_data(username):
    conn = establish_database_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to get results as dictionaries

    try:
        cursor.execute("""
            SELECT * FROM student_athletes WHERE username = %s
        """, (username,))
        
        user_data = cursor.fetchone()  # Fetch one row as a dictionary

        if user_data:
            return user_data
        else:
            return None  # User not found

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        cursor.close()
        conn.close()
