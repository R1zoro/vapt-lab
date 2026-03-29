from flask import Flask, request
import requests
import mysql.connector
import re
from urllib.parse import urlparse

from jwt_utils import verify_token

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

BLOCKED_KEYWORDS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "internal",
    "metadata",
    "169.254.169.254"
]

BLOCKED_PROTOCOLS = [
    "file://",
    "gopher://",
    "dict://",
    "ftp://"
]


@app.route("/")
def home():
    return "API Running"

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    send_log("API", "INFO", f"Fetch request to {url} from {request.remote_addr}")
    if not url:
        return "Missing URL", 400

    parsed = urlparse(url)
    url_lower = url.lower()

    # Block protocols
    if parsed.scheme + "://" in BLOCKED_PROTOCOLS:
        send_log("API", "WARNING", f"WAF blocked request: {url}")
        return "Blocked by WAF (protocol)", 403

    # Block keywords
    for keyword in BLOCKED_KEYWORDS:
        if keyword in url_lower:
            send_log("API", "WARNING", f"WAF blocked request: {url}")
            return "Blocked by WAF (keyword)", 403

    # Block private IPs


    try:
        response = requests.get(url)

        # SUCCESS LOG HERE
        send_log("API", "INFO", f"Successful fetch to {url} | Status: {response.status_code}")

        return response.text

    except Exception as e:
        send_log("API", "ERROR", f"Fetch failed: {url} | Error: {str(e)}")
        return str(e), 500

@app.route("/users")
def get_users():
    name = request.args.get("name")
    send_log("API", "INFO", f"User search: {name}")

    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="testdb"
    )
    cursor = conn.cursor()

    # VULNERABLE QUERY
    query = f"SELECT * FROM users WHERE username = '{name}'"
    cursor.execute(query)

    results = cursor.fetchall()
    return {"data": results}

@app.route("/admin")
def admin():
    token = request.headers.get("Authorization")
    if not token:
        return "Missing token", 403

    data = verify_token(token)

    if not data:
        return "Invalid token", 403

    if data.get("role") != "admin":
        return "Unauthorized", 403

    send_log("API", "WARNING", "Unauthorized admin access attempt")
    return {"secret": "Admin panel access granted"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)