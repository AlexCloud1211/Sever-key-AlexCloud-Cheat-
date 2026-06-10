from flask import Flask, render_template_string, request, redirect, session
import random, string, requests, os, urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MEMBER_CODE = "123567"
MY_DOMAIN = "https://sever-key-alexcloud-cheat.onrender.com"
all_keys = []

def generate_unique_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not any(item['key'] == k for item in all_keys): return k

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: sans-serif; display: flex; flex-direction: column; min-height: 100vh; margin: 0; padding: 20px; align-items: center; }
    .tg-btn { position: absolute; top: 15px; right: 15px; width: 35px; height: 35px; }
    .content-wrapper { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
    .card { background: rgba(255,255,255,0.95); padding: 30px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; }
    .btn { background: #000; color: #fff; padding: 12px; border-radius: 10px; cursor: pointer; font-weight: bold; width: 100%; border: none; margin-top: 15px; display: block; text-decoration: none; }
    #keyBox { color: red; font-size: 1.5rem; cursor: pointer; border: 2px dashed red; padding: 10px; border-radius: 10px; margin: 15px 0; }
    footer { padding: 20px; color: #fff; font-weight: bold; }
    footer a { color: #fff; text-decoration: none; }
    .info-box { font-weight: bold; font-size: 1.2rem; color: #333; margin: 10px 0; }
</style>
"""

def get_html(content):
    tg_icon = """<a href='https://t.me/AlexCloud3' class='tg-btn'><svg viewBox='0 0 24 24' fill='#fff'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.07-.19-.05-.27-.03-.12.02-1.93 1.23-5.45 3.62-.51.35-.98.52-1.39.51-.46-.01-1.35-.26-2.01-.48-.81-.27-1.46-.41-1.4-.85.03-.23.35-.47 1.01-.71 3.93-1.72 6.55-2.86 7.85-3.41 3.74-1.59 4.52-1.86 5.02-1.87.11 0 .37.03.54.17.14.12.19.28.21.45-.02.07-.03.14-.05.21z'/></svg></a>"""
    return f"""<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'>{CSS}</head>
    <body>
        {tg_icon}
        <audio autoplay loop><source src='https://files.catbox.moe/mcy4cu.mp3'></audio>
        <div class='content-wrapper'><div class='card'>{content}</div></div>
        <footer><a href='/admin-login'>@2026 AlexCloud</a></footer>
    </body></html>"""

@app.route('/')
def home():
    content = """
    <h1>AlexCloud Cheat</h1>
    <div class='info-box'>Game: Free Fire</div>
    <div class='info-box'>Thời hạn: 1 Ngày</div>
    <a href='/get-key' class='btn'>NHẬN KEY NGAY</a>
    """
    return render_template_string(get_html(content))

@app.route('/get-key')
def get_key():
    code = request.args.get('member_code')
    if code == MEMBER_CODE:
        k = generate_unique_key()
        all_keys.append({'key': k, 'tbi': '1', 'day': '1', 'time': datetime.now().strftime("%H:%M")})
        return redirect(f"/verify?key={k}")
    return render_template_string(get_html("<h1>Xác thực</h1><form action='/get-key' method='GET'><input name='member_code' placeholder='Mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><a href='/get-key-link' class='btn' style='background:#d9534f'>VƯỢT LINK</a>"))

@app.route('/get-key-link')
def get_key_link():
    k = generate_unique_key()
    all_keys.append({'key': k, 'tbi': '1', 'day': '1', 'time': datetime.now().strftime("%H:%M")})
    target_url = f"{MY_DOMAIN}/verify?key={k}"
    try:
        res = requests.get(f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={urllib.parse.quote(target_url)}", timeout=10).json()
        return redirect(res['shortenedUrl'])
    except: return "Lỗi API!"

@app.route('/verify')
def verify():
    k = request.args.get('key')
    return render_template_string(get_html(f"<h1>KEY:</h1><h2 id='keyBox' onclick='navigator.clipboard.writeText(\"{k}\");alert(\"Đã copy\");'>{k}</h2><p>(Nhấn vào Key để copy)</p><a href='/' class='btn'>VỀ TRANG CHỦ</a>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('pin') == ADMIN_PIN: session['admin'] = True
        elif session.get('admin') and request.form.get('create'):
            all_keys.append({'key': generate_unique_key(), 'tbi': request.form.get('tbi'), 'day': request.form.get('day'), 'time': datetime.now().strftime("%H:%M")})
    if session.get('admin'):
        rows = "".join([f"<tr><td>{i['key']}</td><td>{i['tbi']}</td><td>{i['day']}</td><td>{i['time']}</td></tr>" for i in all_keys])
        form = "<form method='POST'><input name='tbi' placeholder='TBI' required><input name='day' placeholder='Ngày' required><button name='create' value='1' class='btn'>TẠO KEY</button></form>"
        return render_template_string(get_html(f"<h1>LOG ADMIN</h1>{form}<table><tr><th>KEY</th><th>TBI</th><th>D</th><th>TIME</th></tr>{rows}</table><br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    return render_template_string(get_html("<h1>ADMIN</h1><form method='POST'><input name='pin' type='password'><button class='btn'>ĐĂNG NHẬP</button></form>"))

@app.route('/admin-logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
