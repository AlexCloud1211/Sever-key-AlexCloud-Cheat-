from flask import Flask, render_template_string, request, redirect, session
import random, string, os, requests, urllib.parse
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MEMBER_CODE = "123567"
MY_DOMAIN = "https://sever-key-alexcloud-cheat.onrender.com"
all_keys = []

# --- HÀM ---
def get_vn_time(): 
    # Trả về chuỗi thời gian HH:MM:SS
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M:%S")

def get_bypass_link():
    ts = random.randint(100000, 999999)
    dest = f"{MY_DOMAIN}/get-key?auto_key=true&_={ts}"
    try:
        url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={urllib.parse.quote(dest)}"
        return requests.get(url, timeout=3).json().get('shortenedUrl', '#')
    except: return "#"

def generate_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not any(i['key'] == k for i in all_keys): return k

# --- UI TỐI ƯU ---
UI = """
<style>
    body { margin:0; background: #000; font-family: sans-serif; color: #fff; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
    .card { background: #1a1a1a; padding: 20px; border-radius: 15px; width: 90%; max-width: 400px; text-align: center; margin-top: 50px; border: 1px solid #333; }
    .btn { background: #fff; color: #000; padding: 12px; border-radius: 8px; font-weight: bold; width: 100%; border: none; margin-top: 10px; cursor: pointer; text-decoration: none; display: block; }
    .btn-red { background: #ff4d4d; color: #fff; }
    .key-box { color: #00ff00; font-size: 1.4rem; border: 1px dashed #00ff00; padding: 10px; margin: 15px 0; cursor: pointer; }
    .time-text { color: #aaa; font-size: 0.9rem; margin-top: 5px; }
</style>
<script>
    function copyText(val) {
        navigator.clipboard.writeText(val);
        alert('Đã sao chép Key!');
    }
</script>
"""

def render_layout(content):
    return render_template_string(f"""
    <html><head>
    <meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    {UI}</head><body>
    <div style='position:fixed; top:10px; right:10px;'><a href='https://t.me/AlexCloud3' style='color:#fff; font-size:24px;'><i class='fab fa-telegram'></i></a></div>
    <div class='card'>{content}</div>
    </body></html>""")

# --- ROUTES ---
@app.route('/')
def home():
    return render_layout("<h1>AlexCloud Cheat</h1><a href='/get-key' class='btn'>GET KEY</a>")

@app.route('/get-key', methods=['GET', 'POST'])
def get_key():
    if request.args.get('auto_key'):
        k = generate_key()
        t = get_vn_time()
        all_keys.append({'key': k, 'time': t})
        # Lưu thời gian vào URL để verify hiển thị
        return redirect(f"/verify?key={k}&time={t}")
    
    if request.args.get('member_code') == MEMBER_CODE:
        t = get_vn_time()
        return redirect(f"/verify?key={generate_key()}&time={t}")
        
    return render_layout(f"<h1>Xác thực</h1><form><input name='member_code' placeholder='Mã...' required><button class='btn'>XÁC NHẬN</button></form><a href='{get_bypass_link()}' class='btn btn-red'>VƯỢT LINK</a>")

@app.route('/verify')
def verify():
    k = request.args.get('key')
    t = request.args.get('time')
    return render_layout(f"<h1>KEY CỦA BẠN:</h1><div class='key-box' onclick=\"copyText('{k}')\">{k}</div><p class='time-text'>Tạo lúc: {t}</p><p>(Nhấn vào Key để copy)</p>")

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('pin') == ADMIN_PIN: session['admin'] = True
    if session.get('admin'):
        rows = "".join([f"<div class='key-box' onclick=\"copyText('{i['key']}')\">{i['key']} <span style='font-size:0.8rem; display:block;'>{i['time']}</span></div>" for i in all_keys])
        return render_layout(f"<h1>ADMIN</h1>{rows}<a href='/' class='btn'>THOÁT</a>")
    return render_layout("<form method=POST><input type=password name=pin placeholder='Pin...'><button class='btn'>LOGIN</button></form>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
