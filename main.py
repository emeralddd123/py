from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

weather_api_key = os.getenv("WEATHER_API_KEY")



def get_weather(client_ip):
    try:
        response = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key=${weather_api_key}&q=${client_ip}"
        )
        if response.status_code == 200:
            print(response.json())
            return response.json()
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
    if "X-Forwarded-For" in request.headers:
        user_ip = request.headers["X-Forwarded-For"].split(",")[0]
        print (user_ip)
    else:
        user_ip = request.remote_addr
    print(f"Request from {user_ip}")
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    # city, country = get_city_and_country(user_ip)
    weather = get_weather(user_ip)

    if weather:
        temperature = weather.get("current").get("temp_c")
        city = weather.get("location").get("name")
        return jsonify(
            {
                "client_ip": user_ip,
                "location": city,
                "greeting": f"Hello, {request.args.get('visitor_name', '')}!, the temperature is {temperature} degrees Celsius in {city}",
            }
        )
    else:
        return {"error": "Unable to fetch weather information."}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
