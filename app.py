import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS submissions ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "text TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()

# Initialize DB when the app starts
init_db()

def save_submission(text):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO submissions (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        address = request.form["address"]
        save_submission(address)
        return redirect(url_for("home", success="1"))

    success = bool(request.args.get("success"))
    return render_template("index.html", success=success)

if __name__ == "__main__":
    app.run(debug=True)
