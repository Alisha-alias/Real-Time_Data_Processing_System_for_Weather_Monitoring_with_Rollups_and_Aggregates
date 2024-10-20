# Real-Time_Data_Processing_System_for_Weather_Monitoring_with_Rollups_and_Aggregates
Developing a real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates. The system will utilize data from the OpenWeatherMap API (https://openweathermap.org/).

## **Table of Contents**
- [Project Overview](#project-overview)
- [Features](#features)
  - [Real-Time Weather Monitoring](#real-time-weather-monitoring)
  - [Weather Alerts](#weather-alerts)
  - [Daily Weather Aggregation](#daily-weather-Aggregation)
  - [Weather Visualization](#weather-visualization)    
- [Technologies Used](#technologies-used)
  - [Backend](#backend)
  - [Database](#database)
  - [Visualization](#visualization)
- [Build Instructions](#build-instructions)
  - [1. Cloning the Repository](#1-cloning-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install the Dependencies](#3-install-the-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Run the Weather Monitoring System](#5-run-the-weather-monitor-system)
  - [6. Visualizing Weather Data](#5-visualizing-weather-data)
- [Design Choices](#design-choices)
  - [Weather Data Processing](#weather-data-processing)
  - [Database Design](#database-design)
  - [Visualization Choices](#visualization-choices)
- [Usage](#usage)
  - [Monitoring Weather Data](#monitoring-weather-data)
  - [Triggering Alerts](#triggering-alerts)
  - [Visualizing Data](#visualizing-data)


## **Project Overview**

This project provides a real-time weather monitoring system that fetches data from the OpenWeatherMap API for multiple cities in India. It stores data in an SQLite database, triggers alerts based on weather thresholds, and provides visualizations for aggregated daily data.


## **Features**

### **Real-Time Weather Monitoring**
Fetches weather data every 5 minutes for predefined cities: Delhi, Mumbai, Chennai, Bangalore, Kolkata, and Hyderabad.

### **Weather Alerts**
Sends email alerts if a city’s temperature exceeds the threshold for two consecutive updates.

### **Daily Weather Aggregation**
Processes daily weather data to calculate average, maximum, minimum temperatures, and dominant weather conditions.

### **Weather Visualization**
Provides visual summaries of daily weather data with graphs showing temperature trends and dominant conditions.


## **Technologies Used**

### **Backend**
 - Python (For data fetching, processing, and alerting)
 - Flask (For API and web framework)
### **Database**
 - SQLite (For storing weather data and alerts)
### **Visualization**
 - Matplotlib (For plotting weather summaries)
 - Pandas (For data manipulation)


## **Build Instructions**

### **1. Cloning the Repository**
Clone the project repository to your local machine:
    
    ```bash
    git clone https://github.com/Alisha-alias/Real-Time_Data_Processing_System_for_Weather_Monitoring_with_Rollups_and_Aggregates.git
    cd weather-monitoring-system
    
### **2. Set Up Virtual Environment**
Create a Python virtual environment to manage dependencies:
   
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Windows, use 'venv\Scripts\activate'
    
### **3. Install Dependencies**
Install the necessary Python libraries:
    
    ```bash
    pip install -r requirements.txt
    
### **4. Configure Environment Variables**
Set the environment variables for OpenWeatherMap API key and email credentials in .env:
    
    makefile
    API_KEY=<your_openweathermap_api_key>
    EMAIL_ADDRESS=<your_email>
    EMAIL_PASSWORD=<your_email_password>
    RECEIVER_EMAIL=<receiver_email>
    
### **5. Running the Weather Monitoring System**
Run the weather monitoring script:
    
    ```bash
    python real_time_weather_monitor.py
    
### **6. Visualizing Weather Data**
To visualize the daily weather summary, use:
    
    ```bash
    python visualize_weather.py
The output images will be saved in the output folder.


## **Design Choices**

### **Weather Data Processing**
 - The weather data is fetched every 5 minutes from the OpenWeatherMap API and stored in an SQLite database. The choice of SQLite is made for simplicity and ease of use for small datasets.

### **Database Design**
 - The database stores raw weather data, daily summaries, and alerts in separate tables. It allows efficient querying for daily rollups and alerting.

### **Visualization Choices**
 - Visualizations include a temperature summary for Indian cities and average temperatures annotated with the dominant weather condition. These choices aim to provide a clear and concise view of the most relevant weather information.


## **Usage**

### **Monitoring Weather Data**
 - The real-time script automatically fetches data and stores it in the database at regular intervals. You can check the database for raw weather data and alerts.

### **Triggering Alerts**
 - Alerts are automatically sent via email when a city experiences high temperatures for two consecutive updates. You can modify the threshold in the script.

### **Visualizing Data**
 - Use the visualization script to generate charts that summarize daily weather conditions. These can help in understanding temperature trends and dominant weather patterns across cities.
