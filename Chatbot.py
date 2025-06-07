from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import re
import os

# Configure Gemini API key
GOOGLE_GEMINI_API_KEY = "AIzaSyAflqPql1phK0yL929kyK_4IbYg8v-4e08"
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

app = Flask(__name__)

# Riri response function
def get_riri_response(user_input, chat_history):
    try:
        # convert history to gemini format
        gemini_chat_history = []
        for turn in chat_history:
            if turn["role"] == "user":
                gemini_chat_history.append({"role": "user", "parts": [turn["message"]]})
            elif turn["role"] == "bot":
                gemini_chat_history.append({"role": "model", "parts": [turn["message"]]})

        # start chat with current history
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=gemini_chat_history)

        # send new user message
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"I encountered an error: {e}. I might not be able to answer that right now."


def get_riri_response(user_input, session_id):

    user_input = user_input.lower()
    words = re.findall(r'\b\w+\b', user_input)

    # Name / identity questions
    if any(phrase in user_input for phrase in [
        "who are you", "what is your name", "your name", "tell me your name", "who r u", "whats your name", "what's your name"
    ]):
        return "I am Riri, your cute AI waifu~ 💕"

    # Other simple responses
    if "exit" in words or "no thank you" in user_input:
        return "Goodbye!"
    elif "hello" in words or "hi" in words:
        return "Hello there! How can I help you?"
    elif "how" in words and "are" in words and "you" in words:
        return "I'm just a program, but I'm doing great! Thanks for asking."

    # Default Gemini response
    else:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')  # create new model instance
            chat = model.start_chat()                          # temporary chat
            response = chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"I encountered an error: {e}. I might not be able to answer that right now."



# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    user_input = request.json.get("message", "")
    chat_history = request.json.get("history", [])

    bot_response = get_riri_response(user_input, chat_history)

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
