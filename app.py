from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("feedback.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        rating INTEGER,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():

    name=request.form["name"]
    email=request.form["email"]
    rating=request.form["rating"]
    message=request.form["message"]

    conn=sqlite3.connect("feedback.db")
    cur=conn.cursor()

    cur.execute(
        "INSERT INTO feedback(name,email,rating,message) VALUES(?,?,?,?)",
        (name,email,rating,message)
    )

    conn.commit()
    conn.close()

    return "Feedback Submitted Successfully"

if __name__=="__main__":
    app.run(debug=True)