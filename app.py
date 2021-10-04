from flask import Flask, render_template, request, redirect, session
from database import sql_select, sql_write
import psycopg2
import bcrypt
import os

from models.goal import all_goals, one_goal
from models.friend import all_friends
from models.name import my_name

SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        goals = all_goals(user_id)
        empty = len(goals) == 0
        name = my_name(user_id)
        return render_template('base.html', user_id = user_id, goals = goals, name = name, empty = empty)
    if not user_id:
        no_user_id = True
        return render_template('base.html', no_user_id = no_user_id)

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
   
    user_details = sql_select("SELECT * FROM users WHERE email = (%s)", [email])
    if user_details:
        user_id = user_details[0][0]
        password_hash = user_details[0][3]
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if valid:
            session['user_id'] = user_id
            return redirect('/')
    
    invalid_user = True
    return render_template('login.html', invalid_user = invalid_user)

@app.route('/edit/<id>')
def edit_goal(id):
    user_id = session.get('user_id') # I also need this in order for the 'global' buttons to show up (add friend, log out)
    name = my_name(user_id)
    if not user_id:
        return redirect('/')
    goal = one_goal(id)
    return render_template('edit_goal.html', user_id = user_id, goal_id = id, goal = goal, name = name)

@app.route('/save_goal_edits', methods=['POST'])
def save_goal_edits():
    goal_content = request.form.get('goal_content')
    goal_id = request.form.get('goal_id')
    sql_write("UPDATE goals SET goal = %s, nudged_by = NULL WHERE id = %s", [goal_content, goal_id])
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
    name = my_name(user_id)
    invalid_email = False
    return render_template('add_friends.html', user_id = user_id, invalid_email = invalid_email, name = name)

@app.route('/add_friend_action', methods=['POST'])
def add_friend_action():
    user_id = session.get('user_id')
    name = my_name(user_id)
    friend_email = request.form.get('new_friend')
    friend_id_result = sql_select("SELECT id FROM users WHERE email LIKE %s", [friend_email])
    
    if not friend_id_result:
        user_id = session.get('user_id')
        invalid_email = True
        return render_template('/add_friends.html', invalid_email = invalid_email, user_id = user_id, name = name)
    else:
        friend_id = friend_id_result[0][0]
        if str(friend_id) == str(user_id):
            user_id = session.get('user_id')
            invalid_email = True
            return render_template('/add_friends.html', invalid_email = invalid_email, user_id = user_id, name = name)

        sql_write("INSERT INTO friendships (friend1_id, friend2_id) VALUES (%s, %s)", [user_id, friend_id])
        sql_write("INSERT INTO friendships (friend1_id, friend2_id) VALUES (%s, %s)", [friend_id, user_id])
        return redirect('/your_friends')
    

@app.route('/your_friends')
def your_friends():
    user_id = session.get('user_id')
    name = my_name(user_id)
    if not user_id:
        return redirect('/')
    else:
        friend_names = all_friends(user_id)
        return render_template('your_friends.html', friend_names = friend_names, user_id = user_id, name = name)

@app.route('/goals/<friend_id>/')
def show_friends_goals(friend_id):
    user_id = session.get('user_id')
    name = my_name(user_id)
    friend_name = my_name(friend_id)
    if not user_id:
        return redirect('/')
    if str(user_id) == friend_id: # You can't be friends with yourself and nudge your own goals
        return redirect('/')
    else:
        friend_goals = all_goals(friend_id)        
        return render_template('friend_goals.html', user_id = user_id, friend_goals = friend_goals, friend_id = friend_id, name = name, friend_name = friend_name)

@app.route('/goals/<friend_id>/<goal_id>/nudge', methods = ['POST'])
def nudge(friend_id, goal_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    else:
        sql_write("UPDATE goals SET nudged_by = %s WHERE id = %s", [user_id, goal_id])
    return redirect(f'/goals/{friend_id}/')

if __name__ == "__main__":
    app.run(debug=True)