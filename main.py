from dotenv import load_dotenv
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI

from tools.calculator import calculator
from tools.weather import get_weather

from memory.memory_store import (
    save_memory,
    all_memories,
)

from memory.memory_decision import should_remember

from memory.cli_memory import (
    display_memories,
    clear_all_memories,
)
from tools.tool_runner import run_tools

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


SYSTEM_MESSAGE = SystemMessage(
    content=(
        "You are a helpful CLI chatbot. "
        "Always respond in plain text. "
        "Do not use LaTeX or mathematical formatting."
    )
)

conversation_history = [
    SYSTEM_MESSAGE
]


print("CLI Chatbot")

print("\nAvailable Commands:")
print("/reset - Clear conversation history")
print("/memories - View saved memories")
print("/clear-memories - Clear saved memories")
print("/exit - Exit chatbot")

print("\nYou can ask questions like:")
print("- What is 25 * 4?")
print("- What is the weather in Ahmedabad?")
print()


while True:

    user_input = input("You: ").strip()

    if not user_input:

        print(
            "Assistant: "
            "Please enter a message.\n"
        )

        continue

    if user_input.lower() == "/reset":

        conversation_history = [
            SYSTEM_MESSAGE
        ]

        print(
            "\nAssistant: "
            "Conversation history has been reset.\n"
        )

        continue

    if user_input.lower() == "/exit":

        print(
            "\nAssistant: Goodbye!"
        )

        break

    if user_input.lower() == "/memories":
        display_memories()
        continue

    if user_input.lower() == "/clear-memories":

        clear_all_memories()

        conversation_history = [
        SYSTEM_MESSAGE
        ]

        print(
            "\nAssistant: "
            "All memories and conversation history "
            "have been cleared.\n"
        )

        continue

    if len(user_input) > 2000:

        print(
            "Assistant: "
            "Your message is too long. "
            "Please keep it under 2000 characters.\n"
        )

        continue


    try:
        conversation_history.append(
            HumanMessage(
                content=user_input
            )
        )

        memory_decision = should_remember(
            user_input
        )


        if (
            memory_decision.should_remember
            and memory_decision.memory
        ):

            save_memory(
                memory_decision.memory
            )

            print(
                f"[Memory Saved: "
                f"{memory_decision.memory}]"
            )


        memories = all_memories()

        memory_context = ""

        if memories:

            memory_context = (
                "Relevant information you remember "
                "about the user:\n"
            )

            for memory in memories:

                memory_context += (
                    f"- {memory}\n"
                )


        messages_for_llm = [

            SYSTEM_MESSAGE,

            SystemMessage(
                content=memory_context
            ),

            *conversation_history[1:],

        ]

        response = llm_with_tools.invoke(
            messages_for_llm
        )


        if response.tool_calls:

            conversation_history.append(response)

            run_tools(
                response.tool_calls,
                conversation_history,
                tool_map
            )

            final_response = llm.invoke(
                conversation_history
            )


            conversation_history.append(
                final_response
            )


            print(
                f"\nAssistant: "
                f"{final_response.content}\n"
            )


        else:
            conversation_history.append(
                response
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

        if (
            conversation_history
            and isinstance(
                conversation_history[-1],
                HumanMessage
            )
        ):

            conversation_history.pop()