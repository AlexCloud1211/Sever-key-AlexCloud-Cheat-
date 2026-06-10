from flask import Flask, render_template_string, request, redirect, session
import random, string, os, requests
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH ---
ADMIN_PIN = "121113"
PASS_PHU = "DanhNgu"
MEMBER_CODE = "123567"
LINK4M_API = "6a27be48f348053ba11f3502" 
all_keys = []

def get_vn_time():
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M:%S")

def get_bypass_link():
    # URL web của bạn (Thay lại link render của bạn vào đây)
    target_url = "https://cheat.onrender.com/get-key?auto_key=true"
    try:
        api_url = f"https://link4m.com/api?api={LINK4M_API}&url={target_url}"
        response = requests.get(api_url).json()
        return response.get('shortenedUrl', '#')
    except:
        return "#"

def generate_unique_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not any(item['key'] == k for item in all_keys): return k

CSS = """
<style>
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: sans-serif; display: flex; flex-direction: column; min-height: 100vh; margin: 0; padding: 20px; align-items: center; }
    .card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; }
    .btn { background: #000; color: #fff; padding: 15px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; border: none; margin-top: 15px; display: block; text-decoration: none; text-align: center; }
    .btn-red { background: #d9534f; }
    .key-text { color: #007bff; font-weight: bold; cursor: pointer; text-decoration: underline; font-size: 1.5rem; display: block; margin: 15px 0; }
</style>
"""

def get_html(content, error=""):
    js = """<script>
        function copyText(t){navigator.clipboard.writeText(t);}
        function loadingLink(btn) {
            btn.innerText = "Đang tạo link, vui lòng chờ...";
            btn.style.pointerEvents = "none";
            setTimeout(function() { window.location.href = btn.getAttribute('data-link'); }, 5000);
        }
    </script>"""
    return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head><body><div class='card'>{error}{content}</div>{js}</body></html>"

@app.route('/')
def home():
    return render_template_string(get_html("<h1>AlexCloud Cheat</h1><a href='/get-key' class='btn'>GET KEY</a>"))

@app.route('/get-key', methods=['GET', 'POST'])
def get_key():
    if request.args.get('auto_key') == "true":
        k = generate_unique_key()
        all_keys.append({'key': k, 'tbi': '1', 'day': '1', 'time': get_vn_time()})
        return redirect(f"/verify?key={k}")

    bypass = get_bypass_link()
    code = request.args.get('member_code')
    
    if code is None:
        return render_template_string(get_html("<h1>Xác thực</h1><form action='/get-key'><input name='member_code' placeholder='Mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><button class='btn btn-red' data-link='"+bypass+"' onclick='loadingLink(this)'>Vượt link để có key</button>"))
    
    if code == MEMBER_CODE:
        return redirect(f"/verify?key={generate_unique_key()}")
        
    return render_template_string(get_html("<h1>Sai Rồi Kìa em!</h1><a href='/get-key' class='btn'>VỀ LẠI</a><button class='btn btn-red' data-link='"+bypass+"' onclick='loadingLink(this)'>Vượt link để có key</button>"))

@app.route('/verify')
def verify():
    k = request.args.get('key')
    return render_template_string(get_html(f"<h1>KEY CỦA BẠN:</h1><span class='key-text' onclick=\"copyText('{k}')\">{k}</span><button class='btn' onclick=\"copyText('{k}')\">Nhấn vô = có key</button><a href='/' class='btn'>VỀ TRANG CHỦ</a>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    error = ""
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == ADMIN_PIN: session['admin'] = 'chinh'
        elif pin == PASS_PHU: session['admin'] = 'phu'
        else: error = "<p style='color:red'>Sai mật khẩu!</p>"
    
    if session.get('admin'):
        if request.method == 'POST' and request.form.get('create'):
            all_keys.append({'key': generate_unique_key(), 'tbi': '1', 'day': '1', 'time': get_vn_time()})
        if request.method == 'POST' and request.form.get('del'):
            all_keys[:] = [x for x in all_keys if x['key'] != request.form.get('del')]
            
        rows = "".join([f"<div style='border-bottom:1px solid #ccc; padding:8px'>KEY: {i['key']} <form method=POST style=display:inline><button name=del value={i['key']}>Xóa</button></form></div>" for i in all_keys])
        return render_template_string(get_html(f"<h1>ADMIN</h1><form method=POST><button name=create value=1 class=btn>TẠO KEY</button></form>{rows}<a href='/admin-logout' class=btn style=background:red>THOÁT</a>", error=error))
    
    return render_template_string(get_html("<h1>LOGIN ADMIN</h1><form method='POST'><input name='pin' type='password'><button class='btn'>LOGIN</button></form>", error=error))

@app.route('/admin-logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
