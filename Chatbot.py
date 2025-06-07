from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import google.generativeai as genai
import os
import re
import uuid

# Configure Gemini API key
GOOGLE_GEMINI_API_KEY = "AIzaSyAflqPql1phK0yL929kyK_4IbYg8v-4e08"
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)  # ADD THIS

app.secret_key = str(uuid.uuid4())

# Initialize model
model = genai.GenerativeModel('gemini-1.5-flash')

# Riri response function
def get_riri_response(user_input):
    user_input_lower = user_input.lower()

    # Initialize session memory if not exists
    if "memory" not in session:
        session["memory"] = []

    # Check if user has set a name
    if "my name is" in user_input_lower:
        name = user_input_lower.split("my name is")[-1].strip().split(" ")[0]
        session["user_name"] = name
        return f"Nice to meet you, {name}~ 💖"

    # Basic Q&A overrides
    if any(kw in user_input_lower for kw in ["who are you", "what's your name", "what is your name"]):
        return "I am Riri~ your cute AI 💖"

    if "who am i" in user_input_lower:
        if "user_name" in session:
            return f"You are {session['user_name']}~! 🌸"
        else:
            return "I don't know yet! What's your name? 💕"

    # Default Gemini chat
    try:
        chat = model.start_chat(history=session["memory"])
        response = chat.send_message(user_input)
        session["memory"].append({"role": "user", "parts": [user_input]})
        session["memory"].append({"role": "model", "parts": [response.text]})
        return response.text
    except Exception as e:
        return f"I encountered an error: {e}"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    user_input = request.json.get("message", "")
    bot_response = get_riri_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
