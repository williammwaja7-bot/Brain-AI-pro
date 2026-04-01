import os
import warnings
import requests, base64, io
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
from PIL import Image

# 1. KUZUIA ONYO (SILENCE WARNINGS)
warnings.filterwarnings("ignore")

app = Flask(__name__)

# 2. API KEYS
GEMINI_KEY = os.environ.get("GEMINI_KEY")
GROQ_KEY = os.environ.get("GROQ_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def analyze_image(prompt, image_base64):
    try:
        model = genai.Generative_Model('gemini-1.5-flash')
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        p = f"Wewe ni Brain AI Pro ya William Richard. Jibu kwa Kiswahili: {prompt if prompt else 'Nieleze picha hii'}"
        return model.generate_content([p, image]).text
    except Exception as e:
        return f"Hitilafu ya Picha: {str(e)}"

# --- HTML CODE (LONG VERSION: 180+ LINES RECONSTRUCTED) ---
HTML_CODE = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Brain AI Pro - William Richard</title>
    
    <meta name="theme-color" content="#075e54">
    <link rel="manifest" href="data:application/manifest+json,{'name':'BrainAI','short_name':'BrainAI','start_url':'.','display':'standalone','background_color':'#0f172a','theme_color':'#075e54','icons':[{'src':'https://cdn-icons-png.flaticon.com/512/1698/1698535.png','sizes':'512x512','type':'image/png'}]}">
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        :root { 
            --bg: #f8fafc; --white: #ffffff; --green: #2ecc71; 
            --user-bg: #dcf8c6; --text: #1e293b; --border: #e2e8f0; 
            --header-bg: #075e54;
        }
        body.dark-mode { 
            --bg: #0f172a; --white: #1e293b; --green: #22c55e; 
            --user-bg: #064e3b; --text: #f8fafc; --border: #334155; 
        }

        body { 
            background: var(--bg); color: var(--text); 
            font-family: 'Outfit', sans-serif; margin: 0; 
            display: flex; flex-direction: column; height: 100vh; 
            overflow: hidden; transition: background 0.3s ease; 
        }

        /* LOGIN OVERLAY CSS */
        #login-overlay { 
            position: fixed; inset: 0; background: var(--header-bg); 
            z-index: 9999; display: flex; align-items: center; justify-content: center; 
        }
        .login-card { 
            background: white; padding: 40px; border-radius: 25px; 
            text-align: center; width: 85%; max-width: 400px; 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5); 
        }
        .login-card h2 { font-family: 'Dancing Script'; font-size: 35px; color: var(--header-bg); margin-bottom: 10px; }
        .login-card input { 
            width: 100%; padding: 15px; margin: 20px 0; 
            border: 2px solid var(--green); border-radius: 12px; 
            font-size: 25px; text-align: center; letter-spacing: 8px; outline: none;
        }
        .login-card button { 
            background: var(--header-bg); color: white; border: none; 
            padding: 15px; width: 100%; border-radius: 12px; 
            font-weight: 600; cursor: pointer; transition: 0.3s;
        }

        /* SIDEBARS */
        .header { 
            padding: 15px 20px; display: flex; align-items: center; 
            justify-content: space-between; background: var(--white); 
            border-bottom: 2px solid var(--green); position: fixed; 
            top: 0; width: 100%; box-sizing: border-box; z-index: 1000; 
        }
        
        .sidebar { 
            height: 100%; width: 0; position: fixed; z-index: 5000; 
            top: 0; background: var(--white); overflow-x: hidden; 
            transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1); 
            box-shadow: 0 0 30px rgba(0,0,0,0.3); 
        }
        .sidebar.left { left: 0; border-right: 4px solid var(--green); }
        .sidebar.right { right: 0; border-left: 4px solid var(--green); }
        
        .sidebar-header { padding: 20px; display: flex; justify-content: space-between; align-items: center; background: var(--bg); }
        .sidebar a, .sidebar button { 
            padding: 15px 25px; text-decoration: none; font-size: 16px; 
            color: var(--text); display: block; border-bottom: 1px solid var(--border); 
            background: none; border-left: none; border-right: none; width: 100%; text-align: left; cursor: pointer;
        }

        /* CHAT AREA */
        #main-view { 
            flex: 1; margin-top: 75px; margin-bottom: 100px; 
            padding: 20px; overflow-y: auto; display: flex; flex-direction: column; 
            scroll-behavior: smooth; 
        }
        
        #welcome-screen { text-align: center; margin-top: 50px; }
        #welcome-screen h1 { font-family: 'Dancing Script'; font-size: 55px; color: var(--green); margin: 0; }
        
        .msg { 
            max-width: 85%; padding: 14px 18px; border-radius: 20px; 
            font-size: 15.5px; line-height: 1.6; margin-bottom: 15px; 
            position: relative; box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
            word-wrap: break-word; animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .user-msg { align-self: flex-end; background: var(--user-bg); border-bottom-right-radius: 4px; }
        .ai-msg { align-self: flex-start; background: var(--white); border-bottom-left-radius: 4px; border-left: 6px solid var(--green); }
        
        /* DRAWING CANVAS */
        #drawing-container { display: none; text-align: center; margin: 15px 0; }
        canvas { 
            border: 3px dashed var(--green); background: #fff; 
            border-radius: 20px; touch-action: none; cursor: crosshair;
        }

        /* FOOTER & INPUT */
        .footer { 
            position: fixed; bottom: 0; width: 100%; padding: 15px; 
            background: var(--bg); border-top: 1px solid var(--border); 
            box-sizing: border-box; z-index: 1000; 
        }
        .input-box { 
            background: var(--white); border-radius: 35px; padding: 8px 20px; 
            display: flex; align-items: center; gap: 15px; 
            box-shadow: 0 -5px 20px rgba(0,0,0,0.08); 
        }
        input[type="text"] { 
            flex: 1; border: none; outline: none; font-size: 16px; 
            background: transparent; color: var(--text); padding: 10px 0;
        }
        .icon-btn { color: var(--green); font-size: 26px; cursor: pointer; transition: 0.2s; }
        .icon-btn:active { transform: scale(0.9); }
    </style>
</head>
<body>

    <div id="login-overlay">
        <div class="login-card">
            <h2>Brain AI Pro</h2>
            <p style="color: #666;">Salama William! Ingiza Saa & Dakika za sasa ili uingie:</p>
            <input type="number" id="sys_pass" placeholder="----">
            <button onclick="verifyPass()">INGIA KWENYE MFUMO</button>
            <p style="font-size: 11px; margin-top: 15px; color: #999;">Mfumo wa ulinzi wa William Richard Mathayo &copy; 2026</p>
        </div>
    </div>

    <div id="leftNav" class="sidebar left">
        <div class="sidebar-header">
            <h3 style="color:var(--green); margin:0;">Memory</h3>
            <span onclick="closeNav('leftNav')" style="font-size:30px; cursor:pointer;">&times;</span>
        </div>
        <a onclick="location.reload()"><i class="fas fa-sync"></i> Safisha Ukurasa</a>
        <div id="memory-list"></div>
        <a onclick="clearMemory()" style="color:#e74c3c; margin-top:30px;"><i class="fas fa-trash-alt"></i> Futa Kumbukumbu Zote</a>
    </div>

    <div id="rightNav" class="sidebar right">
        <div class="sidebar-header">
            <h3 style="color:var(--green); margin:0;">Settings</h3>
            <span onclick="closeNav('rightNav')" style="font-size:30px; cursor:pointer;">&times;</span>
        </div>
        <button onclick="toggleDarkMode()"><i class="fas fa-adjust"></i> Badili Rangi (Dark/Light)</button>
        <button onclick="toggleCanvas()"><i class="fas fa-paint-brush"></i> Chora Michoro ya Umeme</button>
        <button onclick="window.print()"><i class="fas fa-print"></i> Pakua Mazungumzo (PDF)</button>
        <div style="padding: 25px; font-size: 12px; color: #888;">
            <p>Model: Gemini 1.5 + Groq Llama 3</p>
            <p>Developer: William Richard</p>
        </div>
    </div>

    <div class="header">
        <i class="fas fa-history icon-btn" onclick="openNav('leftNav')"></i>
        <h1>Brain AI Pro</h1>
        <i class="fas fa-ellipsis-v icon-btn" onclick="openNav('rightNav')"></i>
    </div>

    <div id="main-view">
        <div id="welcome-screen">
            <h1>William Richard</h1>
            <p>Karibu kwenye akili mnemba yenye uwezo wa picha na sauti.</p>
        </div>

        <div id="drawing-container">
            <canvas id="drawing-canvas" width="320" height="300"></canvas>
            <div style="margin-top: 10px;">
                <button onclick="clearCanvas()" style="background:#e74c3c; color:white; border:none; padding:10px 20px; border-radius:10px;">Futa</button>
                <button onclick="sendDrawing()" style="background:var(--green); color:white; border:none; padding:10px 20px; border-radius:10px;">Tuma Mchoro</button>
            </div>
        </div>

        <div id="chat-container" style="display: flex; flex-direction: column;"></div>
    </div>

    <div class="footer">
        <div class="input-box">
            <label for="file-input"><i class="fas fa-image icon-btn"></i></label>
            <input type="file" id="file-input" accept="image/*" hidden onchange="handleImage()">
            
            <input type="text" id="userInput" placeholder="Andika ujumbe hapa..." onkeypress="if(event.keyCode==13) sendMsg()">
            
            <i class="fas fa-microphone icon-btn" id="mic-btn" onclick="startVoice()"></i>
            <i class="fas fa-paper-plane icon-btn" onclick="sendMsg()"></i>
        </div>
    </div>

    <script>
        // --- LOGIC YA ULINZI (PASSWORD) ---
        function verifyPass() {
            let sasa = new Date();
            let saa = sasa.getHours().toString().padStart(2, '0');
            let dakika = sasa.getMinutes().toString().padStart(2, '0');
            let jibu = saa + dakika; // Mfano 0830
            
            if(document.getElementById('sys_pass').value === jibu) {
                document.getElementById('login-overlay').style.opacity = '0';
                setTimeout(() => { 
                    document.getElementById('login-overlay').style.display = 'none'; 
                    loadMemory(); 
                }, 500);
            } else {
                alert("Password siyo sahihi! Angalia saa na dakika za sasa hivi kwenye simu yako.");
            }
        }

        // --- NAVIGATION ---
        function openNav(id) { document.getElementById(id).style.width = "300px"; }
        function closeNav(id) { document.getElementById(id).style.width = "0"; }
        function toggleDarkMode() { document.body.classList.toggle('dark-mode'); }

        // --- MEMORY / HISTORY SYSTEM ---
        function saveMemory(role, text) {
            let m = JSON.parse(localStorage.getItem('brain_pro_memory') || '[]');
            m.push({role, text, time: new Date().toLocaleTimeString()});
            localStorage.setItem('brain_pro_memory', JSON.stringify(m));
            updateMemoryUI();
        }

        function loadMemory() {
            let m = JSON.parse(localStorage.getItem('brain_pro_memory') || '[]');
            m.forEach(chat => {
                appendMsg(chat.text, chat.role === 'user' ? 'user-msg' : 'ai-msg');
            });
            updateMemoryUI();
        }

        function updateMemoryUI() {
            let m = JSON.parse(localStorage.getItem('brain_pro_memory') || '[]');
            const list = document.getElementById('memory-list');
            list.innerHTML = m.slice(-10).map(c => `<a><b>${c.role}:</b> ${c.text.substring(0,20)}...</a>`).join('');
        }

        function clearMemory() {
            if(confirm("Je, unataka kufuta mazungumzo yote yaliyopita?")) {
                localStorage.removeItem('brain_pro_memory');
                location.reload();
            }
        }

        // --- CHAT LOGIC ---
        let base64Image = null;

        function appendMsg(text, cls) {
            document.getElementById('welcome-screen').style.display = 'none';
            const cont = document.getElementById('chat-container');
            const div = document.createElement('div');
            div.className = `msg ${cls}`;
            div.innerHTML = marked.parse(text);
            cont.appendChild(div);
            document.getElementById('main-view').scrollTop = document.getElementById('main-view').scrollHeight;
        }

        async function sendMsg() {
            const input = document.getElementById('userInput');
            const val = input.value.trim();
            if(!val && !base64Image) return;

            appendMsg(val || "Picha imetumwa...", "user-msg");
            saveMemory('user', val || "Alituma picha");
            input.value = "";

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ q: val, image: base64Image })
                });
                const data = await res.json();
                appendMsg(data.ans, "ai-msg");
                saveMemory('ai', data.ans);
            } catch (e) {
                appendMsg("Samahani William, kuna hitilafu ya mtandao.", "ai-msg");
            }
            base64Image = null;
        }

        // --- IMAGE HANDLING ---
        function handleImage() {
            const file = document.getElementById('file-input').files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                base64Image = e.target.result.split(',')[1];
                sendMsg();
            };
            reader.readAsDataURL(file);
        }

        // --- VOICE RECOGNITION ---
        function startVoice() {
            const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            rec.lang = 'sw-TZ';
            rec.start();
            document.getElementById('mic-btn').style.color = 'red';
            rec.onresult = (e) => {
                document.getElementById('userInput').value = e.results[0][0].transcript;
                sendMsg();
            };
            rec.onend = () => { document.getElementById('mic-btn').style.color = 'var(--green)'; };
        }

        // --- DRAWING CANVAS LOGIC ---
        const canvas = document.getElementById('drawing-canvas');
        const ctx = canvas.getContext('2d');
        let painting = false;

        function toggleCanvas() {
            const box = document.getElementById('drawing-container');
            box.style.display = box.style.display === 'none' ? 'block' : 'none';
            closeNav('rightNav');
        }

        canvas.addEventListener('mousedown', startDraw);
        canvas.addEventListener('mouseup', endDraw);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('touchstart', (e) => { e.preventDefault(); startDraw(e.touches[0]); });
        canvas.addEventListener('touchend', endDraw);
        canvas.addEventListener('touchmove', (e) => { e.preventDefault(); draw(e.touches[0]); });

        function startDraw(e) { painting = true; draw(e); }
        function endDraw() { painting = false; ctx.beginPath(); }
        function draw(e) {
            if(!painting) return;
            ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.strokeStyle = '#075e54';
            const rect = canvas.getBoundingClientRect();
            ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
            ctx.stroke(); ctx.beginPath();
            ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
        }

        function clearCanvas() { ctx.clearRect(0,0,canvas.width,canvas.height); }
        function sendDrawing() {
            base64Image = canvas.toDataURL('image/jpeg').split(',')[1];
            sendMsg(); toggleCanvas(); clearCanvas();
        }
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
    q = data.get('q', '')
    img = data.get('image')

    if img:
        return jsonify({'ans': analyze_image(q, img)})
    
    # GROQ API INTEGRATION (LLAMA 3.3)
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Wewe ni Brain AI Pro iliyotengenezwa na William Richard Mathayo. Jibu kwa Kiswahili fasaha na uonyeshe utaalamu wako."},
            {"role": "user", "content": q}
        ],
        "temperature": 0.7
    }
    
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=20)
        response_data = r.json()
        return jsonify({'ans': response_data['choices'][0]['message']['content']})
    except:
        return jsonify({'ans': 'Tafadhali kagua muunganisho wako wa API Keys kwenye Render Environment Variables.'})

if __name__ == '__main__':
    # William, hii itatumia port inayotolewa na Render (Default 5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
