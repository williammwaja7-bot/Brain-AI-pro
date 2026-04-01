import os
import warnings
import requests, base64, io, json
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
from PIL import Image

# ============================================================
# BRAIN AI PRO V11 - DEVELOPED BY WILLIAM RICHARD MATHAYO
# FULL MOBILE RESPONSIVE OPTIMIZATION (KIOO CHA SIMU)
# ============================================================

warnings.filterwarnings("ignore")
app = Flask(__name__)

# CONFIGURATION ZA API
GEMINI_KEY = os.environ.get("GEMINI_KEY")
GROQ_KEY = os.environ.get("GROQ_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analyze_image(prompt, image_base64):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        p = f"Wewe ni Brain AI Pro ya William Richard. Jibu kwa Kiswahili: {prompt if prompt else 'Nieleze picha hii'}"
        return model.generate_content([p, image]).text
    except Exception as e:
        return f"Hitilafu ya Picha: {str(e)}"

# ============================================================
# FRONT-END (MUONEKANO WA KIOO CHA SIMU - FULL RESPONSIVE)
# ============================================================

HTML_CODE = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Brain AI Pro - William Richard</title>
    
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#075e54">
    <link rel="manifest" href="data:application/manifest+json,{'name':'BrainAI Pro','short_name':'BrainAI','start_url':'.','display':'standalone','background_color':'#0b141a','theme_color':'#075e54'}">
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Outfit:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        :root { 
            --primary: #075e54; --accent: #2ecc71; --bg: #f0f2f5; 
            --white: #ffffff; --text: #1c1e21; --border: #ced4da; 
            --user-bubble: #dcf8c6; --ai-bubble: #ffffff;
            --sidebar-bg: #ffffff;
        }
        
        body.dark-mode { 
            --bg: #0b141a; --white: #111b21; --text: #e9edef; 
            --border: #222d34; --user-bubble: #005c4b; --ai-bubble: #202c33;
            --sidebar-bg: #111b21;
        }

        body { 
            background: var(--bg); color: var(--text); 
            font-family: 'Outfit', sans-serif; margin: 0; 
            display: flex; flex-direction: column; height: 100vh; 
            height: -webkit-fill-available;
            overflow: hidden; transition: 0.3s; 
        }

        /* --- SIDEBAR LEFT (VISTARI VITATU) --- */
        .sidebar-left { 
            height: 100%; width: 0; position: fixed; z-index: 5000; 
            top: 0; left: 0; background: var(--sidebar-bg); 
            overflow-x: hidden; transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
            box-shadow: 5px 0 15px rgba(0,0,0,0.3); 
            display: flex; flex-direction: column;
        }

        .profile-section { 
            padding: 40px 20px 20px; background: var(--primary); color: white; 
            text-align: center; border-bottom: 4px solid var(--accent);
        }
        .profile-img { 
            width: 70px; height: 70px; border-radius: 50%; 
            border: 2px solid var(--accent); margin-bottom: 10px;
            object-fit: cover;
        }

        .menu-list { flex: 1; overflow-y: auto; padding: 5px 0; }
        .menu-item { 
            padding: 16px 20px; display: flex; align-items: center; gap: 15px;
            color: var(--text); text-decoration: none; font-size: 15px;
            border-bottom: 1px solid var(--border); transition: 0.2s;
        }
        .menu-item:active { background: rgba(46, 204, 113, 0.2); }
        .menu-item i { color: var(--accent); width: 25px; font-size: 18px; }

        .search-container { padding: 10px 15px; }
        #searchHistory { 
            width: 100%; padding: 12px; border-radius: 12px; 
            border: 1px solid var(--border); background: var(--bg); color: var(--text);
            font-size: 14px; outline: none;
        }

        /* --- HEADER (FIXED TO SCREEN WIDTH) --- */
        .header { 
            height: 65px; padding: 0 20px; display: flex; align-items: center; 
            justify-content: space-between; background: var(--white); 
            border-bottom: 2px solid var(--accent); position: fixed; 
            top: 0; width: 100%; z-index: 1000; 
        }
        .header h1 { font-family: 'Dancing Script'; font-size: 24px; margin: 0; color: var(--primary); }

        /* --- MAIN VIEW (FULL MOBILE HEIGHT) --- */
        #main-view { 
            flex: 1; margin-top: 65px; margin-bottom: 80px; 
            padding: 15px; overflow-y: auto; display: flex; flex-direction: column;
            width: 100%;
        }
        
        .welcome-center { text-align: center; padding: 40px 10px; }
        .welcome-center h2 { font-family: 'Dancing Script'; font-size: 42px; color: var(--accent); margin: 0; }

        .chat-bubble { 
            max-width: 90%; padding: 12px 16px; border-radius: 18px; 
            margin-bottom: 12px; line-height: 1.5; font-size: 15px;
            position: relative; box-shadow: 0 1px 3px rgba(0,0,0,0.1); 
            animation: bubblePop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes bubblePop { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
        
        .user-bubble { align-self: flex-end; background: var(--user-bubble); border-bottom-right-radius: 2px; color: #1c1e21; }
        .ai-bubble { align-self: flex-start; background: var(--ai-bubble); border-bottom-left-radius: 2px; border-left: 5px solid var(--accent); }

        /* --- CALCULATOR OVERLAY --- */
        #calculator-overlay { 
            display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.9); 
            z-index: 6000; align-items: center; justify-content: center; padding: 20px;
        }
        .calc-body { 
            background: #1c1c1c; padding: 20px; border-radius: 30px; 
            width: 100%; max-width: 320px;
        }
        .calc-screen { 
            width: 100%; background: #000; border: none; color: #fff; 
            padding: 20px; font-size: 30px; text-align: right; margin-bottom: 15px;
            font-family: 'JetBrains Mono'; border-radius: 15px;
        }
        .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
        .calc-grid button { 
            height: 60px; border-radius: 50%; border: none; font-size: 20px;
            background: #333; color: white; cursor: pointer; font-weight: bold;
        }
        .calc-grid button.op { background: #f39c12; }
        .calc-grid button.eq { background: var(--accent); }

        /* --- FOOTER (STAYS AT BOTTOM OF SCREEN) --- */
        .footer { 
            position: fixed; bottom: 0; width: 100%; padding: 10px 15px; 
            background: var(--white); border-top: 1px solid var(--border); 
            z-index: 1000; padding-bottom: calc(10px + env(safe-area-inset-bottom));
        }
        .input-box { 
            background: var(--bg); border-radius: 30px; padding: 5px 15px; 
            display: flex; align-items: center; gap: 10px; width: 100%;
        }
        input[type="text"] { 
            flex: 1; border: none; outline: none; background: transparent; 
            color: var(--text); font-size: 16px; padding: 10px 0;
        }
        .icon-btn { color: var(--primary); font-size: 22px; cursor: pointer; }

        /* CANVAS BOARD */
        #canvas-box { 
            display: none; text-align: center; background: #fff; 
            padding: 10px; border-radius: 20px; margin-bottom: 15px; 
            border: 2px dashed var(--accent); width: 100%;
        }
        canvas { max-width: 100%; height: auto; background: #fff; }
    </style>
</head>
<body>

    <div id="leftSidebar" class="sidebar-left">
        <div class="profile-section">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="profile-img">
            <h3 style="margin:0;">William Richard</h3>
            <p style="font-size:12px;">Auto Electric Specialist</p>
        </div>
        
        <div class="search-container">
            <input type="text" id="searchHistory" placeholder="Tafuta historia..." oninput="filterHistory()">
        </div>

        <div class="menu-list">
            <a onclick="newChat()" class="menu-item"><i class="fas fa-edit"></i> New Chat</a>
            <div id="chatHistoryList"></div>
            <a onclick="toggleCalc()" class="menu-item"><i class="fas fa-calculator"></i> Calculator</a>
            <a onclick="toggleDarkMode()" class="menu-item"><i class="fas fa-adjust"></i> Dark Mode</a>
            <a onclick="clearAll()" class="menu-item" style="color:#e74c3c;"><i class="fas fa-trash-alt"></i> Futa Kumbukumbu</a>
        </div>
        
        <div style="padding:15px; font-size:11px; color:#888; text-align:center;">
            <b>Brain AI Pro</b><br>Toleo la William Richard 2026
        </div>
    </div>

    <div class="header">
        <i class="fas fa-bars icon-btn" onclick="openNav()"></i>
        <h1>Brain AI Pro</h1>
        <i class="fas fa-paint-brush icon-btn" onclick="toggleCanvas()"></i>
    </div>

    <div id="calculator-overlay">
        <div class="calc-body">
            <input type="text" id="calcDisplay" class="calc-screen" readonly>
            <div class="calc-grid">
                <button onclick="calcClear()" style="background:#7f8c8d;">AC</button>
                <button onclick="calcBack()" style="background:#7f8c8d;"><i class="fas fa-backspace"></i></button>
                <button onclick="calcIn('/')" class="op">/</button>
                <button onclick="calcIn('*')" class="op">×</button>
                
                <button onclick="calcIn('7')">7</button><button onclick="calcIn('8')">8</button>
                <button onclick="calcIn('9')">9</button><button onclick="calcIn('-')" class="op">-</button>
                
                <button onclick="calcIn('4')">4</button><button onclick="calcIn('5')">5</button>
                <button onclick="calcIn('6')">6</button><button onclick="calcIn('+')" class="op">+</button>
                
                <button onclick="calcIn('1')">1</button><button onclick="calcIn('2')">2</button>
                <button onclick="calcIn('3')">3</button>
                <button onclick="calcEqual()" class="eq" style="grid-row: span 2; height: 132px; border-radius: 30px;">=</button>
                
                <button onclick="calcIn('0')" style="grid-column: span 2; border-radius: 30px;">0</button>
                <button onclick="calcIn('.')">.</button>
            </div>
            <button onclick="toggleCalc()" style="width:100%; margin-top:20px; background:none; border:1px solid #555; color:white; padding:12px; border-radius:15px;">Funga</button>
        </div>
    </div>

    <div id="main-view">
        <div id="welcome-ui" class="welcome-center">
            <h2>Habari William!</h2>
            <p>Mfumo wa kisasa wa Akili Mnemba upo tayari kukusaidia leo.</p>
        </div>

        <div id="canvas-box">
            <canvas id="drawCanvas" width="300" height="300"></canvas>
            <div style="padding:15px; display:flex; gap:10px; justify-content:center;">
                <button onclick="sendArt()" style="background:var(--accent); color:white; border:none; padding:12px 25px; border-radius:12px; font-weight:bold;">Tuma</button>
                <button onclick="toggleCanvas()" style="background:#95a5a6; color:white; border:none; padding:12px 25px; border-radius:12px;">Funga</button>
            </div>
        </div>

        <div id="chat-container" style="display:flex; flex-direction:column;"></div>
    </div>

    <div class="footer">
        <div class="input-box">
            <label for="imgIn"><i class="fas fa-image icon-btn"></i></label>
            <input type="file" id="imgIn" accept="image/*" hidden onchange="handleImage()">
            
            <input type="text" id="userInput" placeholder="Andika hapa..." onkeypress="if(event.keyCode==13) send()">
            
            <i class="fas fa-microphone icon-btn" id="mic" onclick="startVoice()"></i>
            <i class="fas fa-paper-plane icon-btn" onclick="send()" style="color:var(--accent);"></i>
        </div>
    </div>

    <script>
        let currentImg = null;
        const chatCont = document.getElementById('chat-container');

        // NAVIGATION
        function openNav() { document.getElementById('leftSidebar').style.width = "85%"; }
        function closeNav() { document.getElementById('leftSidebar').style.width = "0"; }

        // MEMORY SYSTEM
        function saveChat(role, msg) {
            let h = JSON.parse(localStorage.getItem('william_v11_db') || '[]');
            h.push({role, msg});
            localStorage.setItem('william_v11_db', JSON.stringify(h));
            renderHistoryList();
        }

        function loadChat() {
            let h = JSON.parse(localStorage.getItem('william_v11_db') || '[]');
            if(h.length > 0) document.getElementById('welcome-ui').style.display = 'none';
            h.forEach(c => appendBubble(c.msg, c.role === 'user' ? 'user-bubble' : 'ai-bubble'));
            renderHistoryList();
        }

        function renderHistoryList() {
            let h = JSON.parse(localStorage.getItem('william_v11_db') || '[]');
            const list = document.getElementById('chatHistoryList');
            list.innerHTML = h.slice(-15).reverse().map(c => `
                <a class="menu-item history-item" onclick="closeNav()">
                    <i class="fas fa-history"></i> ${c.msg.substring(0,25)}...
                </a>
            `).join('');
        }

        function filterHistory() {
            let val = document.getElementById('searchHistory').value.toLowerCase();
            document.querySelectorAll('.history-item').forEach(el => {
                el.style.display = el.innerText.toLowerCase().includes(val) ? 'flex' : 'none';
            });
        }

        function newChat() { if(confirm("Anza upya?")) { localStorage.clear(); location.reload(); } }
        function clearAll() { if(confirm("Futa data zote?")) { localStorage.clear(); location.reload(); } }

        // CALCULATOR
        function toggleCalc() {
            let c = document.getElementById('calculator-overlay');
            c.style.display = (c.style.display === 'flex') ? 'none' : 'flex';
            closeNav();
        }
        function calcIn(v) { document.getElementById('calcDisplay').value += v; }
        function calcClear() { document.getElementById('calcDisplay').value = ""; }
        function calcBack() { let v = document.getElementById('calcDisplay').value; document.getElementById('calcDisplay').value = v.slice(0,-1); }
        function calcEqual() {
            try { document.getElementById('calcDisplay').value = eval(document.getElementById('calcDisplay').value.replace('×','*').replace('÷','/')); }
            catch { document.getElementById('calcDisplay').value = "Error"; }
        }

        // CHAT LOGIC
        function appendBubble(txt, cls) {
            document.getElementById('welcome-ui').style.display = 'none';
            const div = document.createElement('div');
            div.className = `chat-bubble ${cls}`;
            div.innerHTML = marked.parse(txt);
            chatCont.appendChild(div);
            document.getElementById('main-view').scrollTop = document.getElementById('main-view').scrollHeight;
        }

        async function send() {
            const input = document.getElementById('userInput');
            const val = input.value.trim();
            if(!val && !currentImg) return;

            appendBubble(val || "Picha inachambuliwa...", "user-bubble");
            saveChat('user', val || "Picha");
            input.value = "";

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ q: val, image: currentImg })
                });
                const d = await res.json();
                appendBubble(d.ans, "ai-bubble");
                saveChat('ai', d.ans);
            } catch {
                appendBubble("Kuna tatizo la connection!", "ai-bubble");
            }
            currentImg = null;
        }

        function handleImage() {
            const file = document.getElementById('imgIn').files[0];
            const reader = new FileReader();
            reader.onload = (e) => { currentImg = e.target.result.split(',')[1]; send(); };
            reader.readAsDataURL(file);
        }

        function startVoice() {
            const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            rec.lang = 'sw-TZ'; rec.start();
            document.getElementById('mic').style.color = 'red';
            rec.onresult = (e) => { document.getElementById('userInput').value = e.results[0][0].transcript; send(); };
            rec.onend = () => { document.getElementById('mic').style.color = 'var(--primary)'; };
        }

        // CANVAS DRAWING
        const canvas = document.getElementById('drawCanvas');
        const ctx = canvas.getContext('2d');
        let painting = false;

        function toggleCanvas() { 
            let b = document.getElementById('canvas-box');
            b.style.display = (b.style.display === 'block') ? 'none' : 'block';
        }
        canvas.ontouchstart = (e) => { e.preventDefault(); painting = true; ctx.beginPath(); };
        canvas.ontouchmove = (e) => {
            if(!painting) return;
            let t = e.touches[0]; let r = canvas.getBoundingClientRect();
            ctx.lineTo(t.clientX - r.left, t.clientY - r.top);
            ctx.strokeStyle = '#075e54'; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.stroke();
        };
        canvas.ontouchend = () => painting = false;

        function sendArt() {
            currentImg = canvas.toDataURL('image/jpeg').split(',')[1];
            send(); toggleCanvas(); ctx.clearRect(0,0,300,300);
        }

        function toggleDarkMode() { document.body.classList.toggle('dark-mode'); closeNav(); }

        window.onload = loadChat;
    </script>
</body>
</html>
'''

# ============================================================
# BACK-END (API & ROUTES)
# ============================================================

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    q = data.get('q', '')
    img = data.get('image')

    if img:
        return jsonify({'ans': analyze_image(q, img)})
    
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Wewe ni Brain AI Pro ya William Richard. Jibu kwa Kiswahili fasaha na ueleze mambo kitaalamu."},
            {"role": "user", "content": q}
        ],
        "temperature": 0.7
    }
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=25)
  
