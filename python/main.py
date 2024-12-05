from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL_WEATHER = "https://weather-app-2aoc.onrender.com/weather"
API_URL_FORECAST = "https://weather-app-2aoc.onrender.com/forecast"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                # Fetch weather data
                weather_response = requests.get(API_URL_WEATHER, params={"city": city})
                # Fetch forecast data
                forecast_response = requests.get(API_URL_FORECAST, params={"city": city})

                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                else:
                    error_message = weather_response.json().get("error", "Failed to fetch weather data.")
                
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()
                else:
                    error_message = forecast_response.json().get("error", "Failed to fetch forecast data.")
            except requests.exceptions.RequestException as e:
                error_message = f"Failed to fetch data: {str(e)}"
        else:
            error_message = "Please enter a city name."

    # return render_template("index.html", weather_data=weather_data, forecast_data=forecast_data, error_message=error_message)
    return render_template("../templates/index.html", weather_data=weather_data, forecast_data=forecast_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=False)
