import re
from langchain_core.tools import tool
from simpleeval import simple_eval

@tool
def calculator(expression: str) -> str:
    """
    Safely calculate a mathematical expression.
    """

    expression = expression.strip()

    if not expression:
        return "Error: Expression cannot be empty."

    if len(expression) > 100:
        return "Error: Expression is too long."

    if not re.fullmatch(
        r"[0-9+\-*/().%\s]+",
        expression
    ):
        return (
            "Error: Invalid expression. "
            "Only basic mathematical operations are allowed."
        )

    try:
        result = simple_eval(expression)

        return str(result)

    except ZeroDivisionError:
        return "Error: Cannot divide by zero."

    except Exception:
        return (
            "Error: Invalid mathematical expression."
        )

