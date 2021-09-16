from database import sql_select

def my_name(user_id):
    name = sql_select("Select name FROM users WHERE id = %s", [user_id])[0][0]
    return name