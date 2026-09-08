#!/usr/bin/env python3

import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

CITIES = {
    "ahmedabad": {
        "latitude": 23.0225,
        "longitude": 72.5714,
        "timezone": "Asia/Kolkata",
    },
    "davao": {
        "latitude": 7.0731,
        "longitude": 125.6128,
        "timezone": "Asia/Manila",
    },
}

WEATHER = {
    0:  ("☀", "Clear"),
    1:  ("☀", "Mainly clear"),
    2:  ("☁", "Partly cloudy"),
    3:  ("☁", "Cloudy"),
    45: ("≋", "Fog"),
    48: ("≋", "Fog"),
    51: ("☂", "Light drizzle"),
    53: ("☂", "Drizzle"),
    55: ("☂", "Heavy drizzle"),
    61: ("☂", "Light rain"),
    63: ("☂", "Rain"),
    65: ("☂", "Heavy rain"),
    71: ("❄", "Light snow"),
    73: ("❄", "Snow"),
    75: ("❄", "Heavy snow"),
    80: ("☂", "Rain showers"),
    81: ("☂", "Rain showers"),
    82: ("☂", "Heavy showers"),
    95: ("⚡", "Thunderstorm"),
    96: ("⚡", "Thunderstorm"),
    99: ("⚡", "Thunderstorm"),
}


def get_weather(city):
    info = CITIES[city]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={info['latitude']}"
        f"&longitude={info['longitude']}"
        "&current=temperature_2m,weather_code"
        "&hourly=temperature_2m,weather_code"
        "&forecast_days=1"
        f"&timezone={info['timezone']}"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Conky Weather"}
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)

    current_temp = round(data["current"]["temperature_2m"])
    current_code = data["current"]["weather_code"]

    current_icon, current_description = WEATHER.get(
        current_code,
        ("?", "Unknown")
    )

    times = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]
    codes = data["hourly"]["weather_code"]

#    current_hour = datetime.now().strftime("%Y-%m-%dT%H:00")
    current_hour = datetime.now(ZoneInfo(info["timezone"])).strftime("%Y-%m-%dT%H:00")

    try:
        index = times.index(current_hour)
    except ValueError:
        index = 0

    print(f"{current_temp}°C|{current_icon}|{current_description}")

    for i in range(index, min(index + 4, len(times))):
        hour = datetime.fromisoformat(times[i]).strftime("%H:%M")
        temp = round(temperatures[i])
        icon, _ = WEATHER.get(codes[i], ("?", "Unknown"))

        print(f"{hour}|{temp}°|{icon}")


if __name__ == "__main__":
    city = "ahmedabad"

    if len(__import__("sys").argv) > 1:
        city = __import__("sys").argv[1].lower()

    if city not in CITIES:
        print("Unknown city")
        raise SystemExit(1)

    get_weather(city)
