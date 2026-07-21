from langchain_core.messages import SystemMessage
import requests
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

@tool
def calculator(expression: str) -> str:
    """
    Calculate a basic mathematical expression.

    Args:
        expression: A mathematical expression such as
                    '10 + 5' or '20 * 4'.

    Returns:
        The calculated result.
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception:
        return "Unable to calculate the expression."


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.

    Args:
        city: Name of the city.

    Returns:
        Current temperature and wind speed.
    """

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


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


tools = [
    calculator,
    get_weather
]


tool_map = {
    tool.name: tool
    for tool in tools
}



llm_with_tools = llm.bind_tools(tools)


conversation_history = [
    SystemMessage(
        content=(
            "You are a helpful CLI chatbot. "
            "Always respond in plain text. "
            "Do not use LaTeX or mathematical formatting."
        )
    )
]



print("CLI Chatbot")

print("\nAvailable Commands:")
print("/reset - Clear conversation history")
print("/exit  - Exit chatbot") 

print("\nYou can ask questions like:")
print("- What is 25 * 4?")
print("- What is the weather in Ahmedabad?")
print()


while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "/exit":

        print("\nAssistant: Goodbye!")

        break

    if user_input.lower() == "/reset":

        conversation_history = []

        print(
            "\nAssistant: "
            "Conversation history has been reset.\n"
        )

        continue

    if not user_input:

        print(
            "Assistant: "
            "Please enter a message.\n"
        )

        continue


    conversation_history.append(
        HumanMessage(content=user_input)
    )


    try:

        response = llm_with_tools.invoke(
            conversation_history
        )

        if response.tool_calls:

            conversation_history.append(response)


            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]

                tool_args = tool_call["args"]


                # print(
                #     f"\n[Tool Selected: {tool_name}]"
                # )

                # print(
                #     f"[Tool Arguments: {tool_args}]"
                # )


                selected_tool = tool_map.get(
                    tool_name
                )

                if selected_tool is None:

                    tool_result = (
                        f"Unknown tool: {tool_name}"
                    )

                else:


                    tool_result = selected_tool.invoke(
                        tool_args
                    )



                conversation_history.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call["id"]
                    )
                )

            final_response = llm.invoke(
                conversation_history
            )


            conversation_history.append(
                AIMessage(
                    content=final_response.content
                )
            )

            print(
                f"Assistant: "
                f"{final_response.content}\n"
            )


        else:

            conversation_history.append(
                AIMessage(
                    content=response.content
                )
            )


            print(
                f"\nAssistant: "
                f"{response.content}\n"
            )


    except Exception as e:

        print(
            "\nAssistant: "
            "Sorry, something went wrong. "
            "Please try again.\n"
        )

        print(
            "Error:",
            e
        )
        conversation_history.pop()