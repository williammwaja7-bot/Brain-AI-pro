# ==============================================================================
# PROJECT: BRAIN AI PRO - THE ULTIMATE MONSTER EDITION (V16)
# DEVELOPER: WILLIAM RICHARD MATHAYO (ICOT STUDENT & TECHNICIAN)
# LOCATION: DAR ES SALAAM, TANZANIA
# PURPOSE: ADVANCED AI ASSISTANT FOR AUTO-ELECTRIC & PROGRAMMING
# ==============================================================================
# HII KODI IMEANDALIWA KWA AJILI YA WILLIAM PEKEE. USIPUNGUZE MSTARI HATA MMOJA.
# INAJUMUISHA: AI CHAT, IMAGE ANALYZER, IMAGE GENERATOR, CALCULATOR, 
# ARCHIVE SYSTEM, VOICE RECOGNITION, NA UI YA KISASA ZAIDI.
# ==============================================================================

import os
import io
import json
import time
import base64
import requests
import warnings
import datetime
from flask import Flask, render_template_string, request, jsonify
from PIL import Image
import google.generativeai as genai

# Kuzima maonyo yasiyo na lazima kule Render
warnings.filterwarnings("ignore")

# Kuanzisha Flask App
app = Flask(__name__)

# ==============================================================================
# SEHEMU YA MAUJANJA YA API (CONFIGURATION SECTION)
# ==============================================================================
# Hakikisha hizi Keys zipo kwenye Environment Variables za Render
GEMINI_API_KEY = os.environ.get("GEMINI_KEY")
GROQ_API_KEY = os.environ.get("GROQ_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_KEY")

# Configuration ya Google Gemini kwa ajili ya Vision (Picha)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(">>> Gemini Engine Status: ACTIVE")
else:
    print(">>> Gemini Engine Status: MISSING KEY")

# ==============================================================================
# LOGIC ZA NDANI (BACKEND FUNCTIONS)
# ==============================================================================

