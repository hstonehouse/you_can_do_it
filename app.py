from flask import Flask, render_template, request, redirect, session
from database import sql_select, sql_write
import os
import psycopg2
import bcrypt

DB_URL = os.environ.get("DATABASE_URL", "dbname=accountability_db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'String for testing purposes'

@app.route('/')
def index():
    user_id = session.get('user_id')
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT 1', []) # Query to check that the DB connected
    conn.close()
    return render_template('base.html', user_id = user_id)

@app.route('/log_in')
def log_in():
    return render_template('login.html')

@app.route('/log_in_action', methods=['POST'])
def log_in_action(): 
    email = request.form.get('email')
    password = request.form.get('password')

    conn = psycopg2.connect("dbname=accountability_db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = (%s)", [email])
    user_details = cur.fetchall()
    if user_details:
        user_id = user_details[0][0]
        password_hash = user_details[0][3]
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if valid:
            session['user_id'] = user_id
            conn.close()
            return redirect('/')
        else:
            invalid_user = True
            return render_template('base.html', invalid_user = invalid_user)

@app.route('/signup')
def signup():
    user_id = session.get('user_user_')
    if user_id:
         return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/signup_action', methods=['POST'])
def signup_action():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password == confirm_password:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        sql_write("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)", [email, name, password_hash])
        return redirect('/log_in')
    else:
        mismatch = True
        return render_template('signup.html', mismatch = mismatch)

if __name__ == "__main__":
    app.run(debug=True)