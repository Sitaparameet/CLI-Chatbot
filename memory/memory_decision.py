from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


load_dotenv()


class MemoryDecision(BaseModel):
    should_remember: bool = Field(
        description="Whether the user's message contains a durable fact worth remembering."
    )

    memory: str | None = Field(
        default=None,
        description="The concise memory to save if should_remember is true."
    )

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


memory_llm = llm.with_structured_output(MemoryDecision)


def should_remember(user_message: str) -> MemoryDecision:
    """
    Decide whether a user's message contains a durable fact
    that should be saved as persistent memory.
    """

    prompt = f"""
You are a memory decision system for a conversational chatbot.

Decide whether the user's message contains a durable fact
that would be useful to remember in future conversations.

Remember durable information such as:
- User's name
- User's location
- User's occupation
- User's long-term interests
- User's preferences
- User's ongoing projects or learning goals

Do NOT remember:
- Greetings
- Small talk
- Temporary questions
- One-time calculations
- General questions
- Jokes
- Casual conversation

If the message contains a durable fact:
- Set should_remember to true.
- Create a concise memory statement.

If it does not contain a durable fact:
- Set should_remember to false.
- Set memory to null.

User message:
{user_message}
"""

    return memory_llm.invoke(prompt)

if __name__ == "__main__":

    test_messages = [
        "My name is Meet.",
        "I am learning Agentic AI.",
        "What is 25 multiplied by 4?",
        "Hello, how are you?"
    ]

    for message in test_messages:

        result = should_remember(message)

        print("\nUser:", message)
        print("Should Remember:", result.should_remember)
        print("Memory:", result.memory)