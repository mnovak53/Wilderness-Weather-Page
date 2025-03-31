import random
import datetime
import json

LOG_FILE = "weather_station_system_logs.txt"

def log_message(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

# Wilderness parks in the USA and their approximate locations
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

# Simulate realistic random weather data
def generate_random_weather_data(place, lat, lon):
    if random.random() < 0.01:
        log_message(f"Sensor failure at {place}!")
        return None 

    if place in ["Yellowstone National Park", "Yosemite National Park", "Great Smoky Mountains National Park", "Rocky Mountain National Park"]:
        temperature = random.uniform(-15, 25)  
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

    data = {
        "place": place,
        "latitude": lat,
        "longitude": lon,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return data

def send_weather_data():
    alerts = []
    with open('wilderness_weather_data.json', 'w') as f: 
        pass 

    for place, (lat, lon) in PARKS.items():
        data = generate_random_weather_data(place, lat, lon)
        if data:
            with open('wilderness_weather_data.json', 'a', encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
            log_message(f"Today's weather data for {place} sent to data management system.")

            # Check for extreme conditions
            if data['temperature'] < -10:
                alerts.append({
                    "place": place,
                    "message": f"⚠️ Extreme cold detected: {data['temperature']:.1f}°C",
                    "status": "REVIEW"
                })
            elif data['temperature'] > 38:
                alerts.append({
                    "place": place,
                    "message": f"⚠️ Extreme heat detected: {data['temperature']:.1f}°C",
                    "status": "REVIEW"
                })

        else:
            log_message(f"Failed to collect valid data for {place} due to sensor failure.")

    log_message("\n")
    return alerts
