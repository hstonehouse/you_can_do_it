from database import sql_select

def all_goals(user_id):
    results = []
    results = sql_select("SELECT goals.id, user_id, goal, nudged_by, name FROM goals INNER JOIN users ON user_id = users.id WHERE user_id = %s", [user_id])
    goals = []
    for result in results:
        goals.append({
            "id": result[0],
            "name": result[4],
            "goal_content": result[2],
            "who_nudged": result[3]
        })
    return (goals)

