import re
import requests
from langchain_core.tools import tool
from tools.tool_logger import log_tool


@tool
@log_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    city = city.strip()

    if not city:
        return "Error: City name cannot be empty."
    if len(city) > 20:
        return "Error: City name is too long."
    if not re.fullmatch(r"[A-Za-zÀ-ÿ\s.'-]+", city):
        return "Error: Invalid city name. Please enter a valid city."

    try:
        geo_res = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        geo_res.raise_for_status()
        locations = geo_res.json().get("results")

        if not locations:
            return f"Could not find the city: {city}"

        location = locations[0]
        weather_res = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_res.raise_for_status()
        curr = weather_res.json()["current"]

        return (
            f"Weather in {location['name']}: "
            f"Temperature: {curr['temperature_2m']}°C, "
            f"Wind Speed: {curr['wind_speed_10m']} km/h"
        )
    except requests.RequestException:
        return "Unable to retrieve weather data right now."
    except Exception:
        return "An unexpected error occurred while getting weather data."