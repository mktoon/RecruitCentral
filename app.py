# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from db_utils import establish_database_connection
from registration import register_student, coach_login, create_coach_account

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

def login_function(username, password):
    # Implement your login logic here
    # Return 'success' if login is successful, otherwise return 'failure'
    pass
# this is the login function that will be used to check if the user is in the database
def login_function(username, password):
    conn = establish_database_connection()
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
        print(f"Error during login: {e}")
        return 'failure'
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sport = request.form['sport']
        times = request.form['times']
        eligibility_status = request.form['eligibility_status']
        bio = request.form['bio']

        reg_result = register_student(username, password, sport, times, eligibility_status, bio)

        if reg_result == 'success':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('register.html', error='Registration failed')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
