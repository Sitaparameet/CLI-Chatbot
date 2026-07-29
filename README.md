# CLI Chatbot Using OpenAI API & LangChain Tools

## 📌 Project Description

This project is a feature-rich Command-Line Interface (CLI) AI agent built using **Python, LangChain, LangGraph, and the OpenAI API**.

Equipped with **Tool Calling** capabilities and an **Automated Persistent Memory System**, the chatbot can interactively answer questions, perform real-time web searches, fetch weather conditions, evaluate math calculations, read/write local files, and remember user details across sessions.

Developed as part of an LLM and Prompt Engineering task.

---

## ✨ Features

* 🤖 **LangGraph AI Agent (`gpt-4o-mini`)**: Powered by LangChain and LangGraph with `MemorySaver` checkpointer for conversation session history.
* 🛠️ **Custom Tool Integration**:
  * 🌐 `web_search`: Real-time web search using Tavily API for current news, recent events, and external facts.
  * 🌤️ `get_weather`: Live weather updates for any city using OpenWeatherMap API.
  * 🧮 `calculator`: Safe mathematical expression solver using Python `ast`.
  * 📁 `file_io`: Read and write text files directly within the project environment.
* 🧠 **Persistent User Memory**: Automatically extracts personal user facts using OpenAI Structured Output (`MemoryDecision` model) and persists them in `data/memory.json` across sessions.
* 🪵 **Tool Call Execution Logging**: Decorator-based logging (`tool_logger.py`) that records tool calls, inputs, outputs, and timestamps in `logs/tool_calls.log`.
* 📅 **Dynamic Context & System Prompt**: Automatically injects today's date and stored user memories into the system prompt.
* 💬 **Interactive CLI Commands**:
  * `/reset`: Start a fresh conversation session thread.
  * `/memories`: View all saved user memories.
  * `/clear-memories`: Delete all stored memories and reset conversation.
  * `/exit`: Safely exit the chatbot.
* 🔐 **Secure Key Management**: Environment variables managed via `.env` with character length limits and error fallback handling.

---

## 🛠️ Technologies Used

* **Python 3.12**
* **LangChain & LangGraph** (`create_agent`, `MemorySaver`)
* **OpenAI API** (`gpt-4o-mini`, Structured Outputs)
* **Tavily API** (`tavily-python`) for web search
* **OpenWeatherMap API** for weather data
* **Pydantic** for structured memory models
* **python-dotenv** & **uv** package manager

---

## 📁 Project Structure

```text
CLI Chatbot/
│
├── data/                  # Persistent storage directory
│   └── memory.json        # Saved persistent user memories
├── logs/                  # Application logs
│   └── tool_calls.log     # Detailed logs of tool executions
├── memory/                # Memory decision and storage modules
│   ├── cli_memory.py      # CLI handlers for memory commands
│   ├── memory_decision.py # Structured output memory classifier
│   └── memory_store.py    # Memory persistence functions
├── tools/                 # Agent custom tools
│   ├── calculator.py      # Safe AST mathematical calculator tool
│   ├── file_io.py         # File read/write tool
│   ├── tool_logger.py     # Execution logger decorator for tools
│   ├── weather.py         # OpenWeatherMap API weather tool
│   └── web_search.py      # Tavily web search tool
├── .env                   # API keys and environment configuration
├── .gitignore             # Git exclusions
├── main.py                # CLI Chatbot entry point & agent loop
├── structured_output.py   # Memory decision Pydantic models
├── pyproject.toml         # Dependencies and project configuration
├── uv.lock                # Locked dependency versions
└── README.md              # Project documentation
```

---

## ⚙️ Requirements

Before running the project, make sure you have:

* Python 3.12
* `uv` package manager installed
* OpenAI API Key (`OPENAI_API_KEY`)
* Tavily API Key (`TAVILY_API_KEY`) for web search
* OpenWeatherMap API Key (`OPENWEATHER_API_KEY`, optional for weather tool)

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CLI-Chatbot
```

---

### 2. Create and Activate Virtual Environment

```bash
uv venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

Activate on macOS / Linux:

```bash
source .venv/bin/activate
```

---

### 3. Install Dependencies

Install dependencies using `uv`:

