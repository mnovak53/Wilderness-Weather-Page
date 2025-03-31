from flask import Flask, jsonify
from flask_cors import CORS
from simulator import send_weather_data
from archiver import process_and_archive_data
import sqlite3
from flask import request

app = Flask(__name__)
CORS(app)
DB_NAME = "weather_archive.db"

@app.route("/api/fetch", methods=["POST"])
def fetch():
    send_weather_data()

    # Re-analyze the generated weather data to extract alerts
    alerts = []
    try:
        with open("wilderness_weather_data.json", "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    temp = entry["temperature"]
                    wind_speed = entry.get("wind_speed", random.randint(10, 35))  # simulate wind speed

                    if temp < -10:
                        alerts.append({
                            "place": entry["place"],
                            "message": f"⚠️ Extreme cold detected: {temp:.1f}°C",
                            "status": "REVIEW"
                        })
                    if wind_speed > 30:
                        alerts.append({
                            "place": entry["place"],
                            "message": "⚠️ Wind speed exceeds safe thresholds.",
                            "status": "REVIEW"
                        })
                except Exception:
                    continue
    except FileNotFoundError:
        pass  # If the data file doesn't exist yet

    return jsonify({
        "message": "Weather data generated.",
        "alerts": alerts
    })


@app.route("/api/archive", methods=["POST"])
def archive():
    try:
        print("🔄 /api/archive called")
        process_and_archive_data()
        print("✅ process_and_archive_data() finished")
        return jsonify({"message": "Weather data archived."})
    except Exception as e:
        print("Error in /api/archive:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/weather", methods=["GET"])
def get_weather():
    selected_place = request.args.get("place")  # use 'place' to match your DB column
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if selected_place and selected_place != "All":
        cursor.execute("""
            SELECT * FROM weather_data
            WHERE place = ?
            ORDER BY timestamp DESC
            LIMIT 5
        """, (selected_place,))
    else:
        cursor.execute("""
            SELECT * FROM weather_data
            ORDER BY timestamp DESC
            LIMIT 5
        """)

    rows = cursor.fetchall()
    conn.close()

    data = [
        {
            "id": row[0],
            "place": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "temperature": row[4],
            "humidity": row[5],
            "pressure": row[6],
            "timestamp": row[7],
        }
        for row in rows
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
