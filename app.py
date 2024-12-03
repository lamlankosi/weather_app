from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)


API_KEY = "1fd06231c95dbcd0fb997dd84836ab8f"
URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
        response = requests.get(URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })

        if response.status_code == 401:
            return jsonify({"error": "Invalid API key"}), 401
        elif response.status_code == 404:
            return jsonify({"error": "City not found"}), 404

        data = response.json()
        return jsonify({
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch weather data", "details": str(e)}), 500

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))