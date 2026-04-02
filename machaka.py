import os
import warnings
import requests
import base64
import io
import json
import re
import time
import hashlib
import uuid
import random
import yfinance as yf
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from functools import wraps
import threading
import queue

# ==================== KANZU YA MAONYO ====================
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ==================== INSTALL PACKAGES ZA ZIADA ====================
"""
Endesha hizi commands kabla ya kuanza:
pip install google-generativeai pillow PyPDF2 python-docx googlesearch-python yfinance qrcode requests beautifulsoup4 yt-dlp
"""

# ==================== IMPORTS ZA ZIADA ====================
try:
    import google.generativeai as genai
    from PIL import Image
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from googlesearch import search
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# ==================== FLASK APP ====================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "brain-ai-pro-ultimate-secret-key-2024")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file

# ==================== API KEYS ====================
GEMINI_KEY = os.environ.get("GEMINI_KEY")
GROQ_KEY = os.environ.get("GROQ_KEY")
TAVILY_KEY = os.environ.get("TAVILY_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # Tafuta bure kwenye openweathermap.org
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")  # Tafuta bure kwenye newsapi.org

if GEMINI_KEY and GEMINI_AVAILABLE:
    genai.configure(api_key=GEMINI_KEY)

# ==================== USER ACCOUNTS ====================
USERS_FILE = "users.json"
SCHEDULES_FILE = "schedules.json"
NOTES_FILE = "notes.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def load_schedules():
    if os.path.exists(SCHEDULES_FILE):
        with open(SCHEDULES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_schedules(schedules):
    with open(SCHEDULES_FILE, 'w') as f:
        json.dump(schedules, f)

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f)

# ==================== LUGHA 7 ====================
LANGUAGES = {
    "sw": {"name": "Kiswahili", "code": "sw-TZ", "flag": "🇹🇿", "voice_lang": "sw-TZ"},
    "en": {"name": "English", "code": "en-US", "flag": "🇺🇸", "voice_lang": "en-US"},
    "fr": {"name": "Français", "code": "fr-FR", "flag": "🇫🇷", "voice_lang": "fr-FR"},
    "ar": {"name": "العربية", "code": "ar-SA", "flag": "🇸🇦", "voice_lang": "ar-SA"},
    "es": {"name": "Español", "code": "es-ES", "flag": "🇪🇸", "voice_lang": "es-ES"},
    "de": {"name": "Deutsch", "code": "de-DE", "flag": "🇩🇪", "voice_lang": "de-DE"},
    "zh": {"name": "中文", "code": "zh-CN", "flag": "🇨🇳", "voice_lang": "zh-CN"}
}

# ==================== TRANSLATIONS ====================
def get_translation(lang, key):
    translations = {
        "sw": {
            "weather": "🌤️ Hali ya Hewa",
            "news": "📰 Habari za Mwisho",
            "stock": "📊 Bei ya Hisa",
            "crypto": "💰 Bei ya Crypto",
            "no_data": "⚠️ Hakuna taarifa",
            "qr_generated": "✅ QR Code imetengenezwa",
            "note_saved": "✅ Maelezo yamehifadhiwa",
            "reminder_set": "✅ Kumbusho limewekwa",
            "game_start": "🎮 Mchezo umeanza!",
            "email_sent": "📧 Barua pepe imetumwa"
        },
        "en": {
            "weather": "🌤️ Weather",
            "news": "📰 Latest News",
            "stock": "📊 Stock Price",
            "crypto": "💰 Crypto Price",
            "no_data": "⚠️ No data available",
            "qr_generated": "✅ QR Code generated",
            "note_saved": "✅ Note saved",
            "reminder_set": "✅ Reminder set",
            "game_start": "🎮 Game started!",
            "email_sent": "📧 Email sent"
        },
        "fr": {
            "weather": "🌤️ Météo",
            "news": "📰 Dernières nouvelles",
            "stock": "📊 Cours de l'action",
            "crypto": "💰 Prix crypto",
            "no_data": "⚠️ Aucune donnée",
            "qr_generated": "✅ Code QR généré",
            "note_saved": "✅ Note enregistrée",
            "reminder_set": "✅ Rappel défini",
            "game_start": "🎮 Jeu commencé!",
            "email_sent": "📧 E-mail envoyé"
        },
        "ar": {
            "weather": "🌤️ الطقس",
            "news": "📰 آخر الأخبار",
            "stock": "📊 سعر السهم",
            "crypto": "💰 سعر العملة",
            "no_data": "⚠️ لا توجد بيانات",
            "qr_generated": "✅ تم إنشاء رمز QR",
            "note_saved": "✅ تم حفظ الملاحظة",
            "reminder_set": "✅ تم تعيين التذكير",
            "game_start": "🎮 بدأت اللعبة!",
            "email_sent": "📧 تم إرسال البريد"
        },
        "es": {
            "weather": "🌤️ Clima",
            "news": "📰 Últimas noticias",
            "stock": "📊 Precio de acciones",
            "crypto": "💰 Precio crypto",
            "no_data": "⚠️ No hay datos",
            "qr_generated": "✅ Código QR generado",
            "note_saved": "✅ Nota guardada",
            "reminder_set": "✅ Recordatorio establecido",
            "game_start": "🎮 ¡Juego iniciado!",
            "email_sent": "📧 Correo enviado"
        },
        "de": {
            "weather": "🌤️ Wetter",
            "news": "📰 Aktuelle Nachrichten",
            "stock": "📊 Aktienkurs",
            "crypto": "💰 Kryptopreis",
            "no_data": "⚠️ Keine Daten",
            "qr_generated": "✅ QR-Code generiert",
            "note_saved": "✅ Notiz gespeichert",
            "reminder_set": "✅ Erinnerung gesetzt",
            "game_start": "🎮 Spiel gestartet!",
            "email_sent": "📧 E-Mail gesendet"
        },
        "zh": {
            "weather": "🌤️ 天气",
            "news": "📰 最新消息",
            "stock": "📊 股票价格",
            "crypto": "💰 加密货币价格",
            "no_data": "⚠️ 没有数据",
            "qr_generated": "✅ 二维码已生成",
            "note_saved": "✅ 笔记已保存",
            "reminder_set": "✅ 提醒已设置",
            "game_start": "🎮 游戏开始！",
            "email_sent": "📧 邮件已发送"
        }
    }
    return translations.get(lang, translations["sw"]).get(key, key)

# ==================== WEATHER ====================
def get_weather(city, lang="sw"):
    """Pata hali ya hewa kwa mji wowote"""
    if not WEATHER_API_KEY:
        return f"⚠️ {get_translation(lang, 'no_data')}. Weka WEATHER_API_KEY kwenye environment."
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang={lang[:2]}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            return f"""
            **{get_translation(lang, 'weather')} - {city.upper()}** 🌍
            🌡️ Joto: {temp}°C (Inahisika: {feels_like}°C)
            💧 Unyevu: {humidity}%
            🌬️ Upepo: {wind_speed} m/s
            📝 Hali: {description.capitalize()}
            """
        else:
            return f"⚠️ Mji '{city}' haupatikani. Jaribu tena."
    except Exception as e:
        return f"⚠️ Hitilafu: {str(e)}"

# ==================== NEWS ====================
def get_news(category="general", lang="sw"):
    """Pata habari za mwisho"""
    if not NEWS_API_KEY:
        return f"⚠️ {get_translation(lang, 'no_data')}. Weka NEWS_API_KEY kwenye environment."
    
    categories = {
        "general": "general", "tech": "technology", "sports": "sports",
        "business": "business", "entertainment": "entertainment", "health": "health"
    }
    
    cat = categories.get(category, "general")
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=tz&category={cat}&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])[:5]
            
            if not articles:
                # Jaribu dunia nzima
                url = f"https://newsapi.org/v2/top-headlines?category={cat}&apiKey={NEWS_API_KEY}"
                response = requests.get(url, timeout=10)
                data = response.json()
                articles = data.get('articles', [])[:5]
            
            if articles:
                result = f"**{get_translation(lang, 'news')}**\n\n"
                for i, article in enumerate(articles, 1):
                    title = article.get('title', 'No title')
                    source = article.get('source', {}).get('name', 'Unknown')
                    result += f"{i}. **{title[:100]}**\n   📰 {source}\n\n"
                return result
            else:
                return f"⚠️ Hakuna habari za {category} kwa sasa."
        else:
            return f"⚠️ Hitilafu ya API: {response.status_code}"
    except Exception as e:
        return f"⚠️ Hitilafu: {str(e)}"

