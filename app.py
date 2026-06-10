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

def generate_unique_key():
    return f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"

def get_bypass_link():
    # LINK DÍCH: Khi khách vượt xong sẽ quay về link này
    target_url = "https://cheat.onrender.com/get-key?auto_key=true"
    # API Link4m chuẩn theo ảnh bạn gửi
    api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={target_url}"
    try:
        response = requests.get(api_url, timeout=5).json()
        return response.get('shortenedUrl', '#')
    except:
        return "#"

CSS = """
<style>
    body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
    .card { background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; max-width: 400px; margin: auto; }
    .btn { background: #fff; color: #000; padding: 12px; border-radius: 8px; display: block; margin: 10px auto; font-weight: bold; text-decoration: none; border: none; width: 100%; cursor: pointer; }
    .btn-red { background: #d9534f; color: #fff; }
</style>
"""

# Trang chủ
@app.route('/')
def home():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='card'><h1>AlexCloud Cheat</h1><a href='/get-key' class='btn'>GET KEY</a></div></body></html>")

# Trang lấy key
@app.route('/get-key', methods=['GET', 'POST'])
def get_key():
    # Tự động tạo key nếu Link4m trả về tham số auto_key
    if request.args.get('auto_key') == "true":
        k = generate_unique_key()
        all_keys.append({'key': k})
        return redirect(f"/verify?key={k}")
        
    code = request.args.get('member_code')
    bypass = get_bypass_link()
    
    if not code:
        return render_template_string(f"<html><head>{CSS}</head><body><div class='card'><h1>Xác thực</h1><form action='/get-key'><input name='member_code' placeholder='Mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><a href='{bypass}' class='btn btn-red'>VƯỢT LINK LẤY KEY</a></div></body></html>")
    
    if code == MEMBER_CODE:
        return redirect(f"/verify?key={generate_unique_key()}")
        
    return render_template_string(f"<html><head>{CSS}</head><body><div class='card'><h1>Sai mã rồi!</h1><a href='/get-key' class='btn'>THỬ LẠI</a></div></body></html>")

# Trang trả kết quả
@app.route('/verify')
def verify():
    k = request.args.get('key', 'Chưa có key')
    return render_template_string(f"<html><head>{CSS}</head><body><div class='card'><h1>KEY CỦA BẠN:</h1><h2>{k}</h2><a href='/' class='btn'>TRANG CHỦ</a></div></body></html>")

# Admin Login
@app.route('/admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('pin') == ADMIN_PIN: session['admin'] = 'chinh'
    if session.get('admin'):
        return render_template_string(f"<html><head>{CSS}</head><body><div class='card'><h1>ADMIN</h1><p>Hệ thống hoạt động ổn định</p><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a></div></body></html>")
    return render_template_string(f"<html><head>{CSS}</head><body><div class='card'><form method=POST><input name=pin type=password placeholder='Mật khẩu Admin...'><button class='btn'>ĐĂNG NHẬP</button></form></div></body></html>")

@app.route('/admin-logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

