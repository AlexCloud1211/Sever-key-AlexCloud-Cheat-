from flask import Flask, render_template_string, request, redirect
import random, string, requests, urllib.parse
from datetime import datetime
import os

app = Flask(__name__)

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
all_keys = []
GAMES = ["FREE FIRE MAX", "FREE FIRE"]
DURATIONS = ["12 Giờ", "1 Ngày"]

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
    .card { background: rgba(255,255,255,0.98); padding: 40px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); width: 90%; max-width: 450px; text-align: center; }
    h1 { font-size: 2.8rem; font-weight: 800; margin-bottom: 20px; }
    .btn { background: #000; color: #fff; padding: 18px; border-radius: 12px; cursor: pointer; font-size: 1.4rem; font-weight: bold; width: 100%; border: none; margin-top: 25px; transition: 0.3s; }
    .btn:hover { transform: scale(1.02); background: #222; }
    select { font-size: 1.1rem; padding: 12px; width: 100%; margin-top: 15px; border-radius: 10px; border: 2px solid #eee; outline: none; }
</style>
"""

def get_html(content):
    return f"<html><head><meta charset='UTF-8'>{CSS}</head><body><div class='card'>{content}</div></body></html>"

@app.route('/')
def home():
    game_opts = "".join([f"<option value='{g}'>{g}</option>" for g in GAMES])
    time_opts = "".join([f"<option value='{d}'>{d}</option>" for d in DURATIONS])
    content = f"<h1>AlexCloud</h1><select id='game'>{game_opts}</select><select id='duration'>{time_opts}</select><button class='btn' onclick=\"window.location.href='/get-key?game='+document.getElementById('game').value+'&dur='+document.getElementById('duration').value\">NHẬN KEY</button>"
    return render_template_string(get_html(content))

@app.route('/get-key')
def get_key():
    game = request.args.get('game', 'FREE FIRE MAX')
    dur = request.args.get('dur', '1 Ngày')
    k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
    all_keys.append({'key': k, 'game': game, 'dev': '1', 'exp': dur, 'time': datetime.now().strftime("%H:%M:%S")})
    
    # URL bạn muốn người dùng truy cập sau khi vượt link
    target_url = f"https://alexcloud-ukf8.onrender.com/verify?key={k}&dur={dur}"
    
    # API của link4m
    api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={urllib.parse.quote(target_url)}"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if 'shortenedUrl' in data:
            return redirect(data['shortenedUrl'])
        return "Lỗi API: Không lấy được link!"
    except Exception as e:
        return f"Lỗi hệ thống: {str(e)}"

@app.route('/verify')
def verify():
    k = request.args.get('key')
    dur = request.args.get('dur', '1 Ngày')
    return render_template_string(get_html(f"<h1>KEY CỦA BẠN:</h1><h1 style='color:red'>{k}</h1><p>Thời hạn: {dur}</p><a href='/' class='btn'>Về trang chủ</a>"))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
