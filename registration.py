import mysql.connector

# Prompt the user for their role (athlete or coach)
user_role = input("Are you a student athlete or a coach? ")

if user_role.lower() == "athlete":
    # Code for student athlete functionality
    register_student()
elif user_role.lower() == "coach":
    # Code for coach functionality
    coach_login()
else:
    print("Invalid input. Please select either 'athlete' or 'coach'.")

def register_student():
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    cursor = conn.cursor()

    # Create the students table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            sport VARCHAR(255),
            times VARCHAR(255),
            bio TEXT
        )
    """)
    conn.commit()

    print("Student Registration")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    sport = input("Enter the sport: ")
    times = input("Enter the times: ")
    #eligibility_status = input("Enter the eligibility status: ")
    bio = input("Enter the bio: ")

    try:
        # Insert student details into the database
        cursor.execute("""
            INSERT INTO students (username, password, sport, times, eligibility_status, bio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password, sport, times,  bio))
        conn.commit()
        print("Registration successful!")
    except mysql.connector.IntegrityError:
        print("Username already exists. Please choose a different username.")

    # Close the database connection
    conn.close()

def coach_login():
    print("Coach Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    cursor = conn.cursor()

    # Check if the provided username and password match a coach record
    cursor.execute("""
        SELECT * FROM coaches WHERE username = %s AND password = %s
    """, (username, password))

    coach = cursor.fetchone()

    if coach is None:
        print("Invalid username or password.")
        create_coach_account()
    else:
        print("Login successful!")
        # Retrieve student account details associated with the coach from the database
        cursor.execute("""
            SELECT * FROM students WHERE coach_id = %s
        """, (coach[0],))  # Assuming the coach_id is stored in the first column (index 0) of the coaches table

        students = cursor.fetchall()

        if not students:
            print("No students associated with this coach.")
        else:
            print("Students:")
            for student in students:
                print(f"ID: {student[0]}, Username: {student[1]}, Sport: {student[3]}, Times: {student[4]}, Eligibility Status: {student[5]}, Bio: {student[6]}")

    # Close the database connection
    conn.close()

def create_coach_account():
    print("Coach Account Creation")
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    cursor = conn.cursor()

    try:
        # Insert coach details into the database
        cursor.execute("""
            INSERT INTO coaches (username, password)
            VALUES (%s, %s)
        """, (username, password))
        conn.commit()
        print("Coach account created successfully!")
    except mysql.connector.IntegrityError:
        print("Username already exists. Please choose a different username.")

    # Close the database connection
    conn.close()
