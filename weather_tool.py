import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


# ==========================================
# 1. Define Weather Tool
# ==========================================

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.

    Args:
        city: Name of the city.

    Returns:
        Current weather information.
    """

    try:
        # Get latitude and longitude of the city
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

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

        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

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
        return "Unable to retrieve weather data right now."

    except Exception:
        return "An unexpected error occurred while getting weather data."


# ==========================================
# 2. Create LLM
# ==========================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ==========================================
# 3. Bind Weather Tool
# ==========================================

llm_with_tools = llm.bind_tools(
    [get_weather]
)


# ==========================================
# 4. Ask the LLM
# ==========================================

user_message = "What is the current weather in Ahmedabad?"

response = llm_with_tools.invoke(
    user_message
)


# ==========================================
# 5. Check Tool Call
# ==========================================

if response.tool_calls:

    tool_call = response.tool_calls[0]

    print("Tool Selected:", tool_call["name"])

    print("Tool Arguments:", tool_call["args"])


    # ======================================
    # 6. Execute Weather Tool
    # ======================================

    tool_result = get_weather.invoke(
        tool_call["args"]
    )

    print("\nTool Result:")
    print(tool_result)


    # ======================================
    # 7. Send Result to LLM
    # ======================================

    final_response = llm.invoke(
        f"""
        The user asked: {user_message}

        The weather tool returned:
        {tool_result}

        Give the user a clear and concise answer.
        """
    )

    print("\nFinal AI Response:")
    print(final_response.content)


else:

    print("AI Response:")
    print(response.content)