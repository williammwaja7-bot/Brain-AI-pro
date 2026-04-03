import os
import warnings
import requests
import base64
import io
import json
import re
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, session

# ==================== KANZU YA MAONYO ====================
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Jaribu kuimport google.generativeai
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Gemini haipo. Endesha: pip install google-generativeai")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "brain-ai-pro-secret-key-2024")

# ==================== API KEYS ====================
GEMINI_KEY = os.environ.get("GEMINI_KEY")
GROQ_KEY = os.environ.get("GROQ_KEY")

if GEMINI_KEY and GEMINI_AVAILABLE:
    genai.configure(api_key=GEMINI_KEY)
    print("✅ Gemini imesanidiwa!")

# ==================== MEMORY YA MAZUNGUMZO ====================
def get_conversation_history():
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    return session['conversation_history']

def add_to_history(role, content):
    history = get_conversation_history()
    history.append({"role": role, "content": content, "timestamp": datetime.now().isoformat()})
    if len(history) > 30:
        history = history[-30:]
    session['conversation_history'] = history

# ==================== LUGHA ====================
LANGUAGES = {
    "sw": {"name": "Kiswahili", "code": "sw-TZ", "flag": "🇹🇿"},
    "en": {"name": "English", "code": "en-US", "flag": "🇺🇸"},
    "fr": {"name": "Français", "code": "fr-FR", "flag": "🇫🇷"},
    "ar": {"name": "العربية", "code": "ar-SA", "flag": "🇸🇦"},
    "es": {"name": "Español", "code": "es-ES", "flag": "🇪🇸"},
    "de": {"name": "Deutsch", "code": "de-DE", "flag": "🇩🇪"},
    "zh": {"name": "中文", "code": "zh-CN", "flag": "🇨🇳"}
}

# ==================== CALCULATOR ====================
def calculate_expression(expression):
    try:
        expression = expression.replace(" ", "")
        calc_patterns = [
            r'hesabu\s+(.+)',
            r'calc\s+(.+)',
            r'([\d\s\+\-\*\/\%\(\)\.]+)'
        ]
        
        math_expr = None
        for pattern in calc_patterns:
            match = re.search(pattern, expression, re.IGNORECASE)
            if match:
                math_expr = match.group(1)
                break
        
        if not math_expr:
            return None
        
        math_expr = math_expr.replace('^', '**')
        
        allowed_chars = set('0123456789+-*/().% ')
        if not all(c in allowed_chars for c in math_expr):
            return "⚠️ Tafadhali tumia namba na + - * / % ( ) tu."
        
        result = eval(math_expr, {"__builtins__": {}}, {})
        
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 6)
        
        return f"📊 **Matokeo:** `{math_expr} = {result}`"
        
    except ZeroDivisionError:
        return "⚠️ Mgawanyiko kwa sifuri hairuhusiwi!"
    except Exception:
        return None