# ==================== STOCK & CRYPTO ====================
def get_stock_price(symbol, lang="sw"):
    """Pata bei ya hisa au crypto"""
    if not YFINANCE_AVAILABLE:
        return f"⚠️ {get_translation(lang, 'no_data')}. Install yfinance."
    
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        if info:
            price = info.get('regularMarketPrice', info.get('currentPrice', 'N/A'))
            change = info.get('regularMarketChange', 0)
            change_percent = info.get('regularMarketChangePercent', 0)
            
            symbol_display = symbol.upper()
            if symbol_display in ['BTC-USD', 'ETH-USD', 'DOGE-USD']:
                return f"**{get_translation(lang, 'crypto')}**\n💰 {symbol_display}: ${price:,.2f}\n📈 Change: {change:+.2f} ({change_percent:+.2f}%)"
            else:
                return f"**{get_translation(lang, 'stock')}**\n📊 {symbol_display}: ${price:,.2f}\n📈 Change: {change:+.2f} ({change_percent:+.2f}%)"
        else:
            return f"⚠️ {symbol} haipatikani. Jaribu BTC-USD, AAPL, TSLA."
    except Exception as e:
        return f"⚠️ Hitilafu: {str(e)}"

# ==================== QR CODE GENERATOR ====================
def generate_qr_code(data, lang="sw"):
    """Tengeneza QR code"""
    if not QR_AVAILABLE:
        return f"⚠️ {get_translation(lang, 'no_data')}. Install qrcode pillow"
    
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    except Exception as e:
        return f"⚠️ Hitilafu: {str(e)}"