def get_current_timestamp():
    """Inarudisha muda kamili wa sasa wa Tanzania"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def process_vision_ai(user_prompt, base64_image):
    """
    Kazi: Kuchambua picha inayotumwa na William.
    Inatumia Gemini-1.5-Flash kwa ufanisi wa haraka.
    """
    try:
        vision_model = genai.GenerativeModel('gemini-1.5-flash')
        decoded_image = base64.b64decode(base64_image)
        img_buffer = Image.open(io.BytesIO(decoded_image))
        
        system_instruction = (
            "Wewe ni Brain AI Pro, msaidizi mwerevu wa William Richard. "
            "Chambua picha hii kwa kina na utoe maelezo kwa Kiswahili fasaha. "
            f"Prompt ya mtumiaji: {user_prompt if user_prompt else 'Nieleze picha hii'}"
        )
        
        response = vision_model.generate_content([system_instruction, img_buffer])
        return response.text
    except Exception as error:
        return f"Oooh William! Kuna hitilafu kwenye Vision Engine: {str(error)}"

def trigger_dalle_generation(prompt_text):
    """
    Kazi: Kutengeneza picha mpya kabisa (Text-to-Image).
    Inatumia OpenAI DALL-E 3 Model.
    """
    try:
        api_url = "https://api.openai.com/v1/images/generations"
        auth_header = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data_payload = {
            "model": "dall-e-3",
            "prompt": prompt_text,
            "n": 1,
            "size": "1024x1024"
        }
        api_res = requests.post(api_url, headers=auth_header, json=data_payload, timeout=40)
        return api_res.json()['data'][0]['url']
    except Exception:
        return "https://via.placeholder.com/500?text=Sanidi+OpenAI+Key+Kwanza"

# ==============================================================================
# FRONT-END SECTION (HTML, CSS, JAVASCRIPT) - THE MONSTER UI
# ==============================================================================
# Hapa ndipo kodi ilipo ndefu zaidi ili kurembesha mfumo wako.
# ==============================================================================

MONSTER_HTML = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Brain AI Pro - William Richard Edition</title>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

    <style>
        /* CSS RESET & VARIABLES */
        :root {
            --whatsapp-green: #075e54;
            --light-green: #2ecc71;
            --user-bg: #dcf8c6;
            --ai-bg: #ffffff;
            --body-bg: #f0f2f5;
            --dark-text: #1c1e21;
            --border-color: #ced4da;
            --sidebar-width: 300px;
            --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body.dark-mode {
            --body-bg: #0b141a;
            --ai-bg: #202c33;
            --user-bg: #005c4b;
            --dark-text: #e9edef;
            --border-color: #222d34;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--body-bg);
            color: var(--dark-text);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: background 0.5s;
        }

        /* NAVIGATION BAR */
        .navbar {
            height: 70px;
            background: var(--ai-bg);
            border-bottom: 4px solid var(--light-green);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .navbar .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .navbar h1 {
            font-size: 22px;
            font-weight: 800;
            color: var(--whatsapp-green);
            letter-spacing: -0.5px;
        }

        .nav-icons {
            display: flex;
            gap: 20px;
            font-size: 22px;
            color: var(--whatsapp-green);
        }

        .nav-icons i { cursor: pointer; transition: 0.2s; }
        .nav-icons i:active { transform: scale(0.8); }

        /* SIDEBAR / HISTORY SYSTEM */
        .sidebar {
            position: fixed;
            left: calc(-1 * var(--sidebar-width));
            top: 0;
            width: var(--sidebar-width);
            height: 100%;
            background: var(--ai-bg);
            z-index: 2000;
            transition: var(--transition);
            box-shadow: 5px 0 20px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
        }

        .sidebar.active { left: 0; }

        .sidebar-header {
            padding: 40px 20px 20px;
            background: var(--whatsapp-green);
            color: white;
        }

        .history-container {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .history-card {
            padding: 15px;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            border-radius: 8px;
            margin-bottom: 5px;
            transition: 0.2s;
        }

        .history-card:hover { background: var(--body-bg); }

        /* CHAT WINDOW */
        #chat-scroller {
            flex: 1;
            margin-top: 70px;
            margin-bottom: 90px;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            scroll-behavior: smooth;
        }

        .chat-row {
            display: flex;
            width: 100%;
            animation: slideUp 0.4s ease;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .bubble {
            max-width: 85%;
            padding: 14px 18px;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.6;
            position: relative;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .user-bubble {
            background: var(--user-bubble);
            margin-left: auto;
            border-bottom-right-radius: 4px;
            color: #000;
        }

        .ai-bubble {
            background: var(--ai-bg);
            margin-right: auto;
            border-bottom-left-radius: 4px;
            border-left: 6px solid var(--light-green);
        }

        /* CODE BLOCK STYLING */
        pre {
            background: #1e1e1e !important;
            margin: 15px 0;
            padding: 15px;
            border-radius: 12px;
            overflow-x: auto;
            position: relative;
        }

        code { font-family: 'JetBrains Mono', monospace; font-size: 14px; }

        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255,255,255,0.1);
            border: 1px solid var(--light-green);
            color: var(--light-green);
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
        }

        /* INPUT AREA AREA - FIXED SEND BUTTON UI */
        .footer-input {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 15px;
            background: var(--ai-bg);
            border-top: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding-bottom: calc(15px + env(safe-area-inset-bottom));
        }

        .input-container {
            width: 100%;
            max-width: 800px;
            background: var(--body-bg);
            border-radius: 30px;
            padding: 5px 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            border: 1px solid var(--border-color);
        }

        input[type="text"] {
            flex: 1;
            border: none;
            outline: none;
            background: transparent;
            padding: 12px 5px;
            font-size: 16px;
            color: var(--dark-text);
        }

        .action-icons {
            display: flex;
            gap: 15px;
            font-size: 22px;
            color: var(--whatsapp-green);
        }

        #send-trigger {
            font-size: 28px;
            color: var(--light-green);
            cursor: pointer;
            padding: 5px;
            margin-left: 5px;
        }

        /* FLOATING CALCULATOR */
        #calc-ui {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            width: 300px;
            background: var(--ai-bg);
            border-radius: 20px;
            padding: 20px;
            z-index: 3000;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            transition: 0.3s;
        }

        #calc-ui.show { transform: translate(-50%, -50%) scale(1); }

        .calc-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 15px;
        }

        .calc-btn {
            padding: 15px;
            background: var(--body-bg);
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
        }

        .calc-btn.op { background: var(--light-green); color: white; }

        /* WELCOME SCREEN */
        #welcome-hero {
            text-align: center;
            padding: 60px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .hero-icon {
            width: 100px;
            height: 100px;
            background: var(--whatsapp-green);
            color: white;
            border-radius: 30%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 50px;
            margin-bottom: 20px;
            box-shadow: 0 10px 20px rgba(7, 94, 84, 0.3);
        }

        /* TYPING ANIMATION */
        .typing-dots {
            display: none;
            padding: 15px;
            color: var(--light-green);
            font-weight: bold;
            font-style: italic;
        }

    </style>
</head>
<body>

    <div id="overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1500;" onclick="closeAll()"></div>

    <div id="sidebar" class="sidebar">
        <div class="sidebar-header">
            <h2>Brain Archive</h2>
            <p>William Richard Mathayo</p>
        </div>
        <div class="history-container" id="history-box">
            </div>
        <div style="padding:20px;">
            <button onclick="clearHistory()" style="width:100%; padding:12px; background:#ff4757; border:none; color:white; border-radius:10px; font-weight:bold;">
                <i class="fas fa-trash"></i> Futa Data Zote
            </button>
        </div>
    </div>

    <div id="calc-ui">
        <h3 style="text-align:center;">Quick Calc</h3>
        <input type="text" id="calc-display" readonly style="width:100%; padding:15px; margin-top:10px; border:none; background:#eee; border-radius:10px; text-align:right; font-size:24px;">
        <div class="calc-grid">
            <button class="calc-btn" onclick="calcInput('7')">7</button>
            <button class="calc-btn" onclick="calcInput('8')">8</button>
            <button class="calc-btn" onclick="calcInput('9')">9</button>
            <button class="calc-btn op" onclick="calcInput('/')">/</button>
            <button class="calc-btn" onclick="calcInput('4')">4</button>
            <button class="calc-btn" onclick="calcInput('5')">5</button>
            <button class="calc-btn" onclick="calcInput('6')">6</button>
            <button class="calc-btn op" onclick="calcInput('*')">*</button>
            <button class="calc-btn" onclick="calcInput('1')">1</button>
            <button class="calc-btn" onclick="calcInput('2')">2</button>
            <button class="calc-btn" onclick="calcInput('3')">3</button>
            <button class="calc-btn op" onclick="calcInput('-')">-</button>
            <button class="calc-btn" onclick="calcClear()" style="background:#ff4757; color:white;">C</button>
            <button class="calc-btn" onclick="calcInput('0')">0</button>
            <button class="calc-btn" onclick="calcSolve()" style="background:var(--light-green); color:white;">=</button>
            <button class="calc-btn op" onclick="calcInput('+')">+</button>
        </div>
        <button onclick="toggleCalc()" style="width:100%; margin-top:15px; padding:10px; border:none; border-radius:10px;">Funga</button>
    </div>

    <div class="navbar">
        <div class="brand">
            <i class="fas fa-bars" onclick="toggleSidebar()" style="font-size:24px; cursor:pointer;"></i>
            <h1>Brain AI Pro</h1>
        </div>
        <div class="nav-icons">
            <i class="fas fa-calculator" onclick="toggleCalc()"></i>
            <i class="fas fa-moon" onclick="toggleDarkMode()"></i>
            <i class="fas fa-save" onclick="manualSave()"></i>
        </div>
    </div>

    <div id="chat-scroller">
        <div id="welcome-hero">
            <div class="hero-icon">
                <i class="fas fa-bolt"></i>
            </div>
            <h2 style="font-size: 28px;">Habari, William Richard!</h2>
            <p style="opacity: 0.7; margin-top: 10px;">Mfumo wako wa AI uko tayari. Uliza chochote kuhusu Auto-Electric, Programming, au tengeneza picha.</p>
            
            <div style="display:flex; gap:10px; margin-top:25px; overflow-x:auto; width:100%; padding:10px;">
                <button onclick="quickAsk('Jinsi ya kupima sensor ya gari?')" style="padding:10px 20px; border-radius:20px; border:1px solid var(--light-green); background:white; white-space:nowrap;">Pima Sensor</button>
                <button onclick="quickAsk('Andika kodi ya HTML ya Login Page')" style="padding:10px 20px; border-radius:20px; border:1px solid var(--light-green); background:white; white-space:nowrap;">Kodi ya HTML</button>
                <button onclick="quickAsk('Nitengenezee picha ya injini ya kisasa')" style="padding:10px 20px; border-radius:20px; border:1px solid var(--light-green); background:white; white-space:nowrap;">Tengeneza Picha</button>
            </div>
        </div>
        <div id="chat-area"></div>
        <div id="typing-ui" class="typing-dots">Brain AI anaandika kwa ustadi...</div>
    </div>

    <div class="footer-input">
        <div class="input-container">
            <div class="action-icons">
                <label for="picha-upload"><i class="fas fa-camera"></i></label>
                <input type="file" id="picha-upload" accept="image/*" hidden onchange="uploadImage()">
                
                <label for="file-upload"><i class="fas fa-paperclip"></i></label>
                <input type="file" id="file-upload" hidden onchange="handleFile()">
            </div>
            
            <input type="text" id="user-msg" placeholder="Andika ujumbe hapa William..." onkeypress="handleKey(event)">
            
            <div class="action-icons">
                <i class="fas fa-microphone" id="voice-btn" onclick="startVoice()"></i>
                <i class="fas fa-paper-plane" id="send-trigger" onclick="processMessage()"></i>
            </div>
        </div>
    </div>

    <script>
        let currentImageBase64 = null;
        let brainArchive = JSON.parse(localStorage.getItem('brain_v16_history') || '[]');

        // UI CONTROLS
        function toggleSidebar() { 
            document.getElementById('sidebar').classList.toggle('active'); 
            document.getElementById('overlay').style.display = document.getElementById('sidebar').classList.contains('active') ? 'block' : 'none';
        }

        function closeAll() {
            document.getElementById('sidebar').classList.remove('active');
            document.getElementById('calc-ui').classList.remove('show');
            document.getElementById('overlay').style.display = 'none';
        }

        function toggleDarkMode() { document.body.classList.toggle('dark-mode'); }
        function toggleCalc() { 
            document.getElementById('calc-ui').classList.toggle('show');
            document.getElementById('overlay').style.display = document.getElementById('calc-ui').classList.contains('show') ? 'block' : 'none';
        }

        // CHAT LOGIC
        function appendMessage(text, type, isAi = false) {
            document.getElementById('welcome-hero').style.display = 'none';
            const area = document.getElementById('chat-area');
            const row = document.createElement('div');
            row.className = 'chat-row';
            
            const bubble = document.createElement('div');
            bubble.className = `bubble ${type}-bubble`;
            
            if(isAi) {
                    
