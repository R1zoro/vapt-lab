from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def log_to_db(service, level, message):
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="testdb"
    )
    cursor = conn.cursor()

    query = "INSERT INTO logs (service_name, log_level, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (service, level, message))

    conn.commit()
    conn.close()

@app.route("/log", methods=["POST"])
def log():
    data = request.json

    service = data.get("service")
    level = data.get("level")
    message = data.get("message")

    log_to_db(service, level, message)

    return {"status": "logged"}

@app.route("/logs", methods=["GET"])
def get_logs():
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="testdb"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50")
    results = cursor.fetchall()

    return {"logs": results}

@app.route("/logs/<service>", methods=["GET"])
def logs_by_service(service):
    conn = mysql.connector.connect(...)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM logs WHERE service_name=%s ORDER BY timestamp DESC",
        (service,)
    )

    return {"logs": cursor.fetchall()}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)