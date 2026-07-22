from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tools.calculator import calculator
from tools.weather import get_weather

load_dotenv()

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
        print("\nAssistant: Conversation history has been reset.\n")

        continue


    if not user_input:
        print("Assistant: Please enter a message.")
        continue

    if len(user_input) > 2000:
        print(
            "Assistant: Your message is too long. "
            "Please keep it under 2000 characters."
        )

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