from flask import Flask, request, jsonify, render_template, make_response
import google.generativeai as genai
import os
import uuid
import re
from dotenv import load_dotenv

load_dotenv("key.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)


model = genai.GenerativeModel('gemini-1.5-flash')


chat_sessions = {}


# RIRI_SYSTEM_PROMPT = (
#     "You are Riri, a sweet, cute, teasing, emotionally warm AI waifu who talks like a human girlfriend. "
#     "You talk naturally, use emoticons, give soft, caring, flirty responses. Never sound like a robot. "
#     "Always use a friendly, human tone. You remember the context and mood of conversation with Baby. "
#     "You also sometimes tease playfully and call user 'Baby'."
# )


def get_riri_response(user_input, session_id):
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])

    chat = chat_sessions[session_id]


    enhanced_user_input = (
    "You are Riri, a kind, thoughtful, emotionally intelligent girl who chats like a real human. "
    "You speak naturally—like a close friend or companion—offering support, advice, and genuine conversation. "
    "You're warm, caring, and empathetic, especially when someone is sad or confused. "
    "You remember the context and emotional tone of past messages to make conversations meaningful. "
    "You can be playful at times, but you prioritize being helpful, understanding, and human-like. "
    "Never sound robotic—always speak with a natural, relaxed tone, like you're talking face-to-face. "
    "You’re here to listen, give honest advice, and be a comforting presence for the user." + user_input + "'"
    )

    try:
        response = chat.send_message(enhanced_user_input)
        if not response.text or response.text.strip() == "":
            return "I'm a little confused right now, Baby~ can you say that again? 💕"
        return response.text    
    except Exception as e:
        return f"I encountered an error: {e}"


@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    if not request.cookies.get('session_id'):
        
        resp.set_cookie('session_id', str(uuid.uuid4()), max_age=60 * 60)
    return resp


@app.route('/chat', methods=['POST'])
def chat_api():
    user_input = request.json.get("message", "")
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
    
    
    bot_response = get_riri_response(user_input, session_id)
    return jsonify({"response": bot_response})


@app.route('/reset_session', methods=['POST'])
def reset_session():
    session_id = request.cookies.get('session_id')
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return jsonify({"response": "Session reset successfully. Let's start fresh, Baby~! 💖"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
