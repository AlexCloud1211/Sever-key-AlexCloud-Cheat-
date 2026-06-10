from flask import Flask, render_template_string, request, redirect, session
import random, string, requests, os, urllib.parse
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MEMBER_CODE = "123567"
MY_DOMAIN = "https://sever-key-alexcloud-cheat.onrender.com"
all_keys = []

# --- CÁC HÀM HỖ TRỢ ---
def get_vn_time():
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M:%S")

def generate_unique_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not any(item['key'] == k for item in all_keys): return k

def get_bypass_link():
    # URL đích: Quay về trang chủ của bạn với cờ auto_key
    target_url = urllib.parse.quote(f"{MY_DOMAIN}/get-key?auto_key=true")
    api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={target_url}"
    try:
        response = requests.get(api_url, timeout=5).json()
        return response.get('shortenedUrl', '#')
    except:
        return "#"

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; min-height: 100vh; margin: 0; padding: 20px; align-items: center; }
    .card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .btn { background: #000; color: #fff; padding: 15px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; border: none; margin-top: 15px; display: block; text-decoration: none; transition: 0.3s; }
    .btn-red { background: #d9534f; }
    #keyBox { color: #d00; font-size: 1.6rem; cursor: pointer; border: 2px dashed #d00; padding: 12px; border-radius: 10px; margin: 15px 0; font-weight: bold; }
    .admin-row { border-bottom: 1px solid #ccc; padding: 10px; margin: 5px 0; background: #fff; border-radius: 8px; text-align: left; font-size: 0.9rem; }
</style>
"""

def get_html(content):
    js = "<script>function copyKey(){var k=document.getElementById('keyBox').innerText;navigator.clipboard.writeText(k);alert('Đã copy: '+k);}</script>"
    return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head><body><audio autoplay loop><source src='https://files.catbox.moe/5rqwul.mp3'></audio><div style='flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%;'><div class='card'>{content}</div></div><footer><a href='/admin-login' style='color:white'>@2026 AlexCloud</a></footer>{js}</body></html>"

# --- ROUTES ---
@app.route('/')
def home():
    return render_template_string(get_html("<h1>AlexCloud Cheat</h1><a href='/get-key' class='btn'>GET KEY</a>"))

@app.route('/get-key', methods=['GET', 'POST'])
def get_key():
    # Tự động cấp key khi từ Link4m quay về
    if request.args.get('auto_key') == "true":
        k = generate_unique_key()
        all_keys.append({'key': k, 'tbi': '1', 'day': '1', 'time': get_vn_time()})
        return redirect(f"/verify?key={k}")
        
    code = request.args.get('member_code')
    bypass = get_bypass_link()
    
    if code == MEMBER_CODE:
        return redirect(f"/verify?key={generate_unique_key()}")
    
    return render_template_string(get_html(f"<h1>Xác thực</h1><form action='/get-key'><input name='member_code' placeholder='Mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><a href='{bypass}' class='btn btn-red'>VƯỢT LINK LẤY KEY</a>"))

@app.route('/verify')
def verify():
    k = request.args.get('key', 'Chưa có key')
    return render_template_string(get_html(f"<h1>KEY CỦA BẠN:</h1><div id='keyBox' onclick='copyKey()'>{k}</div><a href='/' class='btn'>VỀ TRANG CHỦ</a>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('pin') == ADMIN_PIN: session['admin'] = True
        elif session.get('admin') and request.form.get('create'):
            all_keys.append({'key': generate_unique_key(), 'tbi': request.form.get('tbi'), 'day': request.form.get('day'), 'time': get_vn_time()})
    
    if session.get('admin'):
        rows = "".join([f"<div class='admin-row'><b>KEY:</b> {i['key']} | <b>TBI:</b> {i['tbi']} | <b>D:</b> {i['day']} | <b>TIME:</b> {i['time']}</div>" for i in all_keys])
        return render_template_string(get_html(f"<h1>LOG ADMIN</h1><form method='POST'><input name='tbi' placeholder='TBI' required><input name='day' placeholder='Ngày' required><button name='create' value='1' class='btn'>TẠO KEY</button></form>{rows}<br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    return render_template_string(get_html("<h1>ADMIN</h1><form method='POST'><input name='pin' type='password'><button class='btn'>ĐĂNG NHẬP</button></form>"))

@app.route('/admin-logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
