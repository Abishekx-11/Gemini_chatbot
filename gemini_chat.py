
from google import genai
from google.genai import types
from configure import API_KEY

import sys
import time
import json

# --------------------------------------------------
# API CLIENT CONFIGURATION
# --------------------------------------------------
client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------
CHAT_FILE = "chat_history.json"
MAX_RECENT_MESSAGES = 6
SUMMARY_TRIGGER = 10
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# --------------------------------------------------
# SYSTEM BEHAVIOR (HARDCODED AI PERSONALITY)
# --------------------------------------------------
SYSTEM_INSTRUCTION = (
    "You are a helpful, polite, and concise AI assistant. "
    "Explain concepts in simple language. "
    "For technical questions, respond step-by-step. "
    "Do not use emojis. Avoid unnecessary verbosity. "
    "If you do not know something, say so honestly."
)

# --------------------------------------------------
# FILE HANDLING
# --------------------------------------------------
def save_chat(chat_history):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)
    print("[Chat saved successfully]")

def load_chat():
    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --------------------------------------------------
# UI UTILITIES
# --------------------------------------------------
def stream_text(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

# --------------------------------------------------
# CONTEXT BUILDING (IMPORTANT)
# --------------------------------------------------
def build_conversation_text(chat_history):
    """
    Gemini does NOT accept role-based messages.
    We flatten conversation into plain text.
    """
    lines = []
    for msg in chat_history:
        role = msg["role"].capitalize()
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)

# --------------------------------------------------
# CHAT SUMMARIZATION
# --------------------------------------------------
def summarize_chat(chat_history):
    conversation_text = build_conversation_text(chat_history)

    prompt = (
        "Summarize the following conversation briefly. "
        "Preserve important facts and user preferences. "
        "Do not add new information.\n\n"
        + conversation_text
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=120
        )
    )

    return response.text

# --------------------------------------------------
# GEMINI CALL WITH RETRY LOGIC
# --------------------------------------------------
def generate_with_retry(conversation_text):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation_text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.3,
                    max_output_tokens=150
                )
            )
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < MAX_RETRIES:
                    print(f"[Model overloaded — retrying {attempt}/{MAX_RETRIES}]")
                    time.sleep(RETRY_DELAY)
                else:
                    raise RuntimeError(
                        "Gemini free tier is temporarily overloaded.\n"
                        "Please wait and try again later, or upgrade your plan."
                    )
            else:
                raise e

# --------------------------------------------------
# INITIAL SETUP
# --------------------------------------------------
chat_history = load_chat()

print("-" * 50)
print("\t\tSimple AI Chatbot")
print("-" * 50)
print("Commands: 'quit' | 'clear' | 'save'\n")

# --------------------------------------------------
# MAIN CHAT LOOP
# --------------------------------------------------
while True:
    prompt = input("You: ").strip()

    if prompt.lower() == "quit":
        save_chat(chat_history)
        print("Exiting program...")
        sys.exit()

    if prompt == "":
        print("Please type something.")
        continue

    if prompt.lower() == "clear":
        chat_history = []
        print("[Chat history cleared]")
        continue

    if prompt.lower() == "save":
        save_chat(chat_history)
        continue

    try:
        chat_history.append({"role": "user", "content": prompt})

        # Summarize if chat gets too long
        if len(chat_history) > SUMMARY_TRIGGER:
            summary = summarize_chat(chat_history[:-MAX_RECENT_MESSAGES])
            chat_history = (
                [{"role": "system", "content": f"Conversation summary: {summary}"}]
                + chat_history[-MAX_RECENT_MESSAGES:]
            )

        print("AI is thinking", end="", flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print("\n")

        conversation_text = build_conversation_text(chat_history)
        response = generate_with_retry(conversation_text)

        if response.text:
            print("AI: ", end="", flush=True)
            stream_text(response.text)
            chat_history.append(
                {"role": "assistant", "content": response.text}
            )
        else:
            print("[No response generated]")

    except Exception as e:
        save_chat(chat_history)
        print(f"\n{e}\n")
