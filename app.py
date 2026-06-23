from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Weather code interpretation
WEATHER_DESCRIPTIONS = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "⛈️"),
    71: ("Slight snow", "🌨️"),
    73: ("Moderate snow", "🌨️"),
    75: ("Heavy snow", "🌨️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Violent rain showers", "⛈️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "🌨️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with hail", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️")
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search-cities', methods=['GET'])
def search_cities():
    """Get city suggestions based on user input"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify([])
    
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=10&language=en&format=json"
        response = requests.get(url)
        data = response.json()
        
        cities = []
        if 'results' in data:
            for result in data['results']:
                cities.append({
                    'id': f"{result['latitude']},{result['longitude']}",
                    'name': result['name'],
                    'country': result.get('country', ''),
                    'admin1': result.get('admin1', ''),
                    'lat': result['latitude'],
                    'lon': result['longitude']
                })
        
        return jsonify(cities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get current weather and 7-day forecast"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    name = request.args.get('name')
    country = request.args.get('country')
    
    if not lat or not lon:
        return jsonify({'error': 'Missing coordinates'}), 400
    
    try:
        # Get current weather and 7-day forecast
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        response = requests.get(weather_url)
        weather_data = response.json()
        
        if 'current' not in weather_data:
            return jsonify({'error': 'Unable to fetch weather data'}), 500
        
        current = weather_data['current']
        daily = weather_data['daily']
        
        # Format current weather
        weather_code = current.get('weather_code', 0)
        description, emoji = WEATHER_DESCRIPTIONS.get(weather_code, ("Unknown", "❓"))
        
        current_weather = {
            'city': name,
            'country': country,
            'temperature': current.get('temperature_2m', 'N/A'),
            'humidity': current.get('relative_humidity_2m', 'N/A'),
            'wind_speed': current.get('wind_speed_10m', 'N/A'),
            'description': description,
            'emoji': emoji,
            'code': weather_code
        }
        
        # Format 7-day forecast
        forecast = []
        for i in range(min(7, len(daily['time']))):
            date = daily['time'][i]
            code = daily['weather_code'][i]
            desc, emoji = WEATHER_DESCRIPTIONS.get(code, ("Unknown", "❓"))
            
            forecast.append({
                'date': date,
                'day': datetime.strptime(date, '%Y-%m-%d').strftime('%A'),
                'description': desc,
                'emoji': emoji,
                'max_temp': daily['temperature_2m_max'][i],
                'min_temp': daily['temperature_2m_min'][i],
                'precipitation': daily['precipitation_sum'][i]
            })
        
        return jsonify({
            'current': current_weather,
            'forecast': forecast
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
