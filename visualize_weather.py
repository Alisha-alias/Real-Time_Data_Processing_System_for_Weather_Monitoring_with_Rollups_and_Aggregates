import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to fetch daily weather data from the SQLite database
def fetch_daily_weather_data():
    conn = sqlite3.connect('weather_data.db')
    query = '''
        SELECT city, date, avg_temp, max_temp, min_temp, dominant_condition
        FROM daily_weather
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to visualize average, min, and max temperatures
def visualize_temp_summary(df, output_folder):
    # Set up the bar plot
    temp_summary = df[['city', 'avg_temp', 'min_temp', 'max_temp']]
    ax = temp_summary.set_index('city').plot(kind='bar', figsize=(12, 6), alpha=0.7)

    # Customize the plot
    plt.title('Temperature Summary for Indian Cities')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()

    # Save the plot
    plt.savefig(os.path.join(output_folder, 'temperature_summary.png'))
    plt.show()  # Display the plot
    plt.close()  # Close the plot

# Function to visualize average temperature with color based on dominant condition
def visualize_dominant_weather(df, output_folder):
    # Get the average temperature and dominant condition for each city
    avg_temp_dominant = df.groupby(['city', 'dominant_condition'])['avg_temp'].mean().reset_index()

    # Define a color map for dominant conditions
    color_map = {
        'Clear': 'skyblue',
        'Clouds': 'gray',
        'Rain': 'blue',
        'Drizzle': 'lightblue',
        'Thunderstorm': 'purple',
        'Snow': 'white',
        'Mist': 'lightgray',
        'Haze': 'orange',  # Added Haze condition
        # Add more conditions as needed
    }

    # Map colors based on dominant condition
    avg_temp_dominant['color'] = avg_temp_dominant['dominant_condition'].map(color_map)

    # Create the bar plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(avg_temp_dominant['city'], avg_temp_dominant['avg_temp'], color=avg_temp_dominant['color'])

    # Add labels for the dominant condition on each bar
    for bar, dominant_condition in zip(bars, avg_temp_dominant['dominant_condition']):
        plt.text(bar.get_x() + bar.get_width() / 2, 
                 bar.get_height(), 
                 dominant_condition, 
                 ha='center', 
                 va='bottom')  # Position above the bar

    # Customize the plot
    plt.title('Average Temperature by City with Dominant Weather Condition')
    plt.xlabel('City')
    plt.ylabel('Average Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()

    # Save the plot
    plt.savefig(os.path.join(output_folder, 'dominant_weather.png'))
    plt.show()  # Display the plot
    plt.close()  # Close the plot

if __name__ == '__main__':
    # Define the output folder
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    # Fetch daily weather data
    daily_weather_data = fetch_daily_weather_data()

    # Visualize temperature summary and save
    visualize_temp_summary(daily_weather_data, output_folder)

    # Visualize dominant weather conditions with avg_temp and save
    visualize_dominant_weather(daily_weather_data, output_folder)
