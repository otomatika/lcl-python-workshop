from flask import Flask, render_template
from mariadb.connections import Connection

import os
import mariadb
import sys
from dotenv import load_dotenv

load_dotenv("notebooks/.env")

app = Flask(__name__)

# Database configuration
db_config = {
    'user': os.environ["USER"],
    'password': os.environ["PW"],
    'host': os.environ["SERVER"],
    'database': os.environ["DB"]
}

# Initialize database connection
def get_db_connection():
    try:
        connection: Connection = mariadb.connect(
            user = os.environ["M_USER"],
            password = os.environ["M_PW"],
            host = os.environ["M_SERVER"],
            database = os.environ["M_DB"]
        )
        return connection
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

@app.route('/')
def home():
    return 'Welcome to LCL Logistics Dashboard!'

@app.route('/trucks')
def trucks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT truck_id, license_plate, model, capacity_ton, maintenance_date FROM trucks')
    trucks_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('trucks-db.html', trucks=trucks_data)

if __name__ == '__main__':
    app.run(debug=True)