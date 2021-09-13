from database import sql_select

def all_friends(user_id):
    friends = sql_select("SELECT id, name FROM friendships LEFT JOIN users ON friend2_id = id WHERE friend1_id = %s", [user_id])
    friend_names = []
    for item in friends:
        friend_names.append({
            "id": item[0],
            "name": item[1]
            })
    return friend_names






