import requests
import tkinter as tk
from tkinter import messagebox

def get_weather():
    api_key = 'deba2fe6185f18bbb4719483b0dad32c'  # OpenWeatherMap API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?'

    city = city_entry.get()
    complete_url = f'{base_url}q={city}&appid={api_key}&units=metric'
    forecast_complete_url = f'{forecast_url}q={city}&appid={api_key}&units=metric'

    response = requests.get(complete_url)
    forecast_response = requests.get(forecast_complete_url)

    data = response.json()
    forecast_data = forecast_response.json()

    if data["cod"] != "404":
        weather_info = {
            'City': city.title(),
            'Temperature (Celsius)': f"{data['main']['temp']:.2f}°C",
            'Temperature (Fahrenheit)': f"{(data['main']['temp'] * 9 / 5) + 32:.2f}°F",
            'Humidity': f"{data['main']['humidity']}%",
            'Wind Speed': f"{data['wind']['speed']} m/s",
            'Description': data['weather'][0]['description'].title()
        }

        weather_display.delete(1.0, tk.END)  # Clear previous data

        # Set tags for bold formatting
        weather_display.tag_configure("bold", font=("Arial", 10, "bold"))

        # Display current weather
        weather_display.insert(tk.END, "Current Weather:\n\n", "bold")
        for key, value in weather_info.items():
            weather_display.insert(tk.END, f'{key}: ', "bold")
            weather_display.insert(tk.END, f'{value}\n')
        weather_display.insert(tk.END, "\n")

        # Display forecast for the next five days
        weather_display.insert(tk.END, "Forecast for the next five days:\n\n", "bold")
        for forecast in forecast_data['list']:
            forecast_info = {
                'Date': forecast['dt_txt'],
                'Temperature (Celsius)': f"{forecast['main']['temp']:.2f}°C",
                'Temperature (Fahrenheit)': f"{(forecast['main']['temp'] * 9 / 5) + 32:.2f}°F",
                'Humidity': f"{forecast['main']['humidity']}%",
                'Wind Speed': f"{forecast['wind']['speed']} m/s",
                'Description': forecast['weather'][0]['description'].title()
            }
            weather_display.insert(tk.END, f"Date: {forecast_info['Date']}\n", "bold")
            for key, value in forecast_info.items():
                if key != 'Date':
                    weather_display.insert(tk.END, f'{key}: ', "bold")
                    weather_display.insert(tk.END, f'{value}\n')
            weather_display.insert(tk.END, "\n")
    else:
        messagebox.showerror('Error', 'City not found!')

def clear_weather():
    weather_display.delete(1.0, tk.END)  # Clear weather data
    city_entry.delete(0, tk.END)  # Clear input box

def on_enter(event):
    get_weather()
    
# Create the main window
root = tk.Tk()
root.title("Weather App by Ajith")

# Create and place UI elements
tk.Label(root, text="Enter City:").pack()
city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack()

clear_weather_button = tk.Button(root, text="Clear", command=clear_weather)
clear_weather_button.pack()

weather_display = tk.Text(root, height=40, width=40)
weather_display.pack()

# Bind Enter key to call get_weather function
root.bind('<Return>', on_enter)

root.mainloop()