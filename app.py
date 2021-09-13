from flask import Flask, render_template, request, redirect, session
from database import sql_select, sql_write
import os
import psycopg2
import bcrypt
import requests

from models.goal import all_goals
from models.friend import all_friends

DB_URL = os.environ.get("DATABASE_URL", "dbname=accountability_db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'String for testing purposes'

@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        goals = all_goals(user_id)
        return render_template('base.html', user_id = user_id, goals = goals)
    else:
        return render_template('base.html')

@app.route('/signup')
def signup():
    user_id = session.get('user_id')
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

@app.route('/log_out')
def log_out():
    del session['user_id']
    return redirect('/')

@app.route('/log_in')
def log_in():
    user_id = session.get('user_id')
    if not user_id:
        return render_template('login.html', user_id = user_id)
    else:
        return redirect('/')

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

@app.route('/edit/<id>')
def edit_goal(id):
    user_id = session.get('user_id') # I also need this in order for the 'global' buttons to show up (add friend, log out)
    if not user_id:
        return redirect('/')
    results = sql_select("SELECT goal, nudged_by from goals WHERE id = (%s)", [id])
    goal_content, nudged_by = results[0] # results returns a LIST of tuples so you need to manually select the first one
    return render_template('edit_goal.html', user_id = user_id, goal_id = id, goal_content = goal_content, nudged_by = nudged_by)

@app.route('/save_goal_edits', methods=['POST'])
def save_goal_edits():
    goal_content = request.form.get('goal_content')
    goal_id = request.form.get('goal_id')
    sql_write("UPDATE goals SET goal = %s WHERE id = %s", [goal_content, goal_id])
    return redirect('/')

@app.route('/delete_nudge/<id>', methods=['POST'])
def delete_nudge(id):
    user_id = session.get('user_id') 
    if not user_id:
        return redirect('/')
    sql_write("UPDATE goals SET nudged_by = NULL WHERE id = %s", [id])
    return redirect('/')

@app.route('/delete_goal/<id>', methods=['POST'])
def delete_goal(id):
    user_id = session.get('user_id') 
    if not user_id:
        return redirect('/')
    sql_write("DELETE FROM goals WHERE id = %s", [id])
    return redirect('/')

@app.route('/add_goal_action', methods=['POST'])
def add_new_goal():
    user_id = session.get('user_id')
    goal_content = request.form.get('newgoal')
    sql_write("INSERT INTO goals (user_id, goal) VALUES (%s, %s)", [user_id, goal_content])
    return redirect('/')

@app.route('/add_friends')
def add_friend_page():
    user_id = session.get('user_id')
    invalid_email = False
    return render_template('add_friends.html', user_id = user_id, invalid_email = invalid_email)

@app.route('/add_friend_action', methods=['POST'])
def add_friend_action():
    user_id = session.get('user_id')
    friend_email = request.form.get('new_friend')
    friend_id = sql_select("SELECT id FROM users WHERE email LIKE %s", [friend_email])[0]
    if friend_id and user_id:
        sql_write("INSERT INTO friendships (friend1_id, friend2_id) VALUES (%s, %s)", [user_id, friend_id])
        sql_write("INSERT INTO friendships (friend1_id, friend2_id) VALUES (%s, %s)", [friend_id, user_id])
        return redirect('/')
    else:
        user_id = session.get('user_id')
        invalid_email = True
        return render_template('/add_friends.html', invalid_email = invalid_email, user_id = user_id)

@app.route('/your_friends')
def your_friends():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    else:
        friend_names = all_friends(user_id)
        return render_template('your_friends.html', friend_names = friend_names, user_id = user_id)

@app.route('/goals/<friend_id>/')
def show_friends_goals(friend_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    if str(user_id) == friend_id: # You can't be friends with yourself and nudge your own goals
        return redirect('/')
    else:
        friend_goals = all_goals(friend_id)        
        return render_template('friend_goals.html', user_id = user_id, friend_goals = friend_goals)

if __name__ == "__main__":
    app.run(debug=True)