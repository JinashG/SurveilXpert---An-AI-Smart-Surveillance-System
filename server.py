from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["SurveilXpertDB"]
alerts_collection = db["alerts"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/fire', methods=['POST'])
def fire_alert():
    data = request.json
    print(f"Received Alert: {data}")

    alert_data = {
        "type": "fire",
        "anomaly": data.get("message"),
        "timestamp": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")  # Format: Tue, 18 Feb 2025 21:06:20 GMT
    }

    # Store in MongoDB
    result = alerts_collection.insert_one(alert_data)
    
    # Create a copy without _id for emitting
    emit_data = alert_data.copy()
    
    # Emit to frontend
    socketio.emit('new_alert', json.dumps(emit_data))  # Explicit JSON serialization

    return jsonify({"status": "success", "message": "Alert received!"}), 200

@app.route('/alerts')
def get_alerts():
    alerts = list(alerts_collection.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(alerts)

@app.route('/delete')
def delete_alerts():
    alerts_collection.delete_many({})
    return jsonify({"status": "success", "message": "All alerts deleted!"})

def send_alert(alert):
    socketio.emit('new_alert', json.dumps(alert))

# Run the Flask app
if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
