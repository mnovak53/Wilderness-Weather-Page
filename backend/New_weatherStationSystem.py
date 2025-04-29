import random
import datetime
import json
import os

# File names
LOG_FILE = "weather_station_system_logs.txt"
SENSOR_LOG_FILE = "sensor_health_logs.txt"
UPTIME_FILE = "sensor_uptime.json"

# Logging functions
def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

def log_sensor_alert(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(SENSOR_LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} {message}\n")

# Park data
PARKS = {
    "Yellowstone National Park": (44.4280, -110.5885), 
    "Yosemite National Park": (37.8651, -119.5383),  
    "Grand Canyon National Park": (36.1069, -112.1129),  
    "Great Smoky Mountains National Park": (35.6532, -83.4685),  
    "Zion National Park": (37.2982, -113.0263), 
    "Acadia National Park": (44.3386, -68.2733),  
    "Everglades National Park": (25.2866, -80.8987),  
    "Rocky Mountain National Park": (40.3428, -105.6836), 
}

# Uptime tracking
def load_uptime_data():
    if os.path.exists(UPTIME_FILE):
        with open(UPTIME_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_uptime_data(data):
    with open(UPTIME_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Calculate fake risk level score
def calculate_risk_score(temp, humidity, pressure):
    score = 0
    if temp > 38 or temp < -10:
        score += 3
    if humidity > 90 or humidity < 20:
        score += 2
    if pressure < 1000 or pressure > 1035:
        score += 2
    return min(score, 10)

# Generate weather data
def generate_random_weather_data(place, lat, lon, timestamp, uptime_tracker):
    if place not in uptime_tracker:
        uptime_tracker[place] = {"success": 0, "fail": 0}

    if random.random() < 0.01:
        uptime_tracker[place]["fail"] += 1
        log_message(f"Sensor failure at {place}!")
        return None

    uptime_tracker[place]["success"] += 1

    if place in ["Yellowstone National Park", "Yosemite National Park", "Great Smoky Mountains National Park", "Rocky Mountain National Park"]:
        temperature = random.uniform(-10, 25)
        humidity = random.randint(40, 80)
        pressure = random.randint(1000, 1030)
    elif place in ["Grand Canyon National Park", "Zion National Park"]:
        temperature = random.uniform(20, 40)
        humidity = random.randint(10, 30)
        pressure = random.randint(1005, 1015)
    elif place == "Acadia National Park":
        temperature = random.uniform(10, 20)
        humidity = random.randint(60, 80)
        pressure = random.randint(1010, 1020)
    elif place == "Everglades National Park":
        temperature = random.uniform(25, 35)
        humidity = random.randint(70, 95)
        pressure = random.randint(1005, 1010)

    risk = calculate_risk_score(temperature, humidity, pressure)
    if risk >= 7:
        log_message(f"RED ALERT: High risk weather score of {risk} at {place}!")

    data = {
        "place": place,
        "latitude": lat,
        "longitude": lon,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "risk_level": risk
    }

    return data

# Generate fake alerts
def generate_sensor_health_alerts():
    issues = [
        "Sensor #{num} down — freezing temperatures",
        "Sensor #{num} offline — wildlife damage suspected",
        "Sensor #{num} overheating — sustained high humidity",
        "Sensor #{num} intermittent signal — possible interference",
        "Sensor #{num} failure — battery depletion",
        "Sensor #{num} water damage detected",
        "Sensor #{num} data spike anomaly — needs calibration",
        "Sensor #{num} not responding — unknown error"
    ]

    for place in PARKS:
        if random.random() < 0.2:
            sensor_num = random.randint(1, 10)
            issue = random.choice(issues).format(num=sensor_num)
            log_sensor_alert(f"{place} {issue}")

# Main loop
def send_weather_data():
    # Clear current weather data file
    with open('wilderness_weather_data.json', 'w') as f:
        pass

    uptime_tracker = load_uptime_data()
    today = datetime.datetime.now()

    for day in range(7):  # 7 days
        timestamp = today - datetime.timedelta(days=day)
        for place, (lat, lon) in PARKS.items():
            # 10% chance the entire park's sensors are dead for the day
            if random.random() < 0.10:
                log_message(f" No weather data collected for {place} on {timestamp.strftime('%Y-%m-%d')} due to complete sensor failure.")
                if place not in uptime_tracker:
                    uptime_tracker[place] = {"success": 0, "fail": 0}
                uptime_tracker[place]["fail"] += 1  # counts as a full fail day
                continue

            # Otherwise, normal attempt to generate data
            data = generate_random_weather_data(place, lat, lon, timestamp, uptime_tracker)
            if data:
                with open('wilderness_weather_data.json', 'a') as f:
                    f.write(json.dumps(data) + "\n")
                log_message(f"{timestamp.strftime('%Y-%m-%d')}: {place} data sent.")
            else:
                log_message(f"{timestamp.strftime('%Y-%m-%d')}: Failed to collect data for {place} (individual sensor fail).")

    save_uptime_data(uptime_tracker)
    generate_sensor_health_alerts()
    log_message("1 week of weather data generated with realistic sensor gaps.\n")


if __name__ == "__main__":
    send_weather_data()
