import os
from flask import Flask, request, jsonify, session
import google.generativeai as genai
import base64

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY", "william_pro_2026")

# Unganisha na Gemini
genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    image_data = data.get("image") # Hapa ni kwa ajili ya picha
    
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    history = session['chat_history']
    chat_session = model.start_chat(history=history)
    
    # Kama kuna picha na maandishi
    if image_data:
        img_bytes = base64.b64decode(image_data.split(",")[1])
        response = model.generate_content([user_input, {"mime_type": "image/jpeg", "data": img_bytes}])
    else:
        response = chat_session.send_message(user_input)
    
    # Hifadhi kumbukumbu
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [response.text]})
    session['chat_history'] = history
    
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
    