```bash
uv sync
```

Or manually install:

```bash
uv add langchain langchain-openai langgraph tavily-python python-dotenv requests pydantic
```

---

### 4. Configure API Keys

Create a `.env` file in the root directory:

```text
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

⚠️ **Important:** Never commit your `.env` file to version control.

---

## ▶️ Running the Chatbot

Start the chatbot CLI:

```bash
uv run main.py
```

Sample CLI Startup Display:

```text
==================================================
        CLI Chatbot
==================================================

Available Commands:
/reset          - Clear conversation history
/memories       - View saved memories
/clear-memories - Clear saved memories
/exit           - Exit chatbot

You can ask questions like:
- What is 25 * 4?
- What is the weather in Ahmedabad?
- What is the latest news about AI?
- Create a file named notes.txt with hello world
```

---

## 🧰 Available Tools & Capabilities

The agent automatically invokes the appropriate tool based on user intent:

| Tool | Functionality | Example Prompt |
| --- | --- | --- |
| 🌐 `web_search` | Real-time web search via Tavily API for current news, facts, and updates | *"What is the latest news about space exploration?"* |
| 🌤️ `get_weather` | Fetches live weather report (temp, humidity, description) for a city | *"What's the weather in Tokyo right now?"* |
| 🧮 `calculator` | Evaluates math expressions (`+`, `-`, `*`, `/`, `**`, `%`) safely | *"Calculate (350 * 12) / 4"* |
| 📁 `file_io` | Reads from or writes to local text files inside workspace | *"Write 'Project complete' into status.txt"* |

All tool calls are logged with execution metrics in `logs/tool_calls.log`.

---

## 📌 Interactive CLI Commands

| Command | Description |
| --- | --- |
| `/reset` | Resets current conversation thread history (starts a new thread ID) |
| `/memories` | Displays all saved persistent user memories |
| `/clear-memories` | Deletes all saved user memories and resets conversation |
| `/exit` | Exits the chatbot session |

---

## 🧠 Persistent User Memory System

The chatbot incorporates a **Memory-Write Decision Logic** using OpenAI Structured Outputs (`gpt-4o-mini` with Pydantic):

1. **Extraction**: When you send a message (e.g., *"My name is Meet and I love playing cricket"*), `should_remember()` analyzes the message.
2. **Decision**: Useful, personal facts generate a `MemoryDecision(should_remember=True, memory="User's name is Meet. User loves playing cricket.")`. Temporary queries (*"What is 2 + 2?"*) are ignored.
3. **Storage**: Approved memories are persisted in `data/memory.json`.
4. **Recall**: On future turns and session restarts, stored memories are automatically formatted into the agent's System Prompt.

---

## 💬 Example Usage Scenarios

### Tool Invocation Example (Web Search & Calculator)

```text
You: What is the current news about space exploration?
Assistant: NASA recently announced progress on the Artemis mission...

You: What is 125 * 8?
Assistant: 125 * 8 = 1000
```

### Memory Retention Across Sessions

```text
Session 1:
You: I live in Toronto and work as a software engineer.
[Memory Saved: User lives in Toronto. User works as a software engineer.]

Session 2 (after restart):
You: Where do I live and what is my job?
Assistant: You live in Toronto and work as a software engineer!
```

---

## ⚠️ Error Handling & Security

* **API Keys**: Stored safely in environment variables using `.env`.
* **Input Limits**: Messages over 2000 characters are rejected to prevent context bloat.
* **Tool Safety**: Math calculator uses restricted AST parsing rather than unsafe `eval()`.
* **Robust Fallbacks**: Catches API timeouts, network failures, and tool errors gracefully.

---

## 🎯 Learning Objectives & Highlights

* Building an autonomous **LangGraph Agent** with tool calling capabilities.
* Integrating custom tools (`web_search`, `get_weather`, `calculator`, `file_io`).
* Implementing **Structured Output** for automated memory decision classification.
* Creating persistent memory management systems (`data/memory.json`).
* Decorator pattern for tool execution logging (`logs/tool_calls.log`).
* Clean CLI interface with session state management using `uv`.

---

## 👨‍💻 Author

**Meet**

---

## 📄 License

This project was created for educational and learning purposes.
