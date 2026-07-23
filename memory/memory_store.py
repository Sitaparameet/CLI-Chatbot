import json
from pathlib import Path

MEMORY_FILE = Path("data/memory.json")


def load_memories() -> list[str]:
    """Load all saved memories from the JSON file."""
    if not MEMORY_FILE.exists():
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_memory(memory: str) -> None:
    """Save a new memory to the JSON file if not already stored."""
    memories = load_memories()
    memory = memory.strip()

    if not memory:
        return

    if memory not in memories:
        memories.append(memory)
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(memories, file, indent=4)


def clear_memories() -> None:
    """Delete all saved memories."""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)


def all_memories() -> list[str]:
    """Return all saved memories."""
    return load_memories()
