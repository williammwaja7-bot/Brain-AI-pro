# ==============================================================================
# PROJECT: BRAIN AI PRO - V19 THE FULL HEAVYWEIGHT MONSTER
# DEVELOPER: WILLIAM RICHARD MATHAYO (STUDENT & TECHNICIAN)
# LOCATION: DAR ES SALAAM, TANZANIA
# PURPOSE: ADVANCED AUTO-ELECTRIC & PROGRAMMING ASSISTANT
# ==============================================================================
# HII KODI NI KWA AJILI YA WILLIAM PEKEE. IMEBORESHA UI, CALCULATOR, NA ARCHIVE.
# ==============================================================================

import os
import json
import time
import datetime
import requests
import urllib.parse
from flask import Flask, render_template_string, request, jsonify

# Kuanzisha Flask App
app = Flask(__name__)

# SEHEMU YA API KEYS
# Hakikisha hizi zipo kwenye Render Environment Variables
GROQ_API_KEY = os.environ.get("GROQ_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_KEY")

# ==============================================================================
# FRONT-END (HTML, CSS, JS) - THE BIG DESIGN SECTION
# ==============================================================================

HEAVY_HTML = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Brain AI Pro - William Richard</title>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        /* CSS MASTER VARIABLES */
        :root {
            --primary: #075e54;
            --accent: #2ecc71;
            --bg: #f0f2f5;
            --white: #ffffff;
            --user-chat: #dcf8c6;
            --text: #1c1e21;
            --sidebar-w: 300px;
        }

        body.dark-mode {
            --bg: #0b141a;
            --white: #202c33;
            --user-chat: #005c4b;
            --text: #e9edef;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: 0.4s;
        }

        /* HEADER DESIGN */
        .header {
            height: 70px;
            background: var(--white);
            border-bottom: 4px solid var(--accent);
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

        .header h1 { font-size: 22px; font-weight: 800; color: var(--primary); }

        /* SIDEBAR / ARCHIVE */
        .sidebar {
            position: fixed;
            left: -300px;
            top: 0;
            width: var(--sidebar-w);
            height: 100%;
            background: var(--white);
            z-index: 2000;
            transition: 0.3s ease-in-out;
            box-shadow: 5px 0 15px rgba(0,0,0,0.2);
            padding: 20px;
        }

        .sidebar.active { left: 0; }
        
        .archive-list { margin-top: 20px; max-height: 70vh; overflow-y: auto; }
        .archive-card {
            padding: 15px;
            background: var(--bg);
            border-radius: 10px;
            margin-bottom: 10px;
            cursor: pointer;
            border-left: 4px solid var(--accent);
        }

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

        .bubble {
            max-width: 85%;
            padding: 14px 18px;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.6;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .user { align-self: flex-end; background: var(--user-chat); border-bottom-right-radius: 4px; }
        .ai { align-self: flex-start; background: var(--white); border-bottom-left-radius: 4px; border-left: 6px solid var(--accent); }

        /* CALCULATOR UI */
        #calc-modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            width: 300px;
            background: var(--white);
            padding: 20px;
            border-radius: 25px;
            z-index: 3000;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            transition: 0.3s;
        }

        #calc-modal.active { transform: translate(-50%, -50%) scale(1); }
        .calc-screen { width: 100%; padding: 20px; text-align: right; font-size: 28px; border: none; background: var(--bg); border-radius: 15px; margin-bottom: 15px; color: var(--text); }
        .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
        .btn-c { padding: 15px; border: none; border-radius: 12px; background: var(--bg); font-weight: bold; font-size: 18px; cursor: pointer; color: var(--text); }
        .btn-op { background: var(--accent); color: white; }

        /* INPUT FOOTER */
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 15px;
            background: var(--white);
            border-top: 1px solid #ddd;
            display: flex;
            justify-content: center;
            z-index: 1000;
        }

        .input-wrap {
            width: 100%;
            max-width: 800px;
            background: var(--bg);
            border-radius: 30px;
            padding: 5px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        input[type="text"] { flex: 1; border: none; outline: none; background: transparent; padding: 12px 0; font-size: 16px; color: var(--text); }
        .send-icon { font-size: 28px; color: var(--accent); cursor: pointer; }

        /* TYPING EFFECT */
        #typing { display: none; padding: 10px; font-style: italic; color: var(--accent); font-weight: 600; }

        img { max-width: 100%; border-radius: 15px; margin-top: 10px; border: 2px solid var(--accent); }
    </style>
</head>
<body>

    <div id="sidebar" class="sidebar">
        <h2 style="color:var(--primary);">Brain Archive</h2>
        <p style="font-size:12px; margin-bottom:20px;">Mihifadhi ya William Richard</p>
        <div class="archive-list" id="archive-list"></div>
        <button onclick="clearAll()" style="width:100%; padding:12px; margin-top:20px; background:#ff4757; color:white; border:none; border-radius:10px;">Futa Kila Kitu</button>
    </div>

    <div class="header">
        <i class="fas fa-bars" onclick="toggleS()" style="font-size:24px; cursor:pointer;"></i>
        <h1>Brain AI Pro</h1>
        <div style="display:flex; gap:20px; font-size:20px; color:var(--primary);">
            <i class="fas fa-calculator" onclick="toggleC()"></i>
            <i class="fas fa-moon" onclick="toggleD()"></i>
        </div>
    </div>

    <div id="chat-scroller">
        <div id="chat-area" style="display:flex; flex-direction:column; gap:15px;"></div>
        <div id="typing">Brain AI anafikiria...</div>
    </div>

    <div id="calc-modal">
        <input type="text" id="display" class="calc-screen" readonly>
        <div class="calc-grid">
            <button class="btn-c" onclick="v('7')">7</button><button class="btn-c" onclick="v('8')">8</button><button class="btn-c" onclick="v('9')">9</button><button class="btn-c btn-op" onclick="v('/')">/</button>
            <button class="btn-c" onclick="v('4')">4</button><button class="btn-c" onclick="v('5')">5</button><button class="btn-c" onclick="v('6')">6</button><button class="btn-c btn-op" onclick="v('*')">*</button>
            <button class="btn-c" onclick="v('1')">1</button><button class="btn-c" onclick="v('2')">2</button><button class="btn-c" onclick="v('3')">3</button><button class="btn-c btn-op" onclick="v('-')">-</button>
            <button class="btn-c" onclick="clr()" style="color:red;">C</button><button class="btn-c" onclick="v('0')">0</button><button class="btn-c" onclick="solve()" style="background:var(--accent); color:white;">=</button><button class="btn-c btn-op" onclick="v('+')">+</button>
        </div>
        <button onclick="toggleC()" style="width:100%; margin-top:15px; padding:10px; border:none; border-radius:10px;">Funga</button>
    </div>

    <div class="footer">
        <div class="input-wrap">
            <i class="fas fa-camera" style="color:var(--primary);"></i>
            <input type="text" id="u-msg" placeholder="Andika hapa William..." onkeypress="if(event.key=='Enter') execute()">
            <i class="fas fa-paper-plane send-icon" onclick="execute()"></i>
        </div>
    </div>

    <script>
        let db = JSON.parse(localStorage.getItem('brain_archive_v19') || '[]');

        function toggleS() { document.getElementById('sidebar').classList.toggle('active'); }
        function toggleD() { document.body.classList.toggle('dark-mode'); }
        function toggleC() { document.getElementById('calc-modal').classList.toggle('active'); }

        function append(t, c) {
            const area = document.getElementById('chat-area');
            const d = document.createElement('div');
            d.className = `bubble ${c}`;
            d.innerHTML = marked.parse(t);
            area.appendChild(d);
            document.getElementById('chat-scroller').scrollTop = document.getElementById('chat-scroller').scrollHeight;
        }

        async function execute() {
            const input = document.getElementById('u-msg');
            const val = input.value.trim();
            if(!val) return;

            append(val, 'user');
            input.value = "";
            document.getElementById('typing').style.display = "block";

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ q: val })
                });
                const data = await res.json();
                document.getElementById('typing').style.display = "none";
                append(data.ans, 'ai');
                
                // Save to archive
                save(val, data.ans);
            } catch {
                document.getElementById('typing').style.display = "none";
                append("Kuna hitilafu! Angalia kama umechomeka Groq Key kule Render.", 'ai');
            }
        }

        function v(x) { document.getElementById('display').value += x; }
        function clr() { document.getElementById('display').value = ""; }
        function solve() { 
            try { document.getElementById('display').value = eval(document.getElementById('display').value); } 
            catch { document.getElementById('display').value = "Error"; } 
        }

        function save(q, a) {
            db.unshift({q, a, time: new Date().toLocaleTimeString()});
            if(db.length > 15) db.pop();
            localStorage.setItem('brain_archive_v19', JSON.stringify(db));
            loadArchive();
        }

        function loadArchive() {
            const list = document.getElementById('archive-list');
            list.innerHTML = db.map((i, index) => `
                <div class="archive-card" onclick="restore(${index})">
                    <strong>${i.q.substring(0,25)}...</strong><br>
                    <small>${i.time}</small>
                </div>
            `).join('');
        }

        function restore(idx) {
            append(db[idx].q, 'user');
            append(db[idx].a, 'ai');
            toggleS();
        }

        function clearAll() { localStorage.clear(); location.reload(); }
        window.onload = loadArchive;
    </script>
