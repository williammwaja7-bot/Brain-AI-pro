# ==============================================================================
# PROJECT: BRAIN AI PRO - V21 ULTIMATE PDF & MONSTER EDITION
# DEVELOPER: WILLIAM RICHARD MATHAYO (ICOT TECHNICIAN)
# FIXED: PDF GENERATION, FREE IMAGES, CALCULATOR, & ARCHIVE
# ==============================================================================

import os
import json
import urllib.parse
import requests
from flask import Flask, render_template_string, request, jsonify, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__)

# API KEYS
GROQ_API_KEY = os.environ.get("GROQ_KEY")

# ==============================================================================
# MONSTER UI DESIGN (HTML, CSS, JS)
# ==============================================================================
MONSTER_HTML = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Brain AI Pro - William Richard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --primary: #075e54; --accent: #2ecc71; --bg: #f0f2f5; --white: #fff; --text: #1c1e21; --user-bg: #dcf8c6; }
        body.dark-mode { --bg: #0b141a; --white: #202c33; --text: #e9edef; --user-bg: #005c4b; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Outfit', sans-serif; }
        body { background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; overflow: hidden; transition: 0.4s; }
        
        /* NAVIGATION */
        .navbar { height: 70px; background: var(--white); border-bottom: 4px solid var(--accent); display: flex; align-items: center; justify-content: space-between; padding: 0 20px; position: fixed; top: 0; width: 100%; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .navbar h1 { font-size: 22px; font-weight: 800; color: var(--primary); }

        /* SIDEBAR / ARCHIVE */
        .sidebar { position: fixed; left: -300px; top: 0; width: 300px; height: 100%; background: var(--white); z-index: 2000; transition: 0.3s; box-shadow: 5px 0 15px rgba(0,0,0,0.2); padding: 20px; }
        .sidebar.active { left: 0; }
        .archive-card { padding: 15px; background: var(--bg); border-radius: 10px; margin-bottom: 10px; cursor: pointer; border-left: 5px solid var(--accent); font-size: 14px; }

        /* CHAT AREA */
        #chat-scroller { flex: 1; margin: 75px 0 90px; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; scroll-behavior: smooth; }
        .bubble { max-width: 85%; padding: 14px 18px; border-radius: 20px; font-size: 16px; line-height: 1.6; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .user { align-self: flex-end; background: var(--user-bg); border-bottom-right-radius: 4px; }
        .ai { align-self: flex-start; background: var(--white); border-bottom-left-radius: 4px; border-left: 6px solid var(--accent); }
        
        /* IMAGE & PDF PREVIEW */
        img { max-width: 100%; border-radius: 15px; margin-top: 10px; border: 2px solid var(--accent); }
        .pdf-btn { display: inline-block; padding: 10px 15px; background: #e74c3c; color: white; border-radius: 10px; text-decoration: none; margin-top: 10px; font-weight: bold; }

        /* CALCULATOR */
        #calc-modal { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0); width: 300px; background: var(--white); padding: 20px; border-radius: 25px; z-index: 3000; box-shadow: 0 10px 40px rgba(0,0,0,0.4); transition: 0.3s; }
        #calc-modal.active { transform: translate(-50%, -50%) scale(1); }
        .calc-screen { width: 100%; padding: 15px; text-align: right; font-size: 24px; border: none; background: var(--bg); border-radius: 12px; margin-bottom: 15px; color: var(--text); }
        .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
        .c-btn { padding: 15px; border: none; border-radius: 12px; background: var(--bg); font-weight: bold; font-size: 18px; cursor: pointer; color: var(--text); }

        /* FOOTER INPUT */
        .footer { position: fixed; bottom: 0; width: 100%; padding: 15px; background: var(--white); border-top: 1px solid #ddd; display: flex; justify-content: center; z-index: 1000; }
        .input-wrap { width: 100%; max-width: 800px; background: var(--bg); border-radius: 30px; padding: 5px 20px; display: flex; align-items: center; gap: 15px; }
        input[type="text"] { flex: 1; border: none; outline: none; background: transparent; padding: 12px 0; font-size: 16px; color: var(--text); }
        .send-btn { font-size: 28px; color: var(--accent); cursor: pointer; }
    </style>
</head>
<body>

    <div id="sidebar" class="sidebar">
        <h2 style="color:var(--primary);">Brain Archive</h2>
        <div id="archive-list" style="margin-top:20px;"></div>
        <button onclick="localStorage.clear(); location.reload();" style="width:100%; padding:12px; margin-top:20px; background:#ff4757; color:white; border:none; border-radius:10px;">Futa Kila Kitu</button>
    </div>

    <div class="navbar">
        <i class="fas fa-bars" onclick="document.getElementById('sidebar').classList.toggle('active')"></i>
        <h1>Brain AI Pro</h1>
        <div style="display:flex; gap:20px; font-size:20px; color:var(--primary);">
            <i class="fas fa-calculator" onclick="document.getElementById('calc-modal').classList.toggle('active')"></i>
            <i class="fas fa-moon" onclick="document.body.classList.toggle('dark-mode')"></i>
        </div>
    </div>

    <div id="chat-scroller">
        <div id="chat-area" style="display:flex; flex-direction:column; gap:15px;"></div>
        <div id="typing" style="display:none; color:var(--accent); font-style:italic; font-size:12px; margin-left:10px;">Brain AI anachakata...</div>
    </div>

    <div id="calc-modal">
        <input type="text" id="display" class="calc-screen" readonly>
        <div class="calc-grid">
            <button class="c-btn" onclick="v('7')">7</button><button class="c-btn" onclick="v('8')">8</button><button class="c-btn" onclick="v('9')">9</button><button class="c-btn" onclick="v('/')">/</button>
            <button class="c-btn" onclick="v('4')">4</button><button class="c-btn" onclick="v('5')">5</button><button class="c-btn" onclick="v('6')">6</button><button class="c-btn" onclick="v('*')">*</button>
            <button class="c-btn" onclick="v('1')">1</button><button class="c-btn" onclick="v('2')">2</button><button class="c-btn" onclick="v('3')">3</button><button class="c-btn" onclick="v('-')">-</button>
            <button class="c-btn" onclick="clr()" style="color:red;">C</button><button class="c-btn" onclick="v('0')">0</button><button class="c-btn" onclick="sol()" style="background:var(--accent); color:white;">=</button><button class="c-btn" onclick="v('+')">+</button>
        </div>
        <button onclick="document.getElementById('calc-modal').classList.remove('active')" style="width:100%; margin-top:15px; padding:10px; border:none; border-radius:10px;">Funga</button>
    </div>

    <div class="footer">
        <div class="input-wrap">
            <i class="fas fa-file-pdf" style="color:var(--primary); cursor:pointer;" onclick="alert('Ili kutoa PDF, andika: Toa PDF ya [ujumbe wako]')"></i>
            <input type="text" id="u-msg" placeholder="Andika hapa William..." onkeypress="if(event.key=='Enter') exec()">
            <i class="fas fa-paper-plane send-btn" onclick="exec()"></i>
        </div>
    </div>

    <script>
        let db = JSON.parse(localStorage.getItem('brain_v21_db') || '[]');

        function append(t, c) {
            const area = document.getElementById('chat-area');
            const d = document.createElement('div');
            d.className = `bubble ${c}`;
            d.innerHTML = marked.parse(t);
            area.appendChild(d);
            document.getElementById('chat-scroller').scrollTop = document.getElementById('chat-scroller').scrollHeight;
        }

        async function exec() {
            const input = document.getElementById('u-msg');
            const val = input.value.trim();
            if(!val) return;

            append(val, 'user');
            input.value = "";
            document.getElementById('typing').style.display = "block";

            // CHECK IF PDF REQUEST
            if(val.toLowerCase().startsWith("toa pdf ya")) {
                const topic = val.toLowerCase().replace("toa pdf ya", "").strip();
                window.location.href = `/api/pdf?q=${encodeURIComponent(topic)}`;
                document.getElementById('typing').style.display = "none";
                append("Tayari William! PDF yako inatengenezwa na kupakuliwa...", 'ai');
                return;
            }

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ q: val })
                });
                const data = await res.json();
                document.getElementById('typing').style.display = "none";
                append(data.ans, 'ai');
                save(val, data.ans);
            } catch {
                document.getElementById('typing').style.display = "none";
                append("Error! Hakikisha API Key iko sahihi.", 'ai');
            }
        }

        function v(x) { document.getElementById('display').value += x; }
        function clr() { document.getElementById('display').value = ""; }
        function sol() { try { document.getElementById('display').value = eval(document.getElementById('display').value); } catch { alert("Error"); } }

        function save(q, a) {
            db.unshift({q, a, time: new Date().toLocaleTimeString()});
            if(db.length > 10) db.pop();
            localStorage.setItem('brain_v21_db', JSON.stringify(db));
            renderA();
        }

        function renderA() {
            document.getElementById('archive-list').innerHTML = db.map((i, idx) => `
                <div class="archive-card" onclick="append('${i.q}','user');append('${i.a}','ai');document.getElementById('sidebar').classList.remove('active')">
                    <strong>${i.q.substring(0,25)}...</strong><br><small>${i.time}</small>
                </div>
            `).join('');
        }
        window.onload = renderA;
    </script>
