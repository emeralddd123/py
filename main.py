from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

weather_api_key = os.getenv("WEATHER_API_KEY")

def get_city(client_ip):
    try:
        response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        if response.status_code == 200:
            data = response.json()
            city = data.get("city")
            return city
        else:
            print(response.json())
            return None
    except Exception as e:
        print(f"Error getting city: {e}")
        return None

def get_weather(city):
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric")
        if response.status_code == 200:
            print(response.json())
            return response.json().get("main").get("temp")
        else:
            print(response.json())
            return None

    except Exception as e:
        print(f"Error getting weather: {e}")
        return None


@app.route("/")
def index():
    return jsonify(
        {"success": True, "message": "Welcome to user geographical condition app"}
    )


@app.route("/api/hello")
def log_request():
    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(",")[0]
    city = get_city(user_ip)
    temperature = get_weather(city)

    if temperature:

        return jsonify(
            {
                "client_ip": user_ip,
                "location": city,
                "greeting": f"Hello, {request.args.get('visitor_name', 'visitor')}!, the temperature is {temperature} degrees Celsius in {city}",
            }
        )
    else:
        return {"error": "Unable to fetch weather information."}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
