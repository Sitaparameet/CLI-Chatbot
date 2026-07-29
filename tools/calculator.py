import re
from langchain_core.tools import tool
from simpleeval import simple_eval
from tools.tool_logger import log_tool


@tool
@log_tool
def calculator(expression: str) -> str:
    """Safely calculate a mathematical expression."""
    expression = expression.strip()

    if not expression:
        return "Error: Expression cannot be empty."
    if len(expression) > 50:
        return "Error: Expression is too long."
    if not re.fullmatch(r"[0-9+\-*/().%\s]+", expression):
        return "Error: Invalid expression. Only basic mathematical operations are allowed."

    try:
        return str(simple_eval(expression))
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
    except Exception:
        return "Error: Calculation failed."