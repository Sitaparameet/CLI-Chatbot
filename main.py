from datetime import datetime
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent

from memory.cli_memory import clear_all_memories, display_memories
from memory.memory_decision import should_remember
from memory.memory_store import all_memories, save_memory
from tools.calculator import calculator
from tools.weather import get_weather
from tools.file_io import file_io
from tools.web_search import web_search

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [calculator, get_weather, file_io, web_search]
checkpointer = MemorySaver()

SYSTEM_PROMPT = """You are a helpful CLI chatbot.

Always respond in plain text.
Do not use LaTeX or mathematical formatting.

WEB SEARCH RULES:
You have access to a web_search tool.
You MUST use web_search when the user asks for:
- latest news
- current events
- recent developments
- today's information
- this week's information
- detailed research
- external facts
- research reports

When the user asks for current or latest information:
1. Always call web_search before answering.
2. Do not rely only on your internal knowledge.
3. Do not assume an old year such as 2023.
4. Use the current date when forming the search query.
5. Base your answer on the search results.
6. Mention relevant dates when appropriate."""


def get_system_prompt() -> str:
    current_date = datetime.now().strftime("%B %d, %Y")
    date_context = f"\n\nCURRENT DATE: Today's date is {current_date}."
    memories = all_memories()
    memory_text = (
        "\n\nRelevant information you remember about the user:\n"
        + "\n".join(f"- {m}" for m in memories)
        if memories else ""
    )
    return SYSTEM_PROMPT + date_context + memory_text


def show_help():
    print(
        """
CLI Chatbot

Available Commands:
/reset          - Clear conversation history
/memories       - View saved memories
/clear-memories - Clear saved memories
/exit           - Exit chatbot

You can ask questions like:
- What is 25 * 4?
- What is the weather in Ahmedabad?
"""
    )


agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer,
    system_prompt=get_system_prompt(),
)


class LoopState:
    def __init__(self):
        self.thread_id = 1
        self.running = True

    @property
    def config(self) -> dict:
        return {"configurable": {"thread_id": str(self.thread_id)}}


def handle_exit(state: LoopState):
    print("\nAssistant: Goodbye!")
    state.running = False


def handle_reset(state: LoopState):
    state.thread_id += 1
    print("\nAssistant: Conversation history has been reset.\n")


def handle_memories(state: LoopState):
    display_memories()


def handle_clear_memories(state: LoopState):
    clear_all_memories()
    state.thread_id += 1
    print("\nAssistant: All memories and conversation history have been cleared.\n")


COMMAND_HANDLERS = {
    "/exit": handle_exit,
    "/reset": handle_reset,
    "/memories": handle_memories,
    "/clear-memories": handle_clear_memories,
}


def process_memory_save(user_input: str):
    memory_decision = should_remember(user_input)
    if memory_decision.should_remember and memory_decision.memory:
        save_memory(memory_decision.memory)
        print(f"[Memory Saved: {memory_decision.memory}]")


def main():
    show_help()
    state = LoopState()

    while state.running:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                print("Assistant: Please enter a message.\n")
                continue

            cmd = user_input.lower()
            handler = COMMAND_HANDLERS.get(cmd)
            if handler:
                handler(state)
                continue

            if len(user_input) > 2000:
                print("Assistant: Your message is too long. Please keep it under 2000 characters.\n")
                continue

            process_memory_save(user_input)

            response = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=state.config,
            )
            final_content = response["messages"][-1].content
            print(f"\nAssistant: {final_content}\n")

        except Exception as e:
            print("\nAssistant: Sorry, something went wrong. Please try again.\n")
            print("Error:", e)


if __name__ == "__main__":
    main()