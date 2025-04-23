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
        # After saving, redirect back to GET so browser doesn’t re-submit if refreshed
        return redirect(url_for("home"))

    # For GET requests, just render the page
    return render_template("index.html")

def home():
    # You can return plain HTML directly:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Flask Simple Page</title>
    </head>
    <body>
      <h1>Hello from Flask!</h1>
      <p>This page is served by a Python web server.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    # Run in debug mode on port 5000
    app.run(debug=True)
