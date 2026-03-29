from flask import Flask
from jwt_utils import generate_token

app = Flask(__name__)

@app.route("/internal")
def internal():
    admin_token = generate_token("admin", "admin")

    return {
        "admin_token": admin_token,
        "windows_ip": "10.0.0.5",
        "credentials": "admin:Winter2026!"
    }

@app.route("/admin")
def admin():
    return {
        "db_password": "root123",
        "api_key": "super-secret-key"
    }
@app.route("/backup/internal-data")
def hidden():
    return {
        "admin_token": "...",
        "credentials": "admin:Winter2026!",
        "windows_ip": "10.0.0.5"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)