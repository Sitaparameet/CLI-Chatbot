from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

@tool
def calculator(expression: str) -> str:
    """
    Calculate a basic mathematical expression.

    Args:
        expression: Mathematical expression such as
                    '10 + 5' or '20 * 4'.

    Returns:
        The calculated result.
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception:
        return "Unable to calculate the expression."


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


llm_with_tools = llm.bind_tools(
    [calculator]
)


user_message = "What is 25 multiplied by 4?"

response = llm_with_tools.invoke(
    user_message
)



if response.tool_calls:

    tool_call = response.tool_calls[0]

    print("Tool Selected:", tool_call["name"])

    print("Tool Arguments:", tool_call["args"])


    tool_result = calculator.invoke(
        tool_call["args"]
    )

    print("Tool Result:", tool_result)


    final_response = llm.invoke(
        f"""
        The user asked: {user_message}

        The calculator tool returned: {tool_result}

        Give the user a clear and concise final answer.
        """
    )

    print("\nFinal AI Response:")
    print(final_response.content)

else:

    print("AI Response:")
    print(response.content)