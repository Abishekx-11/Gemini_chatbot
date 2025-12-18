# Simple Gemini AI Chatbot (Python)

A command-line AI chatbot built using Google's Gemini API. This project demonstrates how to integrate an AI model into a Python application with controlled behavior, conversation memory, token optimization, and defensive error handling.

---

## 🌟 Features

- ✅ Command-line chat interface
- ✅ Hardcoded AI behavior using system instructions
- ✅ Conversation memory with automatic summarization
- ✅ Streaming (typing-style) AI responses
- ✅ Retry logic for temporary API overloads (503 errors)
- ✅ Save and load chat history (JSON)
- ✅ Graceful handling of free-tier limitations

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Google Gemini API** (`google-genai`)
- **JSON** for chat persistence

---

## 📁 Project Structure
```
project_folder/
├── gemini_chat.py       # Main chatbot script
├── configure.py         # API key configuration
├── chat_history.json    # Saved conversations (auto-generated)
└── README.md            # Project documentation
```

---

## 🔑 How to Get a Free Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **"Get API Key"**
4. Copy your API key

---

## ⚙️ API Key Setup

Create a file named `configure.py` in the project root directory:
```python
API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
```


---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install google-genai   
```
or 
```bash
python -m pip install google-genai   
```

### 2. Run the Chatbot
```bash
python gemini_chat.py
```

---

## 💬 Commands

| Command | Description |
|---------|-------------|
| `quit` | Exit the program and save chat history |
| `save` | Save chat history manually |
| `clear` | Clear current chat session |

---

## 🎭 Customizing AI Behavior (Hardcoded Roles)

The chatbot uses a **system instruction** to control how the AI behaves.

### How to Change AI's Role:

1. Open `gemini_chat.py`
2. Locate the `SYSTEM_INSTRUCTION` variable
3. Replace its content with your desired behavior
4. Save the file and rerun the program

### Example: Math Tutor
```python
SYSTEM_INSTRUCTION = (
    "You are a patient math tutor. "
    "Explain concepts step-by-step with examples. "
    "Use simple language."
)
```

### Example: Programming Tutor
```python
SYSTEM_INSTRUCTION = (
    "You are a programming tutor. "
    "Explain code clearly and provide short examples. "
    "Focus on Python best practices."
)
```

### Example: Casual Friend
```python
SYSTEM_INSTRUCTION = (
    "You are a friendly and supportive companion. "
    "Be casual, empathetic, and conversational."
)
```

---

## 📚 What I Learned

- ✅ Integrating Gemini API into a Python application
- ✅ Controlling AI behavior using system instructions
- ✅ Implementing conversation memory and summarization
- ✅ Handling temporary API overloads gracefully (503 errors)
- ✅ Writing defensive, production-aware code
- ✅ Building retry logic for unreliable APIs
- ✅ JSON-based data persistence
- ✅ Creating interactive CLI applications

---

## 🎯 Use Cases

- 📖 Learning AI API integration
- 🤖 CLI-based AI assistants
- 🎓 Educational tutoring tools
- 🧪 Prompt and behavior experimentation
- 💼 Personal productivity assistants

---

## ⚠️ Limitations

- No long-term memory beyond saved sessions
- Free-tier API availability depends on server load
- CLI-based interface only (no GUI)
- Conversation summarization triggers after 10+ messages
- Limited to Gemini API capabilities and quotas

---
## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

---

## 🙏 Acknowledgments

- Google Gemini API for providing free-tier access
- Python community for excellent libraries

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
