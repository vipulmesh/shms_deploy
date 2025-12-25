from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Mock database for presentation (Persistent storage requires Supabase/PostgreSQL)
mock_db = [
    {"id": 1, "village": "Greenfield", "diarrhea": 12, "fever": 5, "rainfall": "High", "risk": "High Risk", "date": "2023-12-20"},
    {"id": 2, "village": "Riverside", "diarrhea": 3, "fever": 2, "rainfall": "Low", "risk": "Safe", "date": "2023-12-21"}
]

def calculate_risk(diarrhea, rainfall):
    if diarrhea > 10 and rainfall == 'High': return 'High Risk'
    elif 5 <= diarrhea <= 10: return 'Medium Risk'
    else: return 'Safe'

@app.route("/")
def home(): return render_template("index.html")

@app.route("/login")
def login_p(): return render_template("login.html")

@app.route("/data-entry")
def entry_p(): return render_template("data-entry.html")

@app.route("/dashboard")
def dash_p(): return render_template("dashboard.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(mock_db)

@app.route("/api/submit", methods=["POST"])
def submit_data():
    try:
        data = request.get_json()
        diarrhea = int(data.get("diarrhea"))
        rainfall = data.get("rainfall")
        risk = calculate_risk(diarrhea, rainfall)
        
        new_entry = {
            "id": len(mock_db) + 1,
            "village": data.get("village"),
            "diarrhea": diarrhea,
            "fever": data.get("fever"),
            "rainfall": rainfall,
            "risk": risk,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        mock_db.insert(0, new_entry) 
        return jsonify({"success": True, "risk": risk}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500