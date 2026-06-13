from flask import Flask
import mysql.connector
import time

app = Flask(__name__)

def get_connection():

    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password="root123",
                database="mydb"
            )
            return conn

        except:
            time.sleep(2)

    return None


@app.route("/")
def home():
    return "Flask + MySQL Running"


@app.route("/create")
def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100)
    )
    """)

    conn.commit()

    return "Table Created"


@app.route("/add/<name>")
def add_user(name):

    conn = get_connection()

    cursor = conn.cursor()

    sql = "INSERT INTO users(name) VALUES(%s)"

    cursor.execute(sql, (name,))

    conn.commit()

    return f"{name} Added"


@app.route("/users")
def users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    return str(data)


app.run(host="0.0.0.0", port=5000)