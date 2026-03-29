from flask import Flask, request, jsonify
import mysql.connector
from jwt_utils import generate_token
import requests
app = Flask(__name__)

def send_log(service, level, message):
    try:
        requests.post("http://logs:5003/log", json={
            "service": service,
            "level": level,
            "message": message
        })
    except:
        pass

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="testdb"
    )
    cursor = conn.cursor()

    query = f"SELECT username, role FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    result = cursor.fetchone()

    if result:
        token = generate_token(result[0], result[1])
        send_log("AUTH", "INFO", f"Login attempt successful: {username}")
        return {"token": token}
    else:
        send_log("AUTH", "WARNING", f"Login attempt failed: {username}")

    return {"error": "Invalid credentials"}, 401

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="testdb"
    )
    cursor = conn.cursor()

    #  intentionally vulnerable (no sanitization)
    query = f"INSERT INTO users (username, password, role) VALUES ('{data['username']}', '{data['password']}', 'user')"

    cursor.execute(query)
    conn.commit()

    return {"message": "User created"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)