from flask import Flask, request, jsonify, render_template, make_response
import google.generativeai as genai
import os
import re
import uuid

# Configure Gemini API key
GOOGLE_GEMINI_API_KEY = "AIzaSyAflqPql1phK0yL929kyK_4IbYg8v-4e08"
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

app = Flask(__name__)

# Initialize model and chat with no memory (temporary)
model = genai.GenerativeModel('gemini-1.5-flash')

# 🧠 this will store chat history per session temporarily (not across tab refresh)
chat_sessions = {}

def get_riri_response(user_input, session_id):
    user_input = user_input.lower()
    words = re.findall(r'\b\w+\b', user_input)

    # 🩷 Custom replies
    if any(phrase in user_input for phrase in [
        "who are you", "what is your name", "your name", "tell me your name", "who r u", "whats your name", "what's your name"
    ]):
        return "I am Riri, your cute Virtual Assistant~ 💕"

    elif "exit" in words or "no thank you" in user_input:
        return "Goodbye!"
    elif "hello" in words or "hi" in words:
        return "Hello there! How can I help you?"
    elif "how" in words and "are" in words and "you" in words:
        return "I'm just a program, but I'm doing great! Thanks for asking."

    # 🌸 Handle per-session temporary chat
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])
    chat = chat_sessions[session_id]

    try:
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"I encountered an error: {e}"

# Routes
@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    if not request.cookies.get('session_id'):
        resp.set_cookie('session_id', str(uuid.uuid4()))
    return resp

@app.route('/chat', methods=['POST'])
def chat_api():
    user_input = request.json.get("message", "")
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
    bot_response = get_riri_response(user_input, session_id)
    return jsonify({"response": bot_response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
