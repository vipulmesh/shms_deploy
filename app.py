# ===========================
# IMPORTS
# ===========================
from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

# ===========================
# FLASK APP INITIALIZATION
# ===========================
app = Flask(__name__)

# Simple CORS headers (no external dependency)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# ===========================
# DATABASE SETUP
# ===========================
DATABASE = 'database.db'

def init_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            village TEXT NOT NULL,
            diarrhea INTEGER NOT NULL,
            fever INTEGER NOT NULL,
            rainfall TEXT NOT NULL,
            risk TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized")

# ===========================
# RULE-BASED AI LOGIC
# ===========================
def calculate_risk(diarrhea, rainfall):
    if diarrhea > 10 and rainfall == 'High':
        return 'High Risk'
    elif 5 <= diarrhea <= 10:
        return 'Medium Risk'
    else:
        return 'Safe'

# ===========================
# HTML ROUTES
# ===========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<page>")
def pages(page):
    """
    Example:
    /about   -> about.html
    /contact -> contact.html
    """
    return render_template(f"{page}.html")

# ===========================
# API ENDPOINTS
# ===========================
@app.route("/submit", methods=["POST", "OPTIONS"])
def submit_data():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()

        village = data.get("village")
        diarrhea = int(data.get("diarrhea"))
        fever = int(data.get("fever"))
        rainfall = data.get("rainfall")

        risk = calculate_risk(diarrhea, rainfall)
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO health_data
            (village, diarrhea, fever, rainfall, risk, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (village, diarrhea, fever, rainfall, risk, date))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Data submitted successfully",
            "risk": risk
        }), 201

    except Exception as e:
        print("Submit Error:", e)
        return jsonify({
            "success": False,
            "message": "Error submitting data"
        }), 500

@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM health_data ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        data = []
        for r in rows:
            data.append({
                "id": r[0],
                "village": r[1],
                "diarrhea": r[2],
                "fever": r[3],
                "rainfall": r[4],
                "risk": r[5],
                "date": r[6]
            })

        return jsonify(data), 200

    except Exception as e:
        print("Fetch Error:", e)
        return jsonify([]), 500

# ===========================
# APP START
# ===========================
if __name__ == "__main__":
    init_database()
    app.run()
