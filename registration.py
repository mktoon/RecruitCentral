# registration.py
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
        print("Registration successful!")
        return 'success'
    except Exception as e:
        print(f"Error during registration: {e}")
        return 'failure'
    finally:
        cursor.close()
        conn.close()
