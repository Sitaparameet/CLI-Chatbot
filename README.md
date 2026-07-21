# CLI Chatbot Using OpenAI API

## 📌 Project Description

This project is a command-line interface (CLI) chatbot built using **Python, LangChain, and OpenAI API**.

The chatbot can maintain conversation history during a single session and supports basic commands to reset the conversation or exit the chatbot.

The project was developed as part of an LLM and Prompt Engineering task.

---

## ✨ Features

* 🤖 Chat with an OpenAI Large Language Model (LLM)
* 🧠 Maintains conversation history during the current session
* 🔄 `/reset` command to clear conversation history
* 🚪 `/exit` command to exit the chatbot session
* 🔐 API key stored securely using environment variables
* ⚠️ Basic API error handling
* 🐍 Python 3.12 environment
* 🔗 Built using LangChain

---

## 🛠️ Technologies Used

* Python 3.12
* LangChain
* LangChain OpenAI
* OpenAI API
* python-dotenv
* uv

---

## 📁 Project Structure

```text
CLI Chatbot/
│
├── .venv/                 # Python virtual environment (not uploaded)
├── .env                   # API key (not uploaded)
├── .gitignore             # Files excluded from Git
├── .python-version        # Python version used by the project
├── main.py                # Main chatbot application
├── pyproject.toml         # Project dependencies and configuration
├── uv.lock                # Locked dependency versions
└── README.md              # Project documentation
```

---

## ⚙️ Requirements

Before running the project, make sure you have:

* Python 3.12
* uv package manager
* An OpenAI API key

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd CLI-Chatbot
```

---

### 2. Create the Virtual Environment

The project uses Python 3.12.

```bash
uv venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\activate
```

---

### 3. Install Dependencies

Install the project dependencies using:

```bash
uv sync
```

Or install the required packages manually:

```bash
uv add langchain langchain-openai python-dotenv
```

---

### 4. Configure the OpenAI API Key

Create a file named:

```text
.env
```

Add your OpenAI API key:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual API key.

⚠️ **Important:** Never upload your `.env` file or expose your API key publicly.

---

## ▶️ Running the Chatbot

Run the chatbot using:

```bash
uv run main.py
```

The chatbot will start in the command line.

Example:

```text
==================================================
        LangChain CLI Chatbot
==================================================

Commands:
/reset - Clear conversation history
/exit  - Exit the chatbot

You:
```

---

## 💬 Example Conversation

```text
You: My name is Meet.

Assistant: Nice to meet you, Meet!

You: What is my name?

Assistant: Your name is Meet.
```

The chatbot remembers previous messages during the current session.

---

## 🔄 Reset Conversation

To clear the conversation history, enter:

```text
/reset
```

Example:

```text
You: /reset

Assistant: Conversation history has been reset.
```

After resetting, previous conversation information is removed.

---

## 🚪 Exit the Chatbot

To exit the current chatbot session, enter:

```text
/exit
```

Example:

```text
You: /exit

Assistant: Goodbye!
```

The chatbot program will terminate, but the terminal itself will remain open.

---

## 🧠 Conversation History

The chatbot maintains conversation history using LangChain message objects.

The conversation follows this flow:

```text
User Message
      ↓
Add to Conversation History
      ↓
Send Conversation History to LLM
      ↓
Receive AI Response
      ↓
Add AI Response to History
      ↓
Display Response
      ↓
Wait for Next User Message
```

This allows the chatbot to remember previous messages during a single session.

---

## ⚠️ Error Handling

The chatbot includes basic error handling for API failures.

If an error occurs while communicating with the OpenAI API, the chatbot displays a fallback message and allows the user to try again.

Example:

```text
Assistant: Sorry, I couldn't process your request. Please try again.
```

---

## 🔐 Security

The OpenAI API key is stored in an environment variable using a `.env` file.

The `.env` file should be included in `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

This prevents the API key from being accidentally committed to GitHub.

---

## 📌 Available Commands

| Command  | Description                             |
| -------- | --------------------------------------- |
| `/reset` | Clears the current conversation history |
| `/exit`  | Exits the chatbot session               |

---

## 🎯 Learning Objectives

This project demonstrates:

* Using an LLM API with Python
* Using LangChain with OpenAI
* Managing conversation history
* Working with environment variables
* Building a command-line chatbot
* Handling API errors
* Using `uv` for Python project and dependency management
* Managing a project using Git and GitHub

---

## 👨‍💻 Author

**Meet**

---

## 📄 License

This project was created for educational and learning purposes.
