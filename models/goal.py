from database import sql_select

def all_goals(user_id):
    results = []
    query = """SELECT goals.id, goal, nudged_users.name, users.name 
            FROM goals 
            INNER JOIN users ON user_id = users.id 
            LEFT JOIN users AS nudged_users ON nudged_by = nudged_users.id
            WHERE user_id = %s 
            ORDER BY goal ASC"""
    results = sql_select(query, [user_id])
    goals = []
    for result in results:
        goals.append({
            "id": result[0],
            "name": result[3],
            "goal_content": result[1],
            "who_nudged": result[2]
        })
    return (goals)

