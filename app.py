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

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
    .card { background: rgba(255,255,255,0.98); padding: 30px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); width: 90%; max-width: 450px; text-align: center; }
    h1 { font-size: 1.8rem; color: #000; font-weight: 800; margin-bottom: 20px; }
    .btn { background: #000; color: #fff; padding: 12px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; border: none; margin-top: 10px; display: block; text-decoration: none; transition: 0.3s; }
    .btn:hover { transform: scale(1.02); background: #333; }
    input, select { width: 100%; padding: 10px; margin: 5px 0; border-radius: 8px; border: 1px solid #ccc; box-sizing: border-box; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.7rem; background: #fff; border-radius: 10px; overflow: hidden; }
    th, td { border: 1px solid #ddd; padding: 6px; color: #000; text-align: center; }
    th { background: #000; color: #fff; }
</style>
"""

def get_html(content):
    return f"<html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head><body onclick=\"document.getElementById('bgMusic').play()\"><audio id='bgMusic' loop><source src='https://files.catbox.moe/mcy4cu.mp3' type='audio/mpeg'></audio><div class='card'>{content}</div></body></html>"

@app.route('/')
def home():
    game_opts = "".join([f"<option value='{g}'>{g}</option>" for g in GAMES])
    return render_template_string(get_html(f"<h1>AlexCloud Cheat</h1><select id='game'>{game_opts}</select><button class='btn' onclick=\"window.location.href='/get-key?game='+document.getElementById('game').value\">NHẬN KEY</button><br><a href='/admin-login' style='color:#000'>Admin Panel</a>"))

@app.route('/get-key')
def get_key():
    game = request.args.get('game', 'FREE FIRE MAX')
    code = request.args.get('member_code')
    if code == MEMBER_CODE:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}"
        all_keys.append({'key': k, 'game': game, 'tbi': '1', 'day': '1', 'time': datetime.now().strftime("%H:%M")})
        return redirect(f"/verify?key={k}")
    return render_template_string(get_html(f"<h1>Xác thực</h1><form action='/get-key' method='GET'><input type='hidden' name='game' value='{game}'><input type='password' name='member_code' placeholder='Mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><a href='/get-key-link?game={game}' class='btn' style='background:#d9534f'>VƯỢT LINK</a>"))

@app.route('/get-key-link')
def get_key_link():
    game = request.args.get('game')
    k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}"
    all_keys.append({'key': k, 'game': game, 'tbi': '1', 'day': '1', 'time': datetime.now().strftime("%H:%M")})
    target_url = f"{MY_DOMAIN}/verify?key={k}"
    try:
        response = requests.get(f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={urllib.parse.quote(target_url)}", timeout=10).json()
        return redirect(response['shortenedUrl'])
    except: return "Lỗi API!"

@app.route('/verify')
def verify():
    return render_template_string(get_html(f"<h1>KEY: {request.args.get('key')}</h1><a href='/' class='btn'>VỀ TRANG CHỦ</a>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('pin') == ADMIN_PIN: session['admin'] = True
        elif session.get('admin') and request.form.get('create'):
            all_keys.append({'key': f"AlexCloud-{request.form.get('key_name')}", 'game': request.form.get('game'), 'tbi': request.form.get('tbi'), 'day': request.form.get('day'), 'time': datetime.now().strftime("%H:%M")})
    
    if session.get('admin'):
        rows = "".join([f"<tr><td>{i['key']}</td><td>{i['tbi']}</td><td>{i['day']}</td><td>{i['time']}</td></tr>" for i in all_keys])
        form = "<form method='POST'><input name='key_name' placeholder='Tên key...' required><select name='game'><option>FREE FIRE</option></select><input name='tbi' placeholder='TBI' required><input name='day' placeholder='Ngày' required><button name='create' value='1' class='btn'>TẠO</button></form>"
        return render_template_string(get_html(f"<h1>ADMIN</h1>{form}<table><tr><th>KEY</th><th>TBI</th><th>D</th><th>TIME</th></tr>{rows}</table><br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    return render_template_string(get_html("<h1>NHẬP PIN</h1><form method='POST'><input name='pin' type='password'><button class='btn'>XÁC NHẬN</button></form>"))

@app.route('/admin-logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
