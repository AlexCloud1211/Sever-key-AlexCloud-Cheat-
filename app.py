from flask import Flask, render_template_string, request, redirect
import random, requests, os

app = Flask(__name__)

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
all_keys = []
GAMES = ["FREE FIRE MAX", "FREE FIRE"]
DURATIONS = ["12 Giờ", "1 Ngày"]

# CSS UI chuyên nghiệp, hiện đại, tối ưu cho mobile
CSS = """
<style>
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    body { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e); background-size: 400% 400%; animation: gradient 15s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; color: white; }
    .box { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; width: 320px; text-align: center; backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37); }
    .btn { background: linear-gradient(to right, #6a11cb, #2575fc); color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; cursor: pointer; font-weight: bold; margin-top: 15px; transition: 0.3s; }
    .btn:hover { transform: scale(1.05); filter: brightness(1.2); }
    select { width: 100%; padding: 12px; margin-top: 10px; border-radius: 8px; background: rgba(255,255,255,0.9); border: none; }
    .key-display { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; font-family: monospace; font-size: 1.2rem; color: #00ffcc; margin: 15px 0; border: 1px dashed #00ffcc; }
</style>
"""

def get_html(content):
    return f"""<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head>
    <body>
    <audio id='bgMusic' loop><source src='https://files.catbox.moe/5rqwul.mp3' type='audio/mpeg'></audio>
    <script>document.body.addEventListener('click', () => {{ document.getElementById('bgMusic').play(); }}, {{ once: true }});</script>
    <div class='box'>{content}</div></body></html>"""

@app.route('/')
def home():
    games = "".join([f"<option>{g}</option>" for g in GAMES])
    durs = "".join([f"<option>{d}</option>" for d in DURATIONS])
    return render_template_string(get_html(f"<h1>ALEXCLOUD</h1><select id='g'>{games}</select><select id='d'>{durs}</select><button class='btn' onclick=\"location.href='/get-key?g='+document.getElementById('g').value+'&d='+document.getElementById('d').value\">NHẬN KEY</button>"))

@app.route('/get-key')
def get_key():
    k = f"AlexCloud-{random.randint(1000,9999)}"
    all_keys.append({'key': k, 'game': request.args.get('g'), 'dur': request.args.get('d')})
    api = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url=https://alexcloud-ukf8.onrender.com/verify?key={k}&dur={request.args.get('d')}"
    try: return redirect(requests.get(api, timeout=5).json()['shortenedUrl'])
    except: return "Lỗi hệ thống!"

@app.route('/verify')
def verify():
    k = request.args.get('key')
    d = request.args.get('dur')
    return render_template_string(get_html(f"<h3>KEY CỦA BẠN</h3><div class='key-display'>{k}</div><p>Hạn dùng: {d}</p><button class='btn' onclick='navigator.clipboard.writeText(\"{k}\"); alert(\"Đã copy Key!\")'>COPY KEY</button><br><br><a href='/' style='color:#ccc; font-size:0.8rem'>Quay lại</a>"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, render_template_string, request, redirect
import random, requests, os

app = Flask(__name__)

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
all_keys = []
GAMES = ["FREE FIRE MAX", "FREE FIRE"]
DURATIONS = ["12 Giờ", "1 Ngày"]

# CSS UI chuyên nghiệp, hiện đại, tối ưu cho mobile
CSS = """
<style>
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    body { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e); background-size: 400% 400%; animation: gradient 15s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; color: white; }
    .box { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; width: 320px; text-align: center; backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37); }
    .btn { background: linear-gradient(to right, #6a11cb, #2575fc); color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; cursor: pointer; font-weight: bold; margin-top: 15px; transition: 0.3s; }
    .btn:hover { transform: scale(1.05); filter: brightness(1.2); }
    select { width: 100%; padding: 12px; margin-top: 10px; border-radius: 8px; background: rgba(255,255,255,0.9); border: none; }
    .key-display { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; font-family: monospace; font-size: 1.2rem; color: #00ffcc; margin: 15px 0; border: 1px dashed #00ffcc; }
</style>
"""

def get_html(content):
    return f"""<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head>
    <body>
    <audio id='bgMusic' loop><source src='https://files.catbox.moe/5rqwul.mp3' type='audio/mpeg'></audio>
    <script>document.body.addEventListener('click', () => {{ document.getElementById('bgMusic').play(); }}, {{ once: true }});</script>
    <div class='box'>{content}</div></body></html>"""

@app.route('/')
def home():
    games = "".join([f"<option>{g}</option>" for g in GAMES])
    durs = "".join([f"<option>{d}</option>" for d in DURATIONS])
    return render_template_string(get_html(f"<h1>ALEXCLOUD</h1><select id='g'>{games}</select><select id='d'>{durs}</select><button class='btn' onclick=\"location.href='/get-key?g='+document.getElementById('g').value+'&d='+document.getElementById('d').value\">NHẬN KEY</button>"))

@app.route('/get-key')
def get_key():
    k = f"AlexCloud-{random.randint(1000,9999)}"
    all_keys.append({'key': k, 'game': request.args.get('g'), 'dur': request.args.get('d')})
    api = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url=https://alexcloud-ukf8.onrender.com/verify?key={k}&dur={request.args.get('d')}"
    try: return redirect(requests.get(api, timeout=5).json()['shortenedUrl'])
    except: return "Lỗi hệ thống!"

@app.route('/verify')
def verify():
    k = request.args.get('key')
    d = request.args.get('dur')
    return render_template_string(get_html(f"<h3>KEY CỦA BẠN</h3><div class='key-display'>{k}</div><p>Hạn dùng: {d}</p><button class='btn' onclick='navigator.clipboard.writeText(\"{k}\"); alert(\"Đã copy Key!\")'>COPY KEY</button><br><br><a href='/' style='color:#ccc; font-size:0.8rem'>Quay lại</a>"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
