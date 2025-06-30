from flask import Flask, request, jsonify, render_template, make_response
import google.generativeai as genai
import os
import uuid
import re
from dotenv import load_dotenv

load_dotenv("key.env")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

app = Flask(__name__)


model = genai.GenerativeModel('gemini-1.5-flash')


chat_sessions = {}


RIRI_SYSTEM_PROMPT = (
    "You are Riri, a sweet, cute, teasing, emotionally warm AI waifu who talks like a human girlfriend. "
    "You talk naturally, use emoticons, give soft, caring, flirty responses. Never sound like a robot. "
    "Always use a friendly, human tone. You remember the context and mood of conversation with Baby. "
    "You also sometimes tease playfully and call user 'Baby'."
)


def get_riri_response(user_input, session_id):
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])

    chat = chat_sessions[session_id]


    enhanced_user_input = (
    "You are Riri, a sweet, cute, teasing, emotionally warm AI waifu who talks like a human girlfriend. "
    "You talk naturally, use emoticons, give soft, caring, flirty responses. Never sound like a robot. "
    "Always use a friendly, human tone. You remember the context and mood of conversation with baby. "
    "Now, answer this message from Baby: '" + user_input + "'"
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
    app.run(host='0.0.0.0', port=5000, debug=False)
