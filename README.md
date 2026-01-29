# 🤖 Riri AI – Intelligent Conversational Assistant

Riri AI is a **full-stack conversational AI web application** built with Flask and powered by large language models via OpenRouter. It features **multiple AI personalities**, session-based memory, and a modern, responsive UI.

---

## 🌟 Features

### 🧠 Multi-Personality AI Modes

Riri AI dynamically switches behavior based on user commands:

* **Balanced Mode (Default)**
  Professional, calm, emotionally intelligent responses suitable for productivity, academics, and general assistance.

* **FRIDAY Mode**
  Logical, analytical, and technical AI inspired by Iron Man’s assistant.

Users can activate modes using keywords like:

* `activate friday mode`
* `riri online`

---

### 🔁 Smart Mode Detection

* Automatically detects intent from user messages
* Switches personality instantly without restarting the app

---

### 💾 Session-Based Memory

* Each user receives a unique session ID via cookies
* Conversation history is stored per session
* Includes **reset session** functionality
* Conversations stored in `conversation_history.json`

---

### 🤖 AI Model & API

* Powered by **OpenRouter API**
* Model used: `gryphe/mythomax-l2-13b`
* Secure API key handling using environment variables

---

### 🎨 Frontend & UI

* Responsive HTML & CSS interface
* Custom avatar and branding
* Background video support
* Progressive Web App ready (`manifest.json` included)

---

## 📁 Project Structure

```
Riri_Ai-main/
│── Chatbot.py
│── requirements.txt
│── conversation_history.json
│── static/
│   ├── css/
│   ├── images/
│   └── videos/
│── templates/
│   └── index.html
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SwaritSingh0017/riri-ai.git
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Environment Variables

Create a `.env` or `key.env` file and add:

```
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 4️⃣ Run the Application

```bash
python Chatbot.py
```

The app will start on `http://localhost:5000`

---

## 🚀 Deployment

* Website is Deployed and Live in **https://riri-ai.onrender.com**

* Compatible with **Render**, **Heroku**, and other Flask-friendly platforms
* Environment variables must be set in the hosting dashboard

---

## 🔐 Security

* API keys are never hardcoded
* Session handling via secure cookies
* Error handling for external API calls

---

## 🛠️ Tech Stack

* Python
* Flask
* OpenRouter API (LLM)
* HTML, CSS, JavaScript
* REST APIs

---

## 📌 Use Cases

* Personal AI assistant
* AI chatbot website
* Portfolio & demo project
* Conversational AI experiments

---

## 📄 License

This project is intended for **educational and personal use**.

---

## ❤️ Author

Developed by **[Swarit Singh]**
If you like this project, don’t forget to ⭐ star the repository!
