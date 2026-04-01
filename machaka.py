import os
import warnings
import requests, base64, io
from flask import Flask, render_template_string, request, jsonify, session
import google.generativeai as genai
from PIL import Image

warnings.filterwarnings("ignore")
app = Flask(__name__)
app.secret_key = "brain_ai_secret_william" # Siri ya Memory

# API KEYS kutoka Render Environment
GEMINI_KEY = os.environ.get("GEMINI_KEY")
GROQ_KEY = os.environ.get("GROQ_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

HTML_CODE = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Brain AI Pro</title>
    <link rel="manifest" href="data:application/manifest+json,{'name':'BrainAI','short_name':'BrainAI','start_url':'.','display':'standalone','background_color':'#075e54'}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #e5ddd5; --green: #075e54; --white: #ffffff; }
        body { font-family: 'Outfit', sans-serif; margin: 0; background: var(--bg); display: flex; flex-direction: column; height: 100vh; }
        
        /* Login UI */
        #login-screen { position: fixed; inset: 0; background: var(--green); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 5000; }
        .login-box { background: white; padding: 20px; border-radius: 15px; color: #333; width: 80%; max-width: 300px; text-align: center; }
        input.pass { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }

        /* Main UI */
        .header { background: var(--green); color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; }
        #chatBox { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; padding-bottom: 100px; }
        .msg { max-width: 80%; padding: 10px 15px; border-radius: 15px; font-size: 15px; position: relative; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
        .user-msg { align-self: flex-end; background: #dcf8c6; border-top-right-radius: 2px; }
        .ai-msg { align-self: flex-start; background: white; border-top-left-radius: 2px; }

        /* Canvas & Tools */
        #canvas-zone { display: none; background: white; border: 2px solid var(--green); margin: 10px; border-radius: 10px; }
        
        /* Footer Input (WhatsApp Style) */
        .footer { position: fixed; bottom: 0; width: 100%; background: #f0f0f0; padding: 10px; display: flex; align-items: center; gap: 8px; box-sizing: border-box; }
        .input-box { flex: 1; background: white; border-radius: 25px; padding: 8px 15px; display: flex; align-items: center; gap: 10px; }
        input[type="text"] { border: none; flex: 1; outline: none; font-size: 16px; background: transparent; }
        .circle-btn { background: var(--green); color: white; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; border: none; }
    </style>
</head>
<body>

<div id="login-screen">
    <div class="login-box">
        <h3>Brain AI Pro</h3>
        <input type="password" id="passInput" class="pass" placeholder="Password ya William...">
        <button onclick="checkPass()" style="background:var(--green); color:white; border:none; padding:10px 20px; border-radius:5px;">Ingia</button>
    </div>
</div>

<div class="header">
    <i class="fas fa-bars" onclick="alert('Memory Imewashwa!')"></i>
    <span style="font-weight: 600;">William Richard - AI</span>
    <i class="fas fa-paint-brush" onclick="toggleCanvas()"></i>
</div>

<center id="canvas-zone">
    <canvas id="mainCanvas" width="300" height="200" style="touch-action:none;"></canvas>
    <br><button onclick="sendCanvas()" style="margin-bottom:10px;">Tuma Mchoro</button>
</center>

<div id="chatBox"></div>

<div class="footer">
    <i class="fas fa-plus" style="color:#555;"></i>
    <div class="input-box">
        <input type="text" id="userInput" placeholder="Andika au tumia sauti...">
        <label for="cam"><i class="fas fa-camera" style="color:#555;"></i></label>
        <input type="file" id="cam" accept="image/*" hidden onchange="handleImg()">
    </div>
    <button class="circle-btn" id="actionBtn" onclick="handleAction()"><i class="fas fa-microphone"></i></button>
</div>

<script>
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const actionBtn = document.getElementById('actionBtn');
    
    // Check Password
    function checkPass() {
        if(document.getElementById('passInput').value === 'william2026') {
            document.getElementById('login-screen').style.display = 'none';
            loadMemory();
        } else { alert('Password siyo sahihi!'); }
    }

    // Memory Logic (LocalStorage)
    function saveMemory(role, text) {
        let mem = JSON.parse(localStorage.getItem('brain_mem') || '[]');
        mem.push({role, text});
        localStorage.setItem('brain_mem', JSON.stringify(mem));
    }
    function loadMemory() {
        let mem = JSON.parse(localStorage.getItem('brain_mem') || '[]');
        mem.forEach(m => addMsg(m.text, m.role === 'user' ? 'user-msg' : 'ai-msg'));
    }

    function addMsg(text, cls) {
        chatBox.innerHTML += `<div class="msg ${cls}">${text}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function send(text, img = null) {
        addMsg(text, 'user-msg'); saveMemory('user', text);
        userInput.value = "";
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ q: text, img: img })
        });
        const d = await res.json();
        addMsg(d.ans, 'ai-msg'); saveMemory('ai', d.ans);
    }

    // Voice & Send Button Switch
    userInput.oninput = () => {
        actionBtn.innerHTML = userInput.value ? '<i class="fas fa-paper-plane"></i>' : '<i class="fas fa-microphone"></i>';
    };

    function handleAction() {
        if(userInput.value) { send(userInput.value); }
        else { startVoice(); }
    }

    function startVoice() {
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'sw-TZ';
        rec.start();
        actionBtn.style.background = "red";
        rec.onresult = (e) => { send(e.results[0][0].transcript); actionBtn.style.background = "#075e54"; };
        rec.onend = () => actionBtn.style.background = "#075e54";
    }

    // Drawing Logic
    const canvas = document.getElementById('mainCanvas'); const ctx = canvas.getContext('2d');
    let drawing = false;
    function toggleCanvas() { document.getElementById('canvas-zone').style.display = 'block'; }
    canvas.onpointerdown = () => drawing = true;
    canvas.onpointermove = (e) => { if(drawing){ ctx.lineTo(e.offsetX, e.offsetY); ctx.stroke(); } };
    canvas.onpointerup = () => { drawing = false; ctx.beginPath(); };
    function sendCanvas() { send("Nimechora huu mchoro wa umeme, nieleze:", canvas.toDataURL('image/jpeg').split(',')[1]); document.getElementById('canvas-zone').style.display='none'; }

    function handleImg() {
        const reader = new FileReader();
        reader.onload = (e) => send("Nimekutumia picha hii ya gari:", e.target.result.split(',')[1]);
        reader.readAsDataURL(document.getElementById('cam').files[0]);
    }
</script>
</body>
</html>
'''

@app.route('/')
def home(): return render_template_string(HTML_CODE)

@app.route('/chat', methods=['POST'])
def chat():
    d = request.json; q = d.get('q', ''); img = d.get('img')
    try:
        if img:
            model = genai.GenerativeModel('gemini-1.5-flash')
            image_data = base64.b64decode(img)
            image = Image.open(io.BytesIO(image_data))
            res = model.generate_content([f"Wewe ni Brain AI Pro ya William. Jibu kwa Kiswahili: {q}", image])
            return jsonify({'ans': res.text})
        
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Wewe ni Brain AI Pro. Jibu Kiswahili."}, {"role": "user", "content": q}]}
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        return jsonify({'ans': r.json()['choices'][0]['message']['content']})
    except: return jsonify({'ans': 'Hitilafu! Hakikisha API Keys zipo Render.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