</body>
</html>
'''

# ==============================================================================
# BACK-END LOGIC (FLASK & API)
# ==============================================================================

@app.route('/')
def home():
    return render_template_string(HEAVY_HTML)

@app.route('/api/chat', methods=['POST'])
def chat_engine():
    data = request.json
    user_query = data.get('q', '').lower()

    # 1. GENERATE IMAGE (FREE - POLLINATIONS AI)
    # William, hii inafanya kazi hata kama huna hela ya OpenAI
    if "tengeneza picha ya" in user_query or "picha ya" in user_query:
        search_term = user_query.replace("tengeneza picha ya", "").strip()
        encoded = urllib.parse.quote(search_term)
        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
        return jsonify({'ans': f"Tayari William! Nimekutengenezea picha ya **{search_term}**: \n\n![AI Image]({image_url})"})

    # 2. TEXT CHAT (GROQ ENGINE)
    if not GROQ_API_KEY:
        return jsonify({'ans': "William, umesahau kuweka GROQ_KEY kule kwenye Render Environment Variables!"})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Wewe ni Brain AI Pro, umetengenezwa na William Richard Mathayo. Wewe ni bingwa wa Auto Electric na Coding. Jibu kwa Kiswahili."},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=25
        )
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            return jsonify({'ans': result})
        else:
            return jsonify({'ans': "Groq API imekataa. Hakikisha key yako ni sahihi."})
    except Exception as e:
        return jsonify({'ans': f"Hitilafu: {str(e)}"})

# SERVER START
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# MWISHO WA KODI YA V19 - THE MONSTER IS BACK!
