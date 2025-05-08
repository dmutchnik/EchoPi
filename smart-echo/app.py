from datetime import datetime
from flask import Flask, render_template
from typing import Dict, Union
import requests

app = Flask(__name__)

@app.route("/")
def index():
    current_time = datetime.now()
    weather = open_meteo_weather(40.1163, -88.2435)
    weather_emoji_arr = weather_emoji(weather)

    return render_template("index.html",
                           time=time_string(current_time),
                           date_string=date_string(current_time),
                           time_of_day=time_of_day(current_time),
                           temperature_f=weather["temp_F"],
                           weather_emoji=weather_emoji_arr[0],
                           weather_type=weather_emoji_arr[1])

def time_of_day(current_time):
    if current_time.hour > 17:
        return "evening"
    elif current_time.hour > 11:
        return "afternoon"
    else:
        return "morning"

def time_string(current_time):
    am_pm = "AM" if current_time.hour < 12 else "PM"
    minute = "{:02d}".format(current_time.minute)
    hour = 12 if current_time.hour % 12 == 0 else current_time.hour % 12
    return f"{hour}:{minute} {am_pm}"

def date_string(current_time):
    return f"{current_time.month}/{current_time.day}/{current_time.year}"

def open_meteo_weather(lat: float, lon: float) -> Dict[str, Union[str, float]]:
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "precipitation,rain,showers,snowfall,cloudcover",
        "forecast_hours": 1,
        "timezone": "auto"
    }
    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    j = r.json()

    return {
        "rain": j["hourly"]["rain"],
        "cloudcover": j["hourly"]["cloudcover"],
        "temp_F": int(j["current_weather"]["temperature"] * 1.8 + 32),
        "snowfall": j["hourly"]["snowfall"],
        "wind_kph": j["current_weather"]["windspeed"],
    }

def weather_emoji(weather):
    if weather["snowfall"][0] > 0:
        return ["❄️", "snowing"]
    elif weather["rain"][0] > 0:
        return ["🌧️", "raining"]
    elif weather["cloudcover"][0] > 70:
        return ["🌥", "cloudy"]
    elif weather["cloudcover"][0] > 30:
        return ["⛅", "partially cloudy"]
    elif weather["wind_kph"] > 30:
        return ['🌬', "windy"]
    else:
        return ["🌤️", "sunny"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
