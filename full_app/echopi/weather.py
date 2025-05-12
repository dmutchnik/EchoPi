from datetime import datetime
from typing import Dict, Union
import requests

# ‑‑ helpers previously inside old app.py ‑‑
def time_of_day(now: datetime):
    return "evening" if now.hour > 17 else "afternoon" if now.hour > 11 else "morning"

def time_string(now: datetime):
    ampm   = "AM" if now.hour < 12 else "PM"
    minute = f"{now.minute:02d}"
    hour   = 12 if now.hour % 12 == 0 else now.hour % 12
    return f"{hour}:{minute} {ampm}"

def date_string(now: datetime):
    return f"{now.month}/{now.day}/{now.year}"

def open_meteo_weather(lat: float, lon: float) -> Dict[str, Union[str, float]]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon, "current_weather": "true",
        "hourly": "precipitation,rain,showers,snowfall,cloudcover",
        "forecast_hours": 1, "timezone": "auto"
    }
    j = requests.get(url, params=params, timeout=5).json()
    return {
        "rain": j["hourly"]["rain"],
        "cloudcover": j["hourly"]["cloudcover"],
        "temp_F": int(j["current_weather"]["temperature"] * 1.8 + 32),
        "snowfall": j["hourly"]["snowfall"],
        "wind_kph": j["current_weather"]["windspeed"],
    }

def weather_emoji(w):
    if w["snowfall"][0] > 0:        return ["❄️", "snowing"]
    if w["rain"][0] > 0:            return ["🌧️", "raining"]
    if w["cloudcover"][0] > 70:     return ["🌥", "cloudy"]
    if w["cloudcover"][0] > 30:     return ["⛅", "partially cloudy"]
    if w["wind_kph"] > 30:          return ['🌬', "windy"]
    return ["🌤️", "sunny"]