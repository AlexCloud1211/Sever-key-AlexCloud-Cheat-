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

# Dữ liệu ngôn ngữ cho toàn bộ các trang
LANGS = {
    'VN': {
        'title': 'AlexCloud Cheat', 'game': 'Game: Free Fire', 'time': 'Thời hạn: 1 Ngày', 
        'btn': 'GET KEY', 'copy': '(Nhấn vào Key để copy)', 'status': 'Trạng thái: Online',
        'auth_title': 'Xác thực', 'auth_input': 'Mã thành viên...', 'auth_btn': 'XÁC NHẬN', 
        'link_btn': 'VƯỢT LINK', 'key_title': 'KEY CỦA BẠN:', 'back': 'VỀ TRANG CHỦ'
    },
    'EN': {
        'title': 'AlexCloud Cheat', 'game': 'Game: Free Fire', 'time': 'Duration: 1 Day', 
        'btn': 'GET KEY', 'copy': '(Click Key to copy)', 'status': 'Status: Online',
        'auth_title': 'Authentication', 'auth_input': 'Member code...', 'auth_btn': 'CONFIRM', 
        'link_btn': 'BYPASS LINK', 'key_title': 'YOUR KEY:', 'back': 'BACK TO HOME'
    }
}

def get_l():
    return LANGS.get(session.get('lang', 'VN'), LANGS['VN'])

def generate_unique_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not any(item['key'] == k for item in all_keys): return k

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; min-height: 100vh; margin: 0; padding: 20px; align-items: center; }
    .top-bar { position: absolute; top: 15px; right: 15px; display: flex; align-items: center; gap: 12px; z-index: 100; }
    .flag { font-size: 20px; cursor: pointer; text-decoration: none; }
    .tg-icon { width: 32px; height: 32px; fill: #fff; filter: drop-shadow(0 0 2px #000); }
    .content-wrapper { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
    .card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .btn { background: #000; color: #fff; padding: 15px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; border: none; margin-top: 15px; display: block; text-decoration: none; transition: 0.3s; }
    .btn:hover { background: #333; transform: scale(1.02); }
    #keyBox { color: #d00; font-size: 1.6rem; cursor: pointer; border: 2px dashed #d00; padding: 12px; border-radius: 10px; margin: 15px 0; font-weight: bold; }
    footer { padding: 20px; color: #fff; font-weight: bold; text-shadow: 1px 1px 2px #000; }
    footer a { color: #fff; text-decoration: none; }
    .info-box { font-weight: bold; font-size: 1.1rem; color: #333; margin: 5px 0; }
    .status-badge { display: inline-block; padding: 5px 15px; border-radius: 20px; background: #28a745; color: white; font-size: 0.8rem; margin-bottom: 10px; }
</style>
"""

def get_html(content):
    tg_svg = """<a href='https://t.me/AlexCloud3' target='_blank'><svg class='tg-icon' viewBox='0 0 24 24'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.07-.19-.05-.27-.03-.12.02-1.93 1.23-5.45 3.62-.51.35-.98.52-1.39.51-.46-.01-1.35-.26-2.01-.48-.81-.27-1.46-.41-1.4-.85.03-.23.35-.47 1.01-.71 3.93-1.72 6.55-2.86 7.85-3.41 3.74-1.59 4.52-1.86 5.02-1.87.11 0 .37.03.54.17.14.12.19.28.21.45-.02.07-.03.14-.05.21z'/></svg></a>"""
    js = "<script>function copyKey(){var k=document.getElementById('keyBox').innerText;navigator.clipboard.writeText(k);alert('Copy: '+k);}</script>"
    return f"""<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'>{CSS}</head>
    <body>
        <div class='top-bar'><a href='/lang/VN' class='flag'>🇻🇳</a><a href='/lang/EN' class='flag'>🇬🇧</a>{tg_svg}</div>
        <audio autoplay loop><source src='https://files.catbox.moe/mcy4cu.mp3'></audio>
        <div class='content-wrapper'><div class='card'><div class='status-badge'>● System Online</div>{content}</div></div>
        <footer><a href='/admin-login'>@2026 AlexCloud</a></footer>{js}
    </body></html>"""

@app.route('/lang/<lang>')
def set_lang(lang):
    session['lang'] = lang
    return redirect(request.referrer or '/')

@app.route('/')
def home():
    l = get_l()
    return render_template_string(get_html(f"<h1>{l['title']}</h1><div class='info-box'>{l['game']}</div><div class='info-box'>{l['time']}</div><p style='color:green; font-weight:bold'>{l['status']}</p><a href='/get-key' class='btn'>{l['btn']}</a>"))

@app.route('/get-key')
def get_key():
    l = get_l()
    code = request.args.get('member_code')
    if code == MEMBER_CODE:
        k = generate_unique_key()
        all_keys.append({'key': k, 'tbi': '1', 'day': '1', 'time': datetime.now().strftime("%H:%M")})
        return redirect(f"/verify?key={k}")
    return render_template_string(get_html(f"<h1>{l['auth_title']}</h1><form action='/get-key' method='GET'><input name='member_code' placeholder='{l['auth_input']}' required><button class='btn'>{l['auth_btn']}</button></form><a href='/get-key-link' class='btn' style='background:#d9534f'>{l['link_btn']}</a>"))

@app.route('/verify')
def verify():
    l = get_l()
    k = request.args.get('key')
    return render_template_string(get_html(f"<h1>{l['key_title']}</h1><h2 id='keyBox' onclick='copyKey()'>{k}</h2><p>{l['copy']}</p><a href='/' class='btn'>{l['back']}</a>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('pin') == ADMIN_PIN: session['admin'] = True
        elif session.get('admin') and request.form.get('create'):
            all_keys.append({'key': generate_unique_key(), 'tbi': request.form.get('tbi'), 'day': request.form.get('day'), 'time': datetime.now().strftime("%H:%M")})
    if session.get('admin'):
        rows = "".join([f"<tr><td>{i['key']}</td><td>{i['tbi']}</td><td>{i['day']}</td><td>{i['time']}</td></tr>" for i in all_keys])
        return render_template_string(get_html(f"<h1>LOG ADMIN</h1><form method='POST'><input name='tbi' placeholder='TBI' required><input name='day' placeholder='Ngày' required><button name='create' value='1' class='btn'>TẠO KEY</button></form><table><tr><th>KEY</th><th>TBI</th><th>D</th><th>TIME</th></tr>{rows}</table><br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    return render_template_string(get_html("<h1>ADMIN</h1><form method='POST'><input name='pin' type='password'><button class='btn'>ĐĂNG NHẬP</button></form>"))

@app.route('/admin-logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
