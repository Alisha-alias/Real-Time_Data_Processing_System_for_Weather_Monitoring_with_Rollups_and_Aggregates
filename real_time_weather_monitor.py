import requests
import sqlite3
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# API Key for OpenWeatherMap
api_key = "a6de4c52324b3dbe6de575a72411fb5e"  # Replace with your actual API key

# List of cities to track weather for
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Thresholds (You can make these configurable)
TEMP_THRESHOLD = 35  # Alert if temp exceeds 35°C for two consecutive updates

# Email Configurations
EMAIL_ADDRESS = "your_email@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "your_password"        # Replace with your email password
RECEIVER_EMAIL = "receiver_email@gmail.com"  # Replace with receiver's email

# Create or connect to SQLite database
def create_database():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Table for raw weather data
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
        city TEXT,
        temp REAL,
        feels_like REAL,
        condition TEXT,
        timestamp INTEGER
    )''')

    # Table for daily aggregates
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_weather (
        city TEXT,
        date TEXT,
        avg_temp REAL,
        max_temp REAL,
        min_temp REAL,
        dominant_condition TEXT
    )''')

    # Table for alert tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
        city TEXT,
        alert_message TEXT,
        timestamp INTEGER
    )''')

    conn.commit()
    conn.close()

# Fetch weather data for a specific city
def get_weather_data(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'condition': data['weather'][0]['main'],
            'time': data['dt']
        }

        # Print the retrieved data for each city
        print(f"City: {city_name}, Temp: {weather_data['temp']}°C, Feels Like: {weather_data['feels_like']}°C, Condition: {weather_data['condition']}, Time: {datetime.utcfromtimestamp(weather_data['time']).strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        return weather_data
    else:
        print(f"Failed to fetch weather data for {city_name}.")
        return None

# Send email alert
def send_email_alert(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email alert sent to {RECEIVER_EMAIL}.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

# Store weather data in the database
def store_weather_data(city, weather_data):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO weather (city, temp, feels_like, condition, timestamp)
    VALUES (?, ?, ?, ?, ?)''', (city, weather_data['temp'], weather_data['feels_like'], weather_data['condition'], weather_data['time']))

    conn.commit()
    conn.close()

# Calculate daily rollups (averages and dominant condition) every 5 minutes
def calculate_daily_rollups():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Clear the daily_weather table
    cursor.execute('DELETE FROM daily_weather')

    for city in CITIES:
        # Group weather data by city for the current date
        cursor.execute('''
        SELECT 
            AVG(temp) as avg_temp, 
            MAX(temp) as max_temp, 
            MIN(temp) as min_temp,
            condition
        FROM weather
        WHERE city = ? AND date(datetime(timestamp, 'unixepoch')) = date('now')
        GROUP BY condition
        ''', (city,))
        
        results = cursor.fetchall()
        
        # If no results, continue to next city
        if not results:
            continue
        
        # For each date, determine dominant weather condition and aggregate temperatures
        daily_conditions = {'avg_temp': 0, 'max_temp': float('-inf'), 'min_temp': float('inf'), 'conditions': {}}
        for row in results:
            avg_temp, max_temp, min_temp, condition = row
            
            daily_conditions['avg_temp'] += avg_temp
            daily_conditions['max_temp'] = max(daily_conditions['max_temp'], max_temp)
            daily_conditions['min_temp'] = min(daily_conditions['min_temp'], min_temp)

            # Count condition occurrences
            if condition not in daily_conditions['conditions']:
                daily_conditions['conditions'][condition] = 1
            else:
                daily_conditions['conditions'][condition] += 1

        # Determine dominant condition
        dominant_condition = max(daily_conditions['conditions'], key=daily_conditions['conditions'].get)

        # Insert rollup data
        cursor.execute('''
        INSERT INTO daily_weather (city, date, avg_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, date('now'), ?, ?, ?, ?)
        ''', (city, daily_conditions['avg_temp'] / len(results), daily_conditions['max_temp'], daily_conditions['min_temp'], dominant_condition))

    conn.commit()
    conn.close()

# Trigger alerts based on thresholds
def check_alerts(city, weather_data):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Get the last two weather entries for the city
    cursor.execute('''
    SELECT temp FROM weather WHERE city = ? ORDER BY timestamp DESC LIMIT 2
    ''', (city,))
    last_two_temps = cursor.fetchall()

    # If both exceed threshold, trigger alert
    if len(last_two_temps) == 2 and all(temp[0] > TEMP_THRESHOLD for temp in last_two_temps):
        alert_message = f"Temperature exceeds {TEMP_THRESHOLD}°C in {city} for two consecutive updates."
        print(alert_message)
        cursor.execute('''
        INSERT INTO alerts (city, alert_message, timestamp) VALUES (?, ?, ?)
        ''', (city, alert_message, weather_data['time']))
        
        # Send an email alert
        send_email_alert(f"Weather Alert for {city}", alert_message)

    conn.commit()
    conn.close()

# Main loop to fetch weather data, store in database, and calculate rollups/alerts
def main():
    create_database()

    while True:
        for city_name in CITIES:
            weather_data = get_weather_data(city_name)
            if weather_data:
                store_weather_data(city_name, weather_data)
                check_alerts(city_name, weather_data)

        # Calculate daily rollups every 5 minutes
        calculate_daily_rollups()

        print("Sleeping for 5 minutes...")
        time.sleep(5 * 60)

if __name__ == "__main__":
    main()