# ==================== GROQ PROCESSING ====================
def process_with_groq(user_message, conversation_history, lang="sw"):
    if not GROQ_KEY:
        return None
    
    try:
        system_prompt = f"""Wewe ni Brain AI Pro. Jibu kwa {LANGUAGES.get(lang, LANGUAGES['sw'])['name']} tu.
        Kuwa mkarimu, msaada, na jibu kwa ufasaha."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in conversation_history[-10:]:
            if msg.get('role') in ['user', 'assistant']:
                messages.append({"role": msg['role'], "content": msg.get('content', '')[:500]})
        
        messages.append({"role": "user", "content": user_message})
        
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"⚠️ Hitilafu ya API: {response.status_code}"
            
    except Exception as e:
        return f"🚨 Hitilafu: {str(e)}"

# ==================== HTML CODE (SIMPLE) ====================
HTML_CODE = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brain AI Pro</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #f0f2f5;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #10b981;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .lang-selector {
            display: flex;
            gap: 5px;
            padding: 10px;
            background: white;
            flex-wrap: wrap;
            justify-content: center;
        }
        .lang-btn {
            padding: 5px 10px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            background: #e5e7eb;
        }
        .lang-btn.active {
            background: #10b981;
            color: white;
        }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .msg {
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 20px;
            word-wrap: break-word;
        }
        .user-msg {
            align-self: flex-end;
            background: #10b981;
            color: white;
        }
        .ai-msg {
            align-self: flex-start;
            background: white;
            color: #333;
        }
        .input-area {
            padding: 15px;
            background: white;
            border-top: 1px solid #ddd;
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
        }
        .input-area button {
            padding: 10px 20px;
            background: #10b981;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
        }
        .loading {
            text-align: center;
            padding: 10px;
            color: #888;
        }
        @media (max-width: 768px) {
            .msg { max-width: 90%; }
        }
    </style>
</head>
<body>
    <div class="header">
        🧠 Brain AI Pro - William Richard
    </div>
    
    <div class="lang-selector" id="langSelector">
        <button class="lang-btn active" data-lang="sw" onclick="changeLang('sw')">🇹🇿 Kiswahili</button>
        <button class="lang-btn" data-lang="en" onclick="changeLang('en')">🇺🇸 English</button>
        <button class="lang-btn" data-lang="fr" onclick="changeLang('fr')">🇫🇷 Français</button>
        <button class="lang-btn" data-lang="ar" onclick="changeLang('ar')">🇸🇦 العربية</button>
        <button class="lang-btn" data-lang="es" onclick="changeLang('es')">🇪🇸 Español</button>
        <button class="lang-btn" data-lang="de" onclick="changeLang('de')">🇩🇪 Deutsch</button>
        <button class="lang-btn" data-lang="zh" onclick="changeLang('zh')">🇨🇳 中文</button>
    </div>
    
    <div class="chat-container" id="chatContainer">
        <div class="msg ai-msg">👋 Habari! Mimi ni Brain AI Pro. Uliza swali lolote!</div>
    </div>
    
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Andika swali lako hapa..." onkeypress="if(event.keyCode==13) sendMessage()">
        <button onclick="sendMessage()">📤 Tuma</button>
    </div>
    
    <script>
        let currentLang = localStorage.getItem('selectedLang') || 'sw';
        
        function changeLang(lang) {
            currentLang = lang;
            localStorage.setItem('selectedLang', lang);
            document.querySelectorAll('.lang-btn').forEach(btn => {
                if(btn.dataset.lang === lang) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }
        
        async function sendMessage() {
            let input = document.getElementById('userInput');
            let message = input.value.trim();
            if(!message) return;
            
            let container = document.getElementById('chatContainer');
            
            // Add user message
            container.innerHTML += `<div class="msg user-msg">${escapeHtml(message)}</div>`;
            input.value = "";
            scrollToBottom();
            
            // Add loading indicator
            let loadingId = 'loading-' + Date.now();
            container.innerHTML += `<div class="msg ai-msg" id="${loadingId}"><span class="loading">🤔 Brain AI inafikiria...</span></div>`;
            scrollToBottom();
            
            try {
                let response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: message, lang: currentLang })
                });
                
                let data = await response.json();
                
                // Remove loading indicator
                document.getElementById(loadingId).remove();
                
                // Add AI response
                container.innerHTML += `<div class="msg ai-msg">${marked.parse(data.response)}</div>`;
                scrollToBottom();
                
            } catch(error) {
                document.getElementById(loadingId).remove();
                container.innerHTML += `<div class="msg ai-msg">❌ Hitilafu: ${error.message}</div>`;
                scrollToBottom();
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function scrollToBottom() {
            const container = document.getElementById('chatContainer');
            container.scrollTop = container.scrollHeight;
        }
        
        // Load marked.js
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
        document.head.appendChild(script);
        
        // Set initial active language
        changeLang(currentLang);
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '').lower().strip()
    lang = data.get('lang', 'sw')
    
    # Check for calculator
    calc_result = calculate_expression(message)
    if calc_result:
        add_to_history("user", message)
        add_to_history("assistant", calc_result)
        return jsonify({'response': calc_result})
    
    # Process with Groq
    conversation_history = get_conversation_history()
    response = process_with_groq(message, conversation_history, lang)
    
    if response:
        add_to_history("user", message)
        add_to_history("assistant", response)
        return jsonify({'response': response})
    
    return jsonify({'response': '🔴 Samahani, kuna tatizo la API. Hakikisha GROQ_KEY imewekwa kwenye environment variables.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
