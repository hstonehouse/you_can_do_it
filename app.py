from flask import Flask, render_template, request, redirect, session
import os
import psycopg2
import bcrypt

DB_URL = os.environ.get("DATABASE_URL", "dbname=accountability_db")

app = Flask(__name__)

@app.route('/')
def index():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT 1', []) # Query to check that the DB connected
    conn.close()
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)