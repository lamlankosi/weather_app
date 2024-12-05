from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = "1fd06231c95dbcd0fb997dd84836ab8f"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


IMAGE_MAP = {
    "clear sky": "https://lamlankosi.github.io/project_images/Images/clear.png",
    "few clouds": "https://lamlankosi.github.io/project_images/Images/cloud.png",
    "overcast clouds": "https://lamlankosi.github.io/project_images/Images/cloud.png",
    "broken clouds": "https://lamlankosi.github.io/project_images/Images/cloud.png",
    "shower rain": "https://lamlankosi.github.io/project_images/Images/rain.png",
    "rain": "https://lamlankosi.github.io/project_images/Images/rain.png",
    "light rain": "https://lamlankosi.github.io/project_images/Images/rain.png",
    "moderate rain": "https://lamlankosi.github.io/project_images/Images/rain.png",
    "thunderstorm": "https://lamlankosi.github.io/project_images/Images/snow.png",
    "snow": "https://lamlankosi.github.io/project_images/Images/snow.png",
    "mist": "https://lamlankosi.github.io/project_images/Images/cloud.png"
}

def get_image(description):
    return IMAGE_MAP.get(description.lower(), "https://lamlankosi.github.io/project_images/Images/cloud.png")

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
        response = requests.get(CURRENT_WEATHER_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })

        if response.status_code == 401:
            return jsonify({"error": "Invalid API key"}), 401
        elif response.status_code == 404:
            return jsonify({"error": "City not found"}), 404

        data = response.json()
        description = data["weather"][0]["description"]
        image_url = get_image(description)

        return jsonify({
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": description,
            "image": image_url,
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", "N/A"),
            "humidity": data["main"]["humidity"]
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch weather data", "details": str(e)}), 500

@app.route('/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
        response = requests.get(FORECAST_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })

        if response.status_code == 401:
            return jsonify({"error": "Invalid API key"}), 401
        elif response.status_code == 404:
            return jsonify({"error": "City not found"}), 404

        data = response.json()
        
       
        daily_forecast = {}
        for item in data.get("list", []):
            date = item["dt_txt"].split(" ")[0]
            # changes the date to a day 
            weekday = datetime.strptime(date, "%Y-%m-%d").strftime("%A") 
            if date not in daily_forecast:
                daily_forecast[date] = {
                    "day": weekday,
                    "temperature_min": item["main"]["temp_min"],
                    "temperature_max": item["main"]["temp_max"],
                    "description": item["weather"][0]["description"],
                    "image": get_image(item["weather"][0]["description"]),
                    "wind_speed": item["wind"]["speed"],
                    "humidity": item["main"]["humidity"]
                }
            else:
              
                daily_forecast[date]["temperature_min"] = min(
                    daily_forecast[date]["temperature_min"], item["main"]["temp_min"])
                daily_forecast[date]["temperature_max"] = max(
                    daily_forecast[date]["temperature_max"], item["main"]["temp_max"])

        forecast_list = [
            {
                "date": date,
                "day": details["day"],
                "temperature_min": details["temperature_min"],
                "temperature_max": details["temperature_max"],
                "description": details["description"],
                "image": details["image"],
                "wind_speed": details["wind_speed"],
                "humidity": details["humidity"]
            }
            for date, details in daily_forecast.items()
        ]

        return jsonify({
            "city": data["city"]["name"],
            "forecast": forecast_list
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch forecast data", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    # app.run(debug=True)