# ==================== SHORTEN URL ====================
def shorten_url(long_url, lang="sw"):
    """Fupisha link"""
    try:
        # Tumia TinyURL API (free, no key)
        response = requests.get(f"https://tinyurl.com/api-create.php?url={long_url}", timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            return long_url
    except:
        return long_url

# ==================== SEND EMAIL ====================
def send_email(to_email, subject, body, lang="sw"):
    """Tuma barua pepe (inahitaji SMTP configuration)"""
    # Hii ni template - kwa production, tumia SMTP
    return f"""
    📧 **Barua pepe imetayarishwa**
    📨 Kwa: {to_email}
    📝 Kichwa: {subject}
    📄 Ujumbe: {body[:200]}
    
    ✅ Kwa kutuma barua pepe halisi, weka SMTP settings kwenye environment.
    """

# ==================== GAMES ====================
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.winner = None
    
    def make_move(self, position):
        if self.board[position] == ' ' and not self.winner:
            self.board[position] = self.current_player
            self.check_winner()
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self):
        winning_combinations = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.winner = self.board[combo[0]]
                return
        if ' ' not in self.board:
            self.winner = 'Tie'
    
    def get_board_display(self):
        display = ""
        for i in range(0, 9, 3):
            display += f"{self.board[i] or i} | {self.board[i+1] or i+1} | {self.board[i+2] or i+2}\n"
            if i < 6:
                display += "---------\n"
        return display

games = {}

# ==================== NOTES & REMINDERS ====================
def save_note(user_id, title, content):
    notes = load_notes()
    if user_id not in notes:
        notes[user_id] = []
    notes[user_id].append({
        'id': str(uuid.uuid4()),
        'title': title,
        'content': content,
        'created_at': datetime.now().isoformat()
    })
    save_notes(notes)
    return True

