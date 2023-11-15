# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from db_utils import establish_database_connection
from registration import register_student, coach_login, create_coach_account
import logging  # Added import for logging
from flask import request
from flask import redirect

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# this is the login function that will be used to check if the user is in the database
def login_function(username, password):
    with establish_database_connection() as conn:
        cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT * FROM student_athletes WHERE username = %s AND password = %s
        """, (username, password))

        user = cursor.fetchone()

        if user:
            # Successful login
            return 'success'
        else:
            # Invalid credentials
            return 'failure'
    except Exception as e:
        logging.error(f"Error during login: {e}")  # Using logging instead of print
        return 'failure'
    finally:
        cursor.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        sports = request.form.getlist('sports')  # Use getlist to get multiple selected sports
        times = request.form['times']
        eligibility_status = request.form['eligibility_status']
        bio = request.form['bio']

        try:
            if role == 'student':
                reg_result = register_student(username, password, sports, times, eligibility_status, bio)
            elif role == 'coach':
                reg_result = create_coach_account(username, password, sports[0])  # Assuming sports[0] is a specialization for a coach

            if reg_result == 'success':
                # Redirect to the login page after successful registration
                return redirect(url_for('login'))
            else:
                # Print registration failure reason
                print(f"Registration failed: {reg_result}")

        except Exception as e:
            # Print any exception that occurred during registration
            print(f"Exception during registration: {e}")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = login_function(username, password)

        if result == 'success':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect to the login page or home page
    return redirect(url_for('login'))  # Update 'login' with your actual login route

@app.route('/update_description', methods=['GET', 'POST'])
def update_description():
    if 'username' in session:
        if request.method == 'POST':
            # Retrieve the description from the form
            description = request.form['description']

            # Call a function to update the description in the database
            update_description_function(session['username'], description)

            # Redirect to the dashboard or another appropriate page
            return redirect(url_for('dashboard'))

        # Render the form for updating description
        return render_template('update_description.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
