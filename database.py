import psycopg2

def sql_select(query, params):
  conn = psycopg2.connect("dbname=accountability_db")
  cur = conn.cursor()
  cur.execute(query, params)
  results = cur.fetchall()
  cur.close()
  conn.close()
  return results

def sql_write(query, params):
  conn = psycopg2.connect("dbname=accountability_db")
  cur = conn.cursor()
  cur.execute(query, params)
  conn.commit()
  conn.close()