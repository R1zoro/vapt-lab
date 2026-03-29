from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"
# Home
@app.route("/")
def home():
    return render_template("index.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = {
        "username": request.form["username"],
        "password": request.form["password"]
    }

    res = requests.post("http://auth:5001/login", json=data).json()

    if "token" in res:
        session["user"] = data["username"]
        session["token"] = res["token"]
        return redirect("/discover")

    return "Login Failed"

# Signup page (
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    data = {
        "username": request.form["username"],
        "password": request.form["password"]
    }

    requests.post("http://auth:5001/signup", json=data)

    return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Discover page
@app.route("/discover")
def discover():
    if "user" not in session:
        return redirect("/login")

    return render_template("discover.html", user=session["user"], results=[])

# Profile (static for now)
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    return render_template("profile.html", user=session["user"])

@app.route("/search")
def search():
    if "user" not in session:
        return redirect("/login")

    name = request.args.get("name")
    res = requests.get(f"http://api:5000/users?name={name}").json()

    return render_template("discover.html", results=res["data"])

# Admin (connected to API)
@app.route("/admin")
def admin():
    if "token" not in session:
        return redirect("/login")

    res = requests.get(
        "http://api:5000/admin",
        headers={"Authorization": session["token"]}
    )

    return res.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)