</body>
</html>
'''

# ==============================================================================
# BACK-END LOGIC
# ==============================================================================

@app.route('/')
def home(): return render_template_string(MONSTER_HTML)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    q = data.get('q', '').lower()

    # 1. IMAGE GENERATION (FREE)
    if "picha ya" in q or "tengeneza picha" in q:
        prompt = q.replace("tengeneza picha ya", "").replace("picha ya", "").strip()
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true"
        return jsonify({'ans': f"Hii hapa picha ya **{prompt}** uliyotaka: \n\n![AI Image]({img_url})"})

    # 2. CHAT (GROQ)
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": "Wewe ni Brain AI Pro ya William Richard. Bingwa wa Auto Electric."}, {"role": "user", "content": q}]
    }
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=25)
        return jsonify({'ans': r.json()['choices'][0]['message']['content']})
    except:
        return jsonify({'ans': "Mtambo wa Groq umegoma. Angalia API Key."})

@app.route('/api/pdf')
def generate_pdf():
    q = request.args.get('q', 'Ujumbe wa William')
    
    # Tunatumia Groq kupata maelezo ya kuweka kwenye PDF
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"Andika maelezo marefu na ya kitaalamu kuhusu {q} kwa ajili ya PDF."}]
    }
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload).json()
        content = r['choices'][0]['message']['content']
    except:
        content = f"Maelezo kuhusu {q} hayakuweza kupatikana."

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"BRAIN AI PRO - PDF REPORT")
    p.setFont("Helvetica", 12)
    
    # Kuandika maudhui (rahisi)
    y = 700
    for line in content.split('\n'):
        if y < 50: p.showPage(); y = 750
        p.drawString(100, y, line[:90])
        y -= 20
        
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"BrainAI_{q}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
