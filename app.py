from flask import Flask, render_template_string, request, redirect, session
import random, string, os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH ---
ADMIN_PIN = "121113"      # Pass Admin Chính
PASS_PHU = "DanhNgu"      # Pass Admin Phụ
MEMBER_CODE = "123567"    # Mã thành viên
all_keys = []

# Hàm lấy giờ Việt Nam (Giờ:Phút:Giây)
def get_vn_time():
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M:%S")

def generate_unique_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not any(item['key'] == k for item in all_keys): return k

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: sans-serif; display: flex; flex-direction: column; min-height: 100vh; margin: 0; padding: 20px; align-items: center; }
    .card { background: rgba(255,255,255,0.95); padding: 20px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; }
    .btn { background: #000; color: #fff; padding: 15px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; border: none; margin-top: 10px; display: block; text-decoration: none; }
    .key-text { color: #007bff; font-weight: bold; cursor: pointer; text-decoration: underline; }
</style>
"""

def get_html(content):
    js = "<script>function copyText(t){navigator.clipboard.writeText(t);}</script>"
    return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head><body><audio autoplay loop><source src='https://files.catbox.moe/5rqwul.mp3'></audio><div style='flex:1; display:flex; align-items:center; justify-content:center; width:100%'><div class='card'>{content}</div></div><footer><a href='/admin-login' style='color:white'>@2026 AlexCloud</a></footer>{js}</body></html>"

@app.route('/')
def home():
    return render_template_string(get_html("<h1>AlexCloud Cheat</h1><a href='/get-key' class='btn'>GET KEY</a>"))

@app.route('/get-key')
def get_key():
    code = request.args.get('member_code')
    if code == MEMBER_CODE:
        k = generate_unique_key()
        all_keys.append({'key': k, 'tbi': '1', 'day': '1', 'time': get_vn_time()})
        return redirect(f"/verify?key={k}")
    return render_template_string(get_html("<h1>Xác thực</h1><form action='/get-key'><input name='member_code' placeholder='Nhập mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form>"))

@app.route('/verify')
def verify():
    k = request.args.get('key')
    return render_template_string(get_html(f"<h1>KEY CỦA BẠN:</h1><h2 id='k'>{k}</h2><button class='btn' onclick=\"copyText(document.getElementById('k').innerText)\">Nhấn vô = có key</button>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('pin') == ADMIN_PIN: session['admin'] = 'chinh'
        elif request.form.get('pin') == PASS_PHU: session['admin'] = 'phu'
    
    if session.get('admin'):
        if request.method == 'POST' and request.form.get('create'):
            tbi = request.form.get('tbi') if session['admin'] == 'chinh' else '1'
            day = request.form.get('day') if session['admin'] == 'chinh' else '1'
            all_keys.append({'key': generate_unique_key(), 'tbi': tbi, 'day': day, 'time': get_vn_time()})
        
        if request.method == 'POST' and request.form.get('del') and session['admin'] == 'chinh':
            all_keys[:] = [x for x in all_keys if x['key'] != request.form.get('del')]

        rows = "".join([f"<div style='border-bottom:1px solid #ccc; padding:8px; text-align:left;'>KEY: <span class='key-text' onclick=\"copyText('{i['key']}')\">{i['key']}</span><br>TBI: {i['tbi']} | D: {i['day']} | {i['time']} {'<form method=POST style=display:inline><button name=del value='+i['key']+'>Xóa</button></form>' if session['admin']=='chinh' else ''}</div>" for i in all_keys])
        
        form_tao = "<form method='POST'><input name='tbi' placeholder='TBI' required><input name='day' placeholder='Ngày' required><button name='create' value='1' class='btn'>TẠO KEY</button></form>" if session['admin'] == 'chinh' else "<form method='POST'><button name='create' value='1' class='btn'>TẠO KEY (Auto 1-1)</button></form>"
        return render_template_string(get_html(f"<h1>ADMIN {session['admin'].upper()}</h1>{form_tao}<div style='margin-top:15px'>{rows}</div><br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    
    return render_template_string(get_html("<h1>LOGIN ADMIN</h1><form method='POST'><input name='pin' type='password' placeholder='Nhập mật khẩu...' required><button class='btn'>ĐĂNG NHẬP</button></form>"))

@app.route('/admin-logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
