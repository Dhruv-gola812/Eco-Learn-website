from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = "secretkey"   # apna strong secret key use karna

# ✅ MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@12345",
        database="hackathon"
    )

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ✅ User Login
@app.route("/dologin", methods=["POST"])
def login():
    username = request.form.get["username"]
    password = request.form.get["password"]

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        session["user"] = username
        return redirect("/")
    else:
        return "Invalid credentials, try again!"

# ✅ Quiz Questions (API)
@app.route("/quiz")
def quiz():
    questions = [
        {
            "question": "Which gas is responsible for global warming?",
            "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
            "answer": "Carbon Dioxide"
        },
        {
            "question": "Which is a renewable energy source?",
            "options": ["Coal", "Oil", "Solar", "Natural Gas"],
            "answer": "Solar"
        },
        {
            "question": "Which animal is most affected by melting ice?",
            "options": ["Lion", "Elephant", "Polar Bear", "Tiger"],
            "answer": "Polar Bear"
        }
    ]
    return jsonify(questions)

# ✅ Submit Score
@app.route("/submit_score", methods=["POST"])
def submit_score():
    if "user" not in session:
        return "Login required!"

    data = request.get_json()
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO score (username, score) VALUES (%s, %s)", (session["user"], data["score"]))
    db.commit()
    cursor.close()
    db.close()
    return "Score submitted!"

# ✅ Leaderboard (API)
@app.route("/leaderboard")
def leaderboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT username, score FROM score ORDER BY score DESC LIMIT 10")
    scores = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(scores)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
