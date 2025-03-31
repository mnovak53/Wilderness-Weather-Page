import sqlite3
import json
import os

DB_NAME = "weather_archive.db"
LOG_FILE = "data_management_system_logs.txt"

def log_message(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    print(message)

# Function to store weather data in the database
def store_weather_data(cursor, conn, data):
    print(f"📦 Storing {data['place']} @ {data['timestamp']}")  
    cursor.execute("""
    SELECT * FROM weather_data WHERE place=? AND timestamp=?
    """, (data['place'], data['timestamp']))
    
    if cursor.fetchone() is None: 
        cursor.execute("""
        INSERT INTO weather_data (place, latitude, longitude, temperature, humidity, pressure, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['place'], data['latitude'], data['longitude'], data['temperature'], data['humidity'], data['pressure'], data['timestamp']))
        conn.commit()
        log_message(f"Archived today's weather data for {data['place']}.")
    else:
        log_message(f"Data for {data['place']} at {data['timestamp']} already exists. Skipping.")

# Function to print archived data
def print_archived_data(cursor):
    cursor.execute("SELECT * FROM weather_data")
    records = cursor.fetchall()
    if records:
        log_message("\nArchived Weather Data:")
        for record in records:
            log_message(str(record))
    else:
        log_message("No weather data has been archived yet.")

def process_and_archive_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place TEXT,
        latitude REAL,
        longitude REAL,
        temperature REAL,
        humidity INTEGER,
        pressure INTEGER,
        timestamp TEXT
    )
    """)
    conn.commit()

    input_file = 'wilderness_weather_data.json'
    archived_file = 'wilderness_weather_data_old.json'

    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(input_file, 'w') as f: 
        pass

    with open(archived_file, 'a') as archive:
        for line in lines:
            try:
                data = json.loads(line)
                if all(key in data for key in ['place', 'latitude', 'longitude', 'temperature', 'humidity', 'pressure', 'timestamp']):
                    store_weather_data(cursor, conn, data)
                    archive.write(line)  
                else:
                    log_message(f"Warning: Incomplete data for {data.get('place', 'Unknown place')}. Skipping this entry.")
            except json.JSONDecodeError as e:
                log_message(f"Error decoding JSON data: {e}. Skipping this entry.")

    #print all archived data to logs
    print_archived_data(cursor)

    conn.close()
