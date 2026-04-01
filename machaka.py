import os
import warnings
import requests, base64, io
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
from PIL import Image

# 1. KUZUIA ONYO (SILENCE WARNINGS)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*google.generativeai.*")

app = Flask(__name__)

# 2. UJANJA WA KUFICHA API KEYS (ENVIRONMENT VARIABLES)
# William, hapa hatuandiki namba zako za siri. Tutaziweka kwenye Render Dashboard.
GEMINI_KEY = os.environ.get("GEMINI_KEY")
GROQ_KEY = os.environ.get("GROQ_KEY")

# Kusanidi Gemini kwa siri
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analyze_image(prompt, image_base64):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        p = f"Wewe ni Brain AI Pro iliyotengenezwa na William Richard. Jibu kwa Kiswahili: {prompt if prompt else 'Nieleze picha hii'}"
        return model.generate_content([p, image]).text
    except Exception as e:
        return f"Hitilafu ya Picha: {str(e)}"

# --- MUONEKANO (HTML/CSS/JS) ---
HTML_CODE = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Brain AI Pro - Online</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --bg: #f8fafc; --white: #ffffff; --green: #2ecc71; --user-bg: #dcf8c6; --text: #1e293b; --border: #e2e8f0; }
        body.dark-mode { --bg: #0f172a; --white: #1e293b; --green: #22c55e; --user-bg: #064e3b; --text: #f8fafc; --border: #334155; }
        body { background: var(--bg); color: var(--text); font-family: 'Outfit', sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; transition: 0.3s; }
        
        .header { padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; background: var(--white); border-bottom: 2px solid var(--green); position: fixed; top: 0; width: 100%; box-sizing: border-box; z-index: 1000; }
        .sidebar { height: 100%; width: 0; position: fixed; z-index: 2000; top: 0; background: var(--white); overflow-x: hidden; transition: 0.4s; padding-top: 20px; box-shadow: 0 0 15px rgba(0,0,0,0.2); }
        .sidebar.left { left: 0; border-right: 3px solid var(--green); }
        .sidebar.right { right: 0; border-left: 3px solid var(--green); }
        
        .search-box { padding: 10px 15px; }
        .search-box input { width: 100%; padding: 8px; border-radius: 20px; border: 1px solid var(--border); background: var(--bg); color: var(--text); outline: none; }
        
        .sidebar a, .sidebar .history-item { padding: 12px 20px; text-decoration: none; font-size: 14px; color: var(--text); display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); cursor: pointer; }
        .history-item.pinned { border-left: 4px solid var(--green); background: rgba(46, 204, 113, 0.1); }
        
        .sidebar-label { padding: 12px 20px; font-size: 11px; font-weight: bold; color: #64748b; background: var(--bg); text-transform: uppercase; }
        .closebtn { font-size: 25px; cursor: pointer; color: var(--green); padding: 10px; }
        
        #main-view { flex: 1; margin-top: 70px; margin-bottom: 85px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; }
        .chat-wrapper { display: flex; flex-direction: column; gap: 12px; width: 100%; }
        
        .msg { max-width: 85%; padding: 12px 16px; border-radius: 18px; font-size: 15px; line-height: 1.5; position: relative; box-shadow: 0 1px 3px rgba(0,0,0,0.1); word-wrap: break-word; }
        .user-msg { align-self: flex-end; background: var(--user-bg); border-bottom-right-radius: 2px; }
        .ai-msg { align-self: flex-start; background: var(--white); border-bottom-left-radius: 2px; border-left: 5px solid var(--green); }
        
        pre { background: #1e293b; color: #f8fafc; padding: 15px; border-radius: 12px; overflow-x: auto; margin: 15px 0; border-left: 5px solid var(--green); }
        .code-actions { display: flex; gap: 8px; margin-top: 5px; }
        .code-btn { background: var(--green); border: none; color: white; padding: 4px 8px; border-radius: 4px; font-size: 10px; cursor: pointer; }
        
        #drawing-canvas { border: 2px dashed var(--green); background: white; display: none; touch-action: none; border-radius: 15px; margin: 10px auto; width: 300px; height: 250px; }
        
        .footer { position: fixed; bottom: 0; width: 100%; padding: 15px; background: var(--bg); border-top: 1px solid var(--border); box-sizing: border-box; z-index: 1000; }
        .input-box { background: var(--white); border-radius: 30px; padding: 10px 20px; display: flex; align-items: center; gap: 12px; box-shadow: 0 -2px 15px rgba(0,0,0,0.1); }
        input[type="text"] { flex: 1; border: none; outline: none; font-size: 16px; background: transparent; color: var(--text); }
        .icon-btn { color: var(--green); font-size: 24px; cursor: pointer; }
    </style>
</head>
<body class="light-mode">
    <div id="leftNav" class="sidebar left">
        <div style="display:flex; justify-content:space-between; align-items:center; padding: 0 15px;">
            <h3 style="color:var(--green);">Menu</h3><span class="closebtn" onclick="closeNav('leftNav')">&times;</span>
        </div>
        <a onclick="newChat()"><i class="fas fa-plus-circle"></i> Chat Mpya</a>
        <div class="search-box"><input type="text" id="histSearch" placeholder="Tafuta..." oninput="filterHistory()"></div>
        <div class="sidebar-label">Pinned</div><div id="pinned-list"></div>
        <div class="sidebar-label">Historia</div><div id="history-list"></div>
        <a onclick="clearAllData()" style="color:#e74c3c; margin-top:20px;"><i class="fas fa-trash-alt"></i> Futa Zote</a>
    </div>

    <div id="rightNav" class="sidebar right">
        <span class="closebtn" onclick="closeNav('rightNav')">&times;</span>
        <a onclick="toggleDarkMode()"><i class="fas fa-moon"></i> Dark Mode</a>
        <a onclick="toggleCanvas()"><i class="fas fa-paint-brush"></i> Chora Umeme</a>
        <a onclick="debugCode()"><i class="fas fa-bug"></i> Debugger</a>
    </div>

    <div class="header">
        <i class="fas fa-bars" onclick="openNav('leftNav')"></i>
        <h3 style="font-family: 'Dancing Script'; font-size: 26px;">Brain AI Pro</h3>
        <i class="fas fa-cog" onclick="openNav('rightNav')"></i>
    </div>

    <div id="main-view">
        <div id="welcome-ui" style="text-align:center; padding-top:40px;">
            <h1 style="font-family: 'Dancing Script'; font-size: 50px; color:var(--green);">William Richard</h1>
            <p>Ujanja wa siri umewekwa. Pakia mtandaoni sasa!</p>
        </div>
        <center>
            <canvas id="drawing-canvas" width="300" height="250"></canvas>
            <div id="draw-btns" style="display:none; margin-top:10px;">
                <button onclick="clearCanvas()" style="background:#e74c3c; color:white; border:none; padding:8px 15px; border-radius:20px;">Futa</button>
                <button onclick="sendDrawing()" style="background:var(--green); color:white; border:none; padding:8px 15px; border-radius:20px;">Tuma</button>
            </div>
        </center>
        <div id="chat-container" class="chat-wrapper"></div>
        <center><img id="preview-img" style="display:none; max-width:200px; border-radius:10px; margin-top:10px;"></center>
    </div>

    <div class="footer">
        <div class="input-box">
            <label for="cam"><i class="fas fa-camera icon-btn"></i></label>
            <input type="file" id="cam" accept="image/*" hidden onchange="previewImg()">
            <input type="text" id="userInput" placeholder="Uliza..." onkeypress="if(event.keyCode==13) send()">
            <div onclick="send()"><i class="fas fa-paper-plane icon-btn"></i></div>
        </div>
    </div>

    <script>
        let currentImg = null; let activeChatId = null;
        let aiMemory = JSON.parse(localStorage.getItem('ai_memory')) || { AI: "", Technical: "" };
        let brainHistory = JSON.parse(localStorage.getItem('brain_history')) || {};
        let pinnedChats = JSON.parse(localStorage.getItem('pinned_chats')) || [];
        const canvas = document.getElementById('drawing-canvas'); const ctx = canvas.getContext('2d'); let drawing = false;

        function openNav(id) { document.getElementById(id).style.width = "280px"; }
        function closeNav(id) { document.getElementById(id).style.width = "0"; }
        function toggleDarkMode() { document.body.classList.toggle('dark-mode'); }

        function renderHistory() {
            const hList = document.getElementById('history-list'); const pList = document.getElementById('pinned-list'); 
            hList.innerHTML = ""; pList.innerHTML = "";
            Object.keys(brainHistory).reverse().forEach(id => {
                const item = brainHistory[id]; const div = document.createElement('div');
                div.className = `history-item ${pinnedChats.includes(id) ? 'pinned' : ''}`;
                div.innerHTML = `<div onclick="loadSavedChat('${id}')" style="flex:1;">${item.title}</div><i class="fas fa-thumbtack" onclick="togglePin('${id}')"></i>`;
                if(pinnedChats.includes(id)) pList.appendChild(div); else hList.appendChild(div);
            });
        }

        function togglePin(id) { 
            if(pinnedChats.includes(id)) pinnedChats = pinnedChats.filter(x => x !== id); 
            else pinnedChats.push(id); 
            localStorage.setItem('pinned_chats', JSON.stringify(pinnedChats)); renderHistory(); 
        }

        function filterHistory() { 
            const val = document.getElementById('histSearch').value.toLowerCase(); 
            document.querySelectorAll('.history-item').forEach(el => { el.style.display = el.innerText.toLowerCase().includes(val) ? 'flex' : 'none'; }); 
        }

        function loadSavedChat(id) { activeChatId = id; document.getElementById('welcome-ui').style.display = 'none'; document.getElementById('chat-container').innerHTML = brainHistory[id].html; closeNav('leftNav'); }
        function newChat() { activeChatId = null; document.getElementById('chat-container').innerHTML = ""; document.getElementById('welcome-ui').style.display = 'block'; closeNav('leftNav'); }

        async function send() {
            let i = document.getElementById('userInput'); let v = i.value.trim(); if(!v && !currentImg) return;
            document.getElementById('welcome-ui').style.display = 'none';
            let c = document.getElementById('chat-container');
            if(v) c.innerHTML += `<div class="msg user-msg">${v}</div>`;
            let aiId = "ai-" + Date.now();
            c.innerHTML += `<div class="msg ai-msg" id="${aiId}">Brain AI inafikiria...</div>`;
            i.value = ""; document.getElementById('main-view').scrollTop = document.getElementById('main-view').scrollHeight;
            try {
                let res = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ q: v, image: currentImg, history: aiMemory }) });
                let d = await res.json();
                document.getElementById(aiId).innerHTML = marked.parse(d.ans) + '<div class="code-actions"><button class="code-btn" onclick="copyC(this)">Copy</button></div>';
                saveWork(d.category, d.ans);
            } catch(e) { document.getElementById(aiId).innerText = "Hitilafu!"; }
            currentImg = null;
        }

        function saveWork(cat, text) {
            if (!activeChatId) { activeChatId = "chat_" + Date.now(); brainHistory[activeChatId] = { title: "Chat " + new Date().toLocaleTimeString(), html: "" }; }
            brainHistory[activeChatId].html = document.getElementById('chat-container').innerHTML;
            localStorage.setItem('brain_history', JSON.stringify(brainHistory)); renderHistory();
        }

        function copyC(btn) { const p = btn.closest('.ai-msg').innerText.replace('Copy', ''); navigator.clipboard.writeText(p); btn.innerText = "Copied!"; }
        function toggleCanvas() { let s = canvas.style.display === 'none' ? 'block' : 'none'; canvas.style.display = s; document.getElementById('draw-btns').style.display = s; closeNav('rightNav'); }
        canvas.addEventListener('touchstart', (e) => { e.preventDefault(); drawing = true; ctx.beginPath(); });
        canvas.addEventListener('touchmove', (e) => { if(!drawing) return; let t = e.touches[0]; let r = canvas.getBoundingClientRect(); ctx.lineTo(t.clientX - r.left, t.clientY - r.top); ctx.strokeStyle = '#2ecc71'; ctx.lineWidth = 3; ctx.stroke(); });
        canvas.addEventListener('touchend', () => drawing = false);
        function clearCanvas() { ctx.clearRect(0,0,300,250); }
        function sendDrawing() { currentImg = canvas.toDataURL('image/jpeg').split(',')[1]; send(); toggleCanvas(); clearCanvas(); }
        function previewImg() { const r = new FileReader(); r.onload = (e) => { currentImg = e.target.result.split(',')[1]; send(); }; r.readAsDataURL(document.getElementById('cam').files[0]); }
        function clearAllData() { if(confirm("Futa kila kitu?")) { localStorage.clear(); location.reload(); } }
        window.onload = renderHistory;
    </script>
</body>
</html>
'''

@app.route('/')
def home(): return render_template_string(HTML_CODE)

@app.route('/chat', methods=['POST'])
def chat():
    d = request.json; q = d.get('q', '').lower(); img, memory = d.get('image'), d.get('history', {})
    category = "AI" if any(x in q for x in ["code", "python", "rashid"]) else "Technical" if any(x in q for x in ["umeme", "gari"]) else "Normal"
    
    if img: return jsonify({'ans': analyze_image(q, img), 'category': category})
    
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Wewe ni Brain AI Pro. Jibu Kiswahili."}, {"role": "user", "content": q}]}
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=15)
        return jsonify({'ans': r.json()['choices'][0]['message']['content'], 'category': category})
    except: return jsonify({'ans': 'Weka API Keys zako kwenye Render ili nianze kazi!', 'category': 'Normal'})

if __name__ == '__main__':
    # Hii inaruhusu kodi kufanya kazi kwenye server yoyote
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
