import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Render provides DATABASE_URL when you connect this service to PostgreSQL.
# If DATABASE_URL is not set, the app uses SQLite locally.
DATABASE_URL = os.environ.get("DATABASE_URL")
SQLITE_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.db")


def get_connection():
    """Return a database connection for PostgreSQL on Render or SQLite locally."""
    if DATABASE_URL:
        import psycopg

        # Render normally provides a postgres:// or postgresql:// URL.
        # psycopg 3 accepts PostgreSQL connection URLs.
        return psycopg.connect(DATABASE_URL.replace("postgres://", "postgresql://", 1))

    return sqlite3.connect(SQLITE_DB)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL
        )
    """) if DATABASE_URL else cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    rating = request.form.get("rating", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not rating or not message:
        return "Please fill in all feedback fields.", 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return "Rating must be between 1 and 5.", 400
    except ValueError:
        return "Invalid rating.", 400

    conn = get_connection()
    cur = conn.cursor()

    if DATABASE_URL:
        cur.execute(
            "INSERT INTO feedback (name, email, rating, message) VALUES (%s, %s, %s, %s)",
            (name, email, rating, message),
        )
    else:
        cur.execute(
            "INSERT INTO feedback (name, email, rating, message) VALUES (?, ?, ?, ?)",
            (name, email, rating, message),
        )

    conn.commit()
    cur.close()
    conn.close()

    return "Feedback Submitted Successfully"


if __name__ == "__main__":
    app.run(debug=True)
