import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY is not found in .env")
    exit()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
)

conversation_history = []

print("CLI Chatbot")
print("/reset - Clear conversation history")
print("/exit  - Exit the chatbot")


while True:

    # Get user input
    user_input = input("You: ").strip()

    if user_input.lower() == "/exit":
        print("\nAssistant: Goodbye!")
        break

    if user_input.lower() == "/reset":

        conversation_history = []

        print("\nAssistant: Conversation history has been reset.\n")

        continue

    if not user_input:
        print("Please enter a message.\n")
        continue

    conversation_history.append(
        HumanMessage(content=user_input)
    )

    try:

        response = llm.invoke(
            conversation_history
        )

        conversation_history.append(
            AIMessage(content=response.content)
        )

        print(f"\nAssistant: {response.content}\n")

    except Exception as e:

        print(
            "\nAssistant: Sorry, I couldn't process "
            "your request. Please try again.\n"
        )

        print("Error:", e)

        # Remove the user's message if API call failed
        conversation_history.pop()