from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os
from tools.ai_tools import get_coordinates_from_request, get_recommendations, get_image, get_granma_image

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Open-Meteo Weather API endpoint
API_URL = os.getenv('API_URL') or "https://api.open-meteo.com/v1/forecast"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip()
    city_data = get_coordinates_from_request(query)
    if city_data.get('error'):
        return jsonify({"error": "I could not find the city"}), 404
    try:
        params = {
            'latitude': city_data['latitude'],
            'longitude': city_data['longitude'],
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
            'timezone': 'auto',
            'current': 'temperature_2m,wind_speed_10m,relative_humidity_2m,precipitation'
        }
        response = requests.get(API_URL, params=params)
        data = response.json()
        
        # Format the data for display
        formatted_data = {
            'current': {
                'temperature': data['current']['temperature_2m'],
                'humidity': data['current']['relative_humidity_2m'],
                'wind_speed': data['current']['wind_speed_10m'],
                'precipitation': data['current']['precipitation'],
            },
            'daily': [],
            'city': city_data['city_name']
        }
        
        # Format daily forecast
        for i in range(7):
            daily_data = {
                'date': data['daily']['time'][i],
                'max_temp': data['daily']['temperature_2m_max'][i],
                'min_temp': data['daily']['temperature_2m_min'][i],
                'precipitation': data['daily']['precipitation_sum'][i]
            }
            formatted_data['daily'].append(daily_data)

        recommendations = get_recommendations(formatted_data['current'], formatted_data['city'])
        formatted_data['recommendations'] = recommendations

        image = get_image(f"{city_data['city_name']} city at ${city_data['local_time']} time")
        formatted_data['image'] = image

        granma_image = get_granma_image()
        formatted_data['granma'] = granma_image

        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 