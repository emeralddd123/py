from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, request
import requests

app = Flask(__name__)

open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")


def get_public_ip():
    try:
        # response = requests.get("https://api.ipify.org?format=json")
        # if response.status_code == 200:
        #     print(response.json())
        #     return response.json().get("ip")
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        print("Client IP:", client_ip)
        return client_ip
        # else:
        #     return None
    except Exception as e:
        print(f"Error getting public IP: {e}")
        return None


def get_city_and_country(public_ip):
    try:
        if public_ip:
            response = requests.get(f"http://ip-api.com/json/{public_ip}")
            if response.status_code == 200:
                return response.json().get("city"), response.json().get("country")
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error getting city: {e}")
        return None


def get_weather(city, country):
    try:
        if city:
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={open_weather_api_key}&units=metric"
            )
            if response.status_code == 200:
                return response.json()
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error getting weather: {e}")
        return None


@app.route("/")
def log_request():
    private_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print("Private IP:", private_ip)
    public_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    city, country = get_city_and_country(public_ip)
    weather = get_weather(city, country)
    # print("Private IP:", private_ip)
    # print("Public IP:", public_ip)
    # print("Weather:", weather)
    if weather:
        temperature = weather.get("main").get("temp")
        return {
            "client_ip": private_ip,
            "location": city,
            "greeting": f"Hello, {request.args.get('visitor_name', '')}!, the temperature is {temperature} degrees Celsius in {city}",
        }
    else:
        return {"error": "Unable to fetch weather information."}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
