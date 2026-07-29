from pathlib import Path
from datetime import datetime
from functools import wraps

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "logs" / "tool_calls.log"


def log_tool_call(tool_name: str, arguments: any, result: str):
    """Log tool calls and their results."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"{'=' * 60}\n"
            f"Timestamp: {datetime.now()}\n"
            f"Tool: {tool_name}\n"
            f"Arguments: {arguments}\n"
            f"Result: {result}\n"
            f"{'=' * 60}\n"
        )


def log_tool(func):
    """Decorator to automatically log tool calls and results."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if kwargs:
            arg_val = kwargs if len(kwargs) > 1 else list(kwargs.values())[0]
        elif args:
            arg_val = args[0]
        else:
            arg_val = ""
        log_tool_call(func.__name__, arg_val, res)
        return res
    return wrapper