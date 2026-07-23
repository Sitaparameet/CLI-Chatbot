from memory.memory_store import (
    all_memories,
    clear_memories,
)


def display_memories():
    memories = all_memories()

    print("\nAssistant: Here are the current memories:")

    if not memories:
        print("No memories saved yet.")
    else:
        for i, memory in enumerate(memories, 1):
            print(f"{i}. {memory}")

    print()


def clear_all_memories():
    clear_memories()

    print(
        "\nAssistant: "
        "All memories have been cleared.\n"
    )
