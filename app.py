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
        user_text = request.form["user_text"]
        save_submission(user_text)
        # redirect with a flag so we can show the message on the next GET
        return redirect(url_for("home", success="1"))

    # on GET, check for the flag
    success = request.args.get("success")
    return render_template("index.html", success=bool(success))

if __name__ == "__main__":
    # Run in debug mode on port 5000
    app.run(debug=True)
