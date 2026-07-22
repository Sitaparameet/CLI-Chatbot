import requests
from langchain_core.tools import tool
import re

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.
    """

    city = city.strip()

    if not city:
        return "Error: City name cannot be empty."

    if len(city) > 20:
        return "Error: City name is too long."

    if not re.fullmatch(
         r"[A-Za-zÀ-ÿ\s.'-]+",
        city
    ):
        return (
            "Error: Invalid city name. "
            "Please enter a valid city."
        )

    try:
        geocoding_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )

        geocoding_response = requests.get(
            geocoding_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        geocoding_response.raise_for_status()

        location_data = geocoding_response.json()

        if "results" not in location_data:
            return f"Could not find the city: {city}"

        location = location_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
                "timezone": "auto"
            },
            timeout=10
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]


        return (
            f"Weather in {city_name}: "
            f"Temperature: {temperature}°C, "
            f"Wind Speed: {wind_speed} km/h"
        )


    except requests.RequestException:

        return (
            "Unable to retrieve weather data right now."
        )


    except Exception:

        return (
            "An unexpected error occurred "
            "while getting weather data."
        )
