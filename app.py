from flask import Flask, render_template_string, request, redirect, session
import random, string, requests, os, urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MEMBER_CODE = "123567"
MY_DOMAIN = "https://sever-key-alexcloud-cheat.onrender.com"
all_keys = []
GAMES = ["FREE FIRE MAX", "FREE FIRE"]
DURATIONS = ["12 Giờ", "1 Ngày"]

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    @keyframes colorChange { 0%{color: #ff0000;} 50%{color: #0000ff;} 100%{color: #ff0000;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
    .card { background: rgba(255,255,255,0.98); padding: 30px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); width: 90%; max-width: 450px; text-align: center; }
    h1 { font-size: 2.2rem; animation: colorChange 4s infinite; font-weight: 800; margin-bottom: 20px; }
    .btn { background: #000; color: #fff; padding: 15px; border-radius: 12px; cursor: pointer; font-size: 1.2rem; font-weight: bold; width: 100%; border: none; margin-top: 15px; transition: 0.3s; text-decoration: none; display: block; }
    .btn:hover { transform: scale(1.02); background: #222; }
    select, input { font-size: 1rem; padding: 12px; width: 100%; margin-top: 10px; border-radius: 10px; border: 2px solid #eee; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; font-size: 0.8rem; border-radius: 10px; overflow: hidden; }
    th, td { border: 1px solid #eee; padding: 8px; text-align: center; color: #000; }
    th { background: #000; color: #fff; }
</style>
"""

def get_html(content):
    return f"<html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head><body onclick=\"document.getElementById('bgMusic').play()\"><audio id='bgMusic' loop><source src='https://files.catbox.moe/mcy4cu.mp3' type='audio/mpeg'></audio><div class='card'>{content}</div></body></html>"

@app.route('/')
def home():
    game_opts = "".join([f"<option value='{g}'>{g}</option>" for g in GAMES])
    time_opts = "".join([f"<option value='{d}'>{d}</option>" for d in DURATIONS])
    content = f"<h1>AlexCloud Cheat</h1><select id='game'>{game_opts}</select><select id='duration'>{time_opts}</select><button class='btn' onclick=\"window.location.href='/get-key?game='+document.getElementById('game').value+'&dur='+document.getElementById('duration').value\">NHẬN KEY</button>"
    return render_template_string(get_html(content))

@app.route('/get-key')
def get_key():
    game = request.args.get('game', 'FREE FIRE MAX')
    dur = request.args.get('dur', '1 Ngày')
    code = request.args.get('member_code')
    
    if code == MEMBER_CODE:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        all_keys.append({'key': k, 'game': game, 'exp': dur, 'time': datetime.now().strftime("%H:%M:%S")})
        return redirect(f"/verify?key={k}&dur={dur}")
    
    html = f"<h1>Xác thực</h1><form action='/get-key' method='GET'><input type='hidden' name='game' value='{game}'><input type='hidden' name='dur' value='{dur}'><input type='password' name='member_code' placeholder='Mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><a href='/get-key-link?game={game}&dur={dur}' class='btn' style='background:#d9534f'>VƯỢT LINK</a>"
    return render_template_string(get_html(html))

@app.route('/get-key-link')
def get_key_link():
    game = request.args.get('game')
    dur = request.args.get('dur')
    k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
    all_keys.append({'key': k, 'game': game, 'exp': dur, 'time': datetime.now().strftime("%H:%M:%S")})
    target_url = f"{MY_DOMAIN}/verify?key={k}&dur={dur}"
    api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={urllib.parse.quote(target_url)}"
    try:
        response = requests.get(api_url, timeout=10).json()
        return redirect(response['shortenedUrl'])
    except: return "Lỗi API, vui lòng thử lại!"

@app.route('/verify')
def verify():
    k = request.args.get('key')
    dur = request.args.get('dur')
    return render_template_string(get_html(f"<h1>KEY CỦA BẠN:</h1><h1 style='color:red'>{k}</h1><p>Thời hạn: <b>{dur}</b></p><a href='/'>Về trang chủ</a>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('pin') == ADMIN_PIN: session['admin'] = True
    if session.get('admin'):
        rows = "".join([f"<tr><td>{i['key']}</td><td>{i['game']}</td><td>{i['exp']}</td><td>{i['time']}</td></tr>" for i in all_keys])
        return render_template_string(get_html(f"<h1>ADMIN</h1><table><tr><th>KEY</th><th>GAME</th><th>HẠN</th><th>LÚC TẠO</th></tr>{rows}</table><br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    return render_template_string(get_html("<h1>NHẬP PIN</h1><form method='POST'><input name='pin' type='password'><button class='btn'>XÁC NHẬN</button></form>"))

@app.route('/admin-logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
