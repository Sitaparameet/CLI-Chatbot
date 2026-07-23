from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

from memory.cli_memory import clear_all_memories, display_memories
from memory.memory_decision import should_remember
from memory.memory_store import all_memories, save_memory
from tools.calculator import calculator
from tools.weather import get_weather

load_dotenv()

# Initialize LLM and Agent Tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [calculator, get_weather]
checkpointer = MemorySaver()


def dynamic_prompt(state: dict) -> list:
    """Build dynamic prompt with system instructions and current memories."""
    memories = all_memories()
    memory_text = ""
    if memories:
        memory_text = (
            "\n\nRelevant information you remember about the user:\n"
            + "\n".join(f"- {m}" for m in memories)
        )

    system_message = SystemMessage(
        content=(
            "You are a helpful CLI chatbot. "
            "Always respond in plain text. "
            "Do not use LaTeX or mathematical formatting."
            f"{memory_text}"
        )
    )

    return [system_message] + state["messages"]


# Build LangGraph React Agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer,
    prompt=dynamic_prompt,
)


def main():
    print("CLI Chatbot (Powered by LangGraph)")
    print("\nAvailable Commands:")
    print("/reset          - Clear conversation history")
    print("/memories       - View saved memories")
    print("/clear-memories - Clear saved memories")
    print("/exit           - Exit chatbot")
    print("\nYou can ask questions like:")
    print("- What is 25 * 4?")
    print("- What is the weather in Ahmedabad?")
    print()

    thread_id = 1
    config = {"configurable": {"thread_id": str(thread_id)}}

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                print("Assistant: Please enter a message.\n")
                continue

            cmd = user_input.lower()

            if cmd == "/exit":
                print("\nAssistant: Goodbye!")
                break

            if cmd == "/reset":
                thread_id += 1
                config = {"configurable": {"thread_id": str(thread_id)}}
                print("\nAssistant: Conversation history has been reset.\n")
                continue

            if cmd == "/memories":
                display_memories()
                continue

            if cmd == "/clear-memories":
                clear_all_memories()
                thread_id += 1
                config = {"configurable": {"thread_id": str(thread_id)}}
                print(
                    "\nAssistant: All memories and conversation history have been cleared.\n"
                )
                continue

            if len(user_input) > 2000:
                print(
                    "Assistant: Your message is too long. Please keep it under 2000 characters.\n"
                )
                continue

            # Check if user message contains durable memory to save
            memory_decision = should_remember(user_input)
            if memory_decision.should_remember and memory_decision.memory:
                save_memory(memory_decision.memory)
                print(f"[Memory Saved: {memory_decision.memory}]")

            # Invoke LangGraph agent
            response = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
            )

            # Retrieve final message content
            final_content = response["messages"][-1].content
            print(f"\nAssistant: {final_content}\n")

        except Exception as e:
            print("\nAssistant: Sorry, something went wrong. Please try again.\n")
            print("Error:", e)


if __name__ == "__main__":
    main()