def get_notes(user_id):
    notes = load_notes()
    return notes.get(user_id, [])

# ==================== MUSIC/YOUTUBE ====================
def search_youtube(query):
    """Tafuta video za YouTube"""
    try:
        # Tumia Invidious API (free, no key)
        response = requests.get(
            f"https://invidious.io.lol/api/v1/search?q={requests.utils.quote(query)}&type=video",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data[:5]:
                videos.append({
                    'title': item.get('title', 'No title'),
                    'url': f"https://youtube.com/watch?v={item.get('videoId', '')}",
                    'thumbnail': f"https://img.youtube.com/vi/{item.get('videoId', '')}/default.jpg"
                })
            return videos
    except:
        pass
    return []

# ==================== MAPS & DIRECTIONS ====================
def get_directions(origin, destination, lang="sw"):
    """Pata maelekezo ya njia"""
    try:
        # Tumia OpenStreetMap Nominatim (free, no key)
        # First get coordinates
        origin_url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(origin)}&format=json&limit=1"
        dest_url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(destination)}&format=json&limit=1"
        
        origin_resp = requests.get(origin_url, headers={'User-Agent': 'BrainAI'}, timeout=10)
        dest_resp = requests.get(dest_url, headers={'User-Agent': 'BrainAI'}, timeout=10)
        
        if origin_resp.status_code == 200 and dest_resp.status_code == 200:
            origin_data = origin_resp.json()
            dest_data = dest_resp.json()
            
            if origin_data and dest_data:
                origin_coords = f"{origin_data[0]['lat']},{origin_data[0]['lon']}"
                dest_coords = f"{dest_data[0]['lat']},{dest_data[0]['lon']}"
                
                # Get route from OSRM
                route_url = f"http://router.project-osrm.org/route/v1/driving/{origin_coords};{dest_coords}"
                route_resp = requests.get(route_url, timeout=10)
                
                if route_resp.status_code == 200:
                    route_data = route_resp.json()
                    if route_data.get('routes'):
                        distance_km = route_data['routes'][0]['distance'] / 1000
                        duration_min = route_data['routes'][0]['duration'] / 60
                        
                        return f"""
                        🗺️ **Maelekezo: {origin} → {destination}**
                        📏 Umbali: {distance_km:.1f} km
                        ⏱️ Muda: {duration_min:.0f} dakika
                        """
        
        return f"⚠️ {get_translation(lang, 'no_data')}. Hakuna maelekezo kwa {origin} → {destination}"
    except Exception as e:
        return f"⚠️ Hitilafu: {str(e)}"

# ==================== CUSTOM INSTRUCTIONS ====================
def get_custom_instructions(user_id):
    custom = session.get('custom_instructions', {})
    return custom.get(user_id, "Jibu kwa lugha safi na kwa heshima.")

# ==================== MAIN PROCESSING ====================
def process_with_ai(user_message, conversation_history, lang="sw"):
    """AI inachakata kila kitu"""
    
    msg_lower = user_message.lower()
    
    # 1. WEATHER
    if "hali ya hewa" in msg_lower or "weather" in msg_lower:
        city_match = re.search(r'(?:hali ya hewa|weather)\s+(\w+)', msg_lower)
        if city_match:
            return get_weather(city_match.group(1), lang)
        return get_weather("Dar es Salaam", lang)
    
    # 2. NEWS
    if "habari" in msg_lower or "news" in msg_lower:
        if "tech" in msg_lower or "technology" in msg_lower:
            return get_news("tech", lang)
        elif "sports" in msg_lower or "michezo" in msg_lower:
            return get_news("sports", lang)
        elif "business" in msg_lower or "biashara" in msg_lower:
            return get_news("business", lang)
        return get_news("general", lang)
    
    # 3. STOCK/CRYPTO
    if "bei ya" in msg_lower or "stock" in msg_lower or "crypto" in msg_lower:
        symbol_match = re.search(r'(?:bei ya|stock|crypto)\s+(\w+)', msg_lower)
        if symbol_match:
            return get_stock_price(symbol_match.group(1), lang)
        return get_stock_price("AAPL", lang)
    
    # 4. CALCULATOR
    if re.search(r'[\d\+\-\*\/\(\)]', user_message):
        try:
            result = eval(user_message.replace('^', '**'))
            return f"📊 **Matokeo:** {user_message} = {result}"
        except:
            pass
    
    # 5. QR CODE
    if "qr code" in msg_lower or "tengeneza qr" in msg_lower:
        data_match = re.search(r'(?:qr code|tengeneza qr)\s+(.+)', msg_lower)
        if data_match:
            qr_base64 = generate_qr_code(data_match.group(1), lang)
            if qr_base64.startswith("data:image"):
                return f"{get_translation(lang, 'qr_generated')}\n![QR Code]({qr_base64})"
            return qr_base64
        return "⚠️ Andika: tengeneza qr https://example.com"
    
    # 6. SHORTEN URL
    if "fupisha" in msg_lower or "shorten" in msg_lower:
        url_match = re.search(r'(?:fupisha|shorten)\s+(https?://[^\s]+)', msg_lower)
        if url_match:
            short = shorten_url(url_match.group(1), lang)
            return f"✅ Link fupi: {short}"
        return "⚠️ Andika: fupisha https://example.com"
    
    # 7. NOTES
    if "hifadhi maelezo" in msg_lower or "save note" in msg_lower:
        title_match = re.search(r'(?:hifadhi maelezo|save note)\s+(.+?)\s*-\s*(.+)', user_message)
        if title_match:
            save_note(session.get('user_id', 'default'), title_match.group(1), title_match.group(2))
            return f"✅ {get_translation(lang, 'note_saved')}: {title_match.group(1)}"
        return "⚠️ Andika: hifadhi maelezo Title - Content"
    
    # 8. GAMES - Tic Tac Toe
    if "tic tac toe" in msg_lower or "cheza" in msg_lower:
        game_id = session.get('game_id')
        if not game_id or game_id not in games:
            games[str(session.get('user_id'))] = TicTacToe()
            session['game_id'] = str(session.get('user_id'))
            game_id = session['game_id']
        
        game = games[game_id]
        # Check for move
        move_match = re.search(r'(\d+)', msg_lower)
        if move_match and int(move_match.group(1)) in range(9):
            game.make_move(int(move_match.group(1)))
        
        board = game.get_board_display()
        if game.winner:
            if game.winner == 'Tie':
                result = "🤝 Mchezo umefungana!\n" + board
            else:
                result = f"🏆 {game.winner} ameshinda!\n" + board
            del games[game_id]
            session.pop('game_id', None)
        else:
            result = f"🎮 Mchezo umeanza! {game.current_player} anacheza.\n{board}\nChagua namba 0-8"
        
        return result
    
    # 9. EMAIL
    if "tuma barua" in msg_lower or "send email" in msg_lower:
        email_match = re.search(r'(?:tuma barua|send email)\s+(\S+@\S+)\s+(.+?)\s*-\s*(.+)', user_message)
        if email_match:
            return send_email(email_match.group(1), email_match.group(2), email_match.group(3), lang)
        return "⚠️ Andika: tuma barua email@example.com Subject - Message"
    
    # 10. MUSIC/YOUTUBE
    if "cheza" in msg_lower or "play" in msg_lower:
        query = user_message.replace("cheza", "").replace("play", "").strip()
        if query:
            videos = search_youtube(query)
            if videos:
                result = f"🎵 **Matokeo ya YouTube:**\n\n"
                for i, v in enumerate(videos, 1):
                    result += f"{i}. [{v['title'][:50]}]({v['url']})\n"
                return result
        return "⚠️ Hakuna matokeo"
    
    # 11. MAPS
    if "maelekezo" in msg_lower or "directions" in msg_lower:
        match = re.search(r'(?:maelekezo|directions)\s+(\w+)\s+to\s+(\w+)', msg_lower)
        if not match:
            match = re.search(r'(?:maelekezo|directions)\s+(\w+)\s*-\s*(\w+)', msg_lower)
        if match:
            return get_directions(match.group(1), match.group(2), lang)
        return "⚠️ Andika: maelekezo Dar to Morogoro"
    
    # 12. WEB SEARCH
    if "tafuta" in msg_lower or "search" in msg_lower:
        query = user_message.replace("tafuta", "").replace("search", "").strip()
        if WEB_SEARCH_AVAILABLE:
            try:
                results = []
                for url in search(query, num_results=3):
                    results.append(f"• {url}")
                if results:
                    return f"**🔍 Matokeo ya utafutaji:**\n\n" + "\n".join(results)
            except:
                pass
        return "⚠️ Web search haipo. Install googlesearch-python"
    
    # DEFAULT - USE GROQ
    if GROQ_KEY:
        try:
            custom_instructions = get_custom_instructions(session.get('user_id', 'default'))
            messages = [
                {"role": "system", "content": f"{LANGUAGES.get(lang, LANGUAGES['sw'])['name']}\n{custom_instructions}"}
            ]
            for msg in conversation_history[-15:]:
                if msg.get('role') in ['user', 'assistant']:
                    messages.append({"role": msg['role'], "content": msg.get('content', '')[:500]})
            messages.append({"role": "user", "content": user_message})
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
                json={"model": "mixtral-8x7b-32768", "messages": messages, "temperature": 0.7, "max_tokens": 1024},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"🚨 Hitilafu: {str(e)}"
    
    return "🔴 Samahani, kuna tatizo. Jaribu tena baadaye."

# ==================== HTML CODE ====================
HTML_CODE = '''
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Brain AI Pro Ultimate - 25 Features</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --bg: #f8fafc;
            --white: #ffffff;
            --green: #10b981;
            --user-bg: #d1fae5;
            --text: #1f2937;
            --border: #e5e7eb;
            --red: #ef4444;
            --yellow: #f59e0b;
            --blue: #3b82f6;
            --purple: #8b5cf6;
            --pink: #ec4899;
        }
        body.dark-mode {
            --bg: #0f172a;
            --white: #1e293b;
            --green: #34d399;
            --user-bg: #064e3b;
            --text: #f3f4f6;
            --border: #374151;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Outfit', sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: 0.3s;
        }
        .header {
            padding: 10px 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--white);
            border-bottom: 3px solid var(--green);
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }
        .header h3 { font-family: 'Dancing Script'; font-size: 20px; color: var(--green); }
        .sidebar {
            height: 100%;
            width: 0;
            position: fixed;
            z-index: 2000;
            top: 0;
            background: var(--white);
            overflow-x: hidden;
            transition: 0.3s;
            padding-top: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }
        .sidebar.left { left: 0; border-right: 3px solid var(--green); }
        .sidebar.right { right: 0; border-left: 3px solid var(--green); }
        .sidebar a, .sidebar .history-item {
            padding: 10px 15px;
            text-decoration: none;
            font-size: 13px;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            transition: 0.2s;
        }
        .sidebar a:hover, .sidebar .history-item:hover { background: var(--green); color: white; }
        .closebtn { font-size: 28px; cursor: pointer; color: var(--green); padding: 0 15px; }
        #main-view {
            flex: 1;
            margin-top: 115px;
            margin-bottom: 70px;
            padding: 10px;
            overflow-y: auto;
        }
        .chat-wrapper { display: flex; flex-direction: column; gap: 8px; }
        .msg {
            max-width: 85%;
            padding: 10px 14px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
            word-wrap: break-word;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-msg { align-self: flex-end; background: var(--user-bg); border-bottom-right-radius: 5px; }
        .ai-msg { align-self: flex-start; background: var(--white); border-bottom-left-radius: 5px; border-left: 4px solid var(--green); }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 8px;
            background: var(--bg);
            border-top
