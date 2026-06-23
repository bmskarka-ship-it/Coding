import requests
from datetime import datetime

name = input("What is your name? ")
location = input("What is your current city/location? ")

try:
    # Get coordinates for the location using geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()
    
    if geo_data['results']:
        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        city = geo_data['results'][0]['name']
        country = geo_data['results'][0].get('country', '')
        
        # Get weather data using Open-Meteo API
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&timezone=auto"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if 'current' not in weather_data:
            print(f"Error: API response structure unexpected. Response: {weather_data}")
            exit()
        
        current_weather = weather_data['current']
        temp = current_weather.get('temperature_2m', 'N/A')
        humidity = current_weather.get('relative_humidity_2m', 'N/A')
        weather_code = current_weather.get('weather_code', 'N/A')
        
        # Weather code interpretation
        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail"
        }
        
        description = weather_descriptions.get(weather_code, f"Weather code: {weather_code}")
        
        print(f"\nHello, {name}!")
        print(f"Location: {city}, {country}")
        print(f"Current Weather: {description}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%\n")
    else:
        print(f"Location '{location}' not found. Please try again.")
except Exception as e:
    print(f"Error fetching weather data: {e}")