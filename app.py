from flask import Flask, render_template_string, request, redirect, session
import random, string, os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH ---
ADMIN_PIN = "121113"        # Admin chính
PASS_PHU = "DanhNgu"        # Admin phụ
MEMBER_CODE = "123567"      # Mã thành viên
all_keys = []

# Hàm lấy giờ Việt Nam
def get_vn_time():
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M:%S")

def generate_unique_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not any(item['key'] == k for item in all_keys): return k

# --- GIAO DIỆN ---
CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; min-height: 100vh; margin: 0; padding: 20px; align-items: center; }
    .card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 20px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .btn { background: #000; color: #fff; padding: 15px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; border: none; margin-top: 15px; display: block; text-decoration: none; text-align: center; }
    .btn-red { background: #d9534f; }
    .key-text { color: #007bff; font-weight: bold; cursor: pointer; text-decoration: underline; font-size: 1.5rem; display: block; margin: 15px 0; }
    .status-badge { display: inline-block; padding: 5px 15px; border-radius: 20px; background: #28a745; color: white; font-size: 0.8rem; margin-bottom: 10px; }
</style>
"""

def get_html(content, error=""):
    # JS: Copy và hiệu ứng chờ tạo link
    js = """
    <script>
        function copyText(t){navigator.clipboard.writeText(t);}
        function loadingLink(btn) {
            btn.innerText = "Đang tạo link, vui lòng chờ...";
            btn.style.pointerEvents = "none";
            btn.style.opacity = "0.7";
            setTimeout(function() {
                window.location.href = "https://google.com"; // THAY LINK VƯỢT CỦA BẠN VÀO ĐÂY
            }, 7000);
        }
    </script>"""
    return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head><body><audio autoplay loop><source src='https://files.catbox.moe/5rqwul.mp3'></audio><div style='flex:1; display:flex; align-items:center; justify-content:center; width:100%'><div class='card'><div class='status-badge'>● System Online</div>{error}{content}</div></div><footer><a href='/admin-login' style='color:white'>@2026 AlexCloud</a></footer>{js}</body></html>"

@app.route('/')
def home():
    return render_template_string(get_html("<h1>AlexCloud Cheat</h1><p>Game: Free Fire</p><p>Thời hạn: 1 Ngày</p><a href='/get-key' class='btn'>GET KEY</a>"))

@app.route('/get-key', methods=['GET', 'POST'])
def get_key():
    code = request.args.get('member_code')
    if code is None:
        return render_template_string(get_html("<h1>Xác thực</h1><form action='/get-key'><input name='member_code' placeholder='Nhập mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><button class='btn btn-red' onclick='loadingLink(this)'>Vượt link để có key</button>"))
    if code == MEMBER_CODE:
        k = generate_unique_key()
        all_keys.append({'key': k, 'tbi': '1', 'day': '1', 'time': get_vn_time()})
        return redirect(f"/verify?key={k}")
    return render_template_string(get_html("<h1>Sai Rồi Kìa em Out Ra get đi</h1><a href='/get-key' class='btn'>VỀ LẠI</a><button class='btn btn-red' onclick='loadingLink(this)'>Vượt link để có key</button>"))

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
        else: error = "<p style='color:red; font-weight:bold'>Sai mật khẩu rồi!</p>"
    
    if session.get('admin'):
        if request.method == 'POST' and request.form.get('create'):
            tbi = request.form.get('tbi') if session['admin'] == 'chinh' else '1'
            day = request.form.get('day') if session['admin'] == 'chinh' else '1'
            all_keys.append({'key': generate_unique_key(), 'tbi': tbi, 'day': day, 'time': get_vn_time()})
        
        if request.method == 'POST' and request.form.get('del') and session['admin'] == 'chinh':
            all_keys[:] = [x for x in all_keys if x['key'] != request.form.get('del')]

        rows = "".join([f"<div style='border-bottom:1px solid #ccc; padding:8px; text-align:left;'>KEY: <span class='key-text' style='font-size:1rem' onclick=\"copyText('{i['key']}')\">{i['key']}</span><br>TBI: {i['tbi']} | D: {i['day']} | {i['time']} {'<form method=POST style=display:inline><button name=del value='+i['key']+'>Xóa</button></form>' if session['admin']=='chinh' else ''}</div>" for i in all_keys])
        
        form_tao = "<form method='POST'><input name='tbi' placeholder='TBI' required><input name='day' placeholder='Ngày' required><button name='create' value='1' class='btn'>TẠO KEY</button></form>" if session['admin'] == 'chinh' else "<form method='POST'><button name='create' value='1' class='btn'>TẠO KEY (Auto 1-1)</button></form>"
        return render_template_string(get_html(f"<h1>ADMIN {session['admin'].upper()}</h1>{form_tao}<div style='margin-top:15px'>{rows}</div><br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    
    return render_template_string(get_html("<h1>LOGIN ADMIN</h1><form method='POST'><input name='pin' type='password' placeholder='Mật khẩu...' required><button class='btn'>ĐĂNG NHẬP</button></form>", error=error))

@app.route('/admin-logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
