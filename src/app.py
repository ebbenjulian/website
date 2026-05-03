from flask import Flask, render_template, request, redirect, url_for, session
from bcrypt import checkpw
from database import main

app = Flask(__name__)

# Change this to a long random secret in production
app.secret_key = "change-this-secret-key"


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", username=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success, user, db_error = main.fetch_one(
            "SELECT userid, username, password_hash FROM users WHERE username = ?",
            (username,)
        )

        if not success:
            error = "Database error."
        elif not user:
            error = "Invalid username or password."
        else:
            userid = user["userid"]
            db_username = user["username"]
            password_hash = user["password_hash"]

            if isinstance(password_hash, str):
                password_hash = password_hash.encode("utf-8")

            if checkpw(password.encode("utf-8"), password_hash):
                session["user_id"] = userid
                session["username"] = db_username
                return redirect(url_for("index"))
            else:
                error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)