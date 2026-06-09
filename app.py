from flask import Flask, render_template_string, request, redirect, session
import random, requests, os, urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'alex_security_key_2026'

# --- CẤU HÌNH HỆ THỐNG ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MEMBER_CODE = "123567"
LIMITS = {"12 Giờ": 1, "1 Ngày": 2}

# --- GIAO DIỆN CSS ---
CSS_STYLE = """
<style>
    body {
        background: linear-gradient(-45deg, #f00, #f80, #ff0, #0f0, #00f);
        background-size: 400% 400%;
        animation: bg 10s infinite;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
    }
    @keyframes bg { 0%,100% {background-position:0% 50%} 50% {background-position:100% 50%} }
    .card {
        background: #fff;
        padding: 40px;
        border-radius: 25px;
        width: 90%;
        max-width: 450px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    .btn {
        background: #000;
        color: #fff;
        padding: 16px;
        width: 100%;
        border: none;
        border-radius: 12px;
        margin-top: 15px;
        cursor: pointer;
        font-weight: bold;
        font-size: 1rem;
        text-decoration: none;
        display: block;
    }
    .btn:hover { background: #333; }
    input, select {
        width: 100%;
        padding: 12px;
        margin-top: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    footer { position: fixed; bottom: 15px; color: #fff; font-weight: bold; text-shadow: 1px 1px 2px #000; }
</style>
"""

def generate_page(content):
    return f"""<html><head><meta charset='UTF-8'>{CSS_STYLE}</head>
    <body onclick="document.getElementById('audio').play()">
    <audio id='audio' loop><source src='https://files.catbox.moe/mcy4cu.mp3'></audio>
    <div class='card'>{content}</div>
    <footer>@2026 AlexCloud</footer>
    </body></html>"""

# --- CÁC ĐƯỜNG DẪN (ROUTES) ---

@app.route('/')
def home():
    admin_btn = f"<a href='/admin' class='btn' style='background:green'>ADMIN: TẠO KEY</a>" if session.get('adm') else ""
    return render_template_string(generate_page(f"""
        <h1>AlexCloud</h1>
        <p>Chọn thời hạn nhận key:</p>
        <select id='d'><option>12 Giờ</option><option>1 Ngày</option></select>
        <button class='btn' onclick="location.href='/get?d='+document.getElementById('d').value">NHẬN KEY</button>
        {admin_btn}
    """))

@app.route('/get')
def get():
    d = request.args.get('d')
    c = request.args.get('code')
    if c == MEMBER_CODE:
        return redirect(f"/ver?k=Alex-{random.randint(1000,9999)}&d={d}")
    return render_template_string(generate_page(f"""
        <h1>Xác thực</h1>
        <form action='/get'>
            <input type='hidden' name='d' value='{d}'>
            <input name='code' type='password' placeholder='Mã thành viên...' required>
            <button class='btn'>XÁC NHẬN</button>
        </form>
        <a href='/link?d={d}&s=1' class='btn' style='background:#d9534f'>VƯỢT {LIMITS[d]} LẦN</a>
    """))

@app.route('/link')
def link():
    d = request.args.get('d')
    s = int(request.args.get('s', 1))
    if s <= LIMITS.get(d, 1):
        next_s = s + 1
        # Lưu ý: Thay domain ở dưới thành domain của bạn trên Render
        ret_url = f"https://alexcloud-ukf8.onrender.com/link?d={d}&s={next_s}"
        api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={urllib.parse.quote(ret_url)}"
        return redirect(requests.get(api_url).json()['shortenedUrl'])
    return redirect(f"/ver?k=Alex-{random.randint(1000,9999)}&d={d}")

@app.route('/ver')
def ver():
    k = request.args.get('k')
    d = request.args.get('d')
    return render_template_string(generate_page(f"""
        <h1>KEY CỦA BẠN</h1>
        <h2 style='color:red'>{k}</h2>
        <p>Hạn sử dụng: {d}</p>
        <button class='btn' onclick='navigator.clipboard.writeText("{k}"); this.innerText="ĐÃ COPY!"'>COPY KEY</button>
        <a href='/' class='btn' style='background:#555'>VỀ TRANG CHỦ</a>
    """))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('p') == ADMIN_PIN:
        session['adm'] = True
    if session.get('adm'):
        if request.form.get('crt'):
            return redirect(f"/ver?k=Alex-{random.randint(1000,9999)}&d={request.form.get('t')}")
        return render_template_string(generate_page("""
            <h1>ADMIN PANEL</h1>
            <form method='POST'>
                <select name='t'><option>12 Giờ</option><option>1 Ngày</option></select>
                <button name='crt' value='1' class='btn'>TẠO KEY NHANH</button>
            </form>
            <a href='/out' class='btn' style='background:red'>ĐĂNG XUẤT</a>
        """))
    return render_template_string(generate_page("""
        <form method='POST'>
            <input name='p' type='password' placeholder='Nhập mã PIN Admin...' required>
            <button class='btn'>ĐĂNG NHẬP</button>
        </form>
    """))

@app.route('/out')
def logout():
    session.pop('adm', None)
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
