from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_URL = "https://weather-app-2aoc.onrender.com/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                
                response = requests.get(API_URL, params={"city": city})
                if response.status_code == 200:
                    weather_data = response.json()
                else:
                    error_message = response.json().get("error", "Something went wrong!")
            except requests.exceptions.RequestException as e:
                error_message = f"Failed to fetch data: {str(e)}"
        else:
            error_message = "Please enter a city name."

    return render_template("index.html", weather_data=weather_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
