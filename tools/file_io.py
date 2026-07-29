from pathlib import Path
from langchain_core.tools import tool
from tools.tool_logger import log_tool

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_ROOT / "data"


@tool
@log_tool
def file_io(operation: str, filename: str, content: str = "") -> str:
    """Read or write a local text file.

    Args:
    If the user asks to create, make, write, or save a document:
    1. If the request requires research, call web_search first.
    2. After receiving the search results, create the document content.
    3. Call file_io with operation='write' to save the document.
    4. Only then provide the final response.

    Returns:
        File content for read operations or a success/error message.
    """
    op = operation.strip().lower()
    fname = filename.strip()

    if op not in ("read", "write"):
        return "Error: Invalid operation. Use 'read' or 'write'."
    if not fname:
        return "Error: Filename cannot be empty."

    file_path = BASE_DIR / fname

    try:
        if op == "write":
            BASE_DIR.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return f"File '{fname}' written successfully."
        else:
            if not file_path.exists():
                return f"Error: File '{fname}' does not exist."
            return file_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"File operation failed: {e}"