from langchain_core.caches import RETURN_VAL_TYPE
import json
from pathlib import Path

MEMORY_FILE=Path("data/memory.json")

def load_memories():
    "load all save memory from the JSON File"
    if not MEMORY_FILE.exists():
        return[]
    try:
        with open(MEMORY_FILE,"r",encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError): 
        return[]

def save_memory(memory: str):
    """ Save a new memory to the JSON file"""
    memories= load_memories()

    memory = memory.strip()
    
    if not memory:
     return
    if memory not in memories:
        memories.append(memory)
    MEMORY_FILE.parent.mkdir(parents=True,exist_ok=True)
    with open(MEMORY_FILE,"w",encoding="utf-8") as file:
        json.dump(
            memories,
            file,
            indent=4
        )
def clear_memories():
    """ delete all saved memeories"""
    MEMORY_FILE.parent.mkdir(parents=True,exist_ok=True)
    with open(MEMORY_FILE,"w",encoding="utf-8") as file:
        json.dump([], file, indent=4)

def all_memories():
    "Return all saved memories"
    return load_memories()
