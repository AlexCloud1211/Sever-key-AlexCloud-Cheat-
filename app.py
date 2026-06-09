from flask import Flask, render_template_string, request, redirect, session
import random, string, requests, os, urllib.parse

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MEMBER_CODE = "123567"
GAMES = ["FREE FIRE MAX", "FREE FIRE"]
DUR_LIMITS = {"12 Giờ": 1, "1 Ngày": 2}
BASE_URL = "https://alexcloud-ukf8.onrender.com"

CSS = """
<style>
    @keyframes bgChange { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
    @keyframes colorChange { 0%{color: #ff0000;} 20%{color: #ff8000;} 40%{color: #ffff00;} 60%{color: #00ff00;} 80%{color: #0000ff;} 100%{color: #ff0000;} }
    body { background: linear-gradient(-45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3); background-size: 400% 400%; animation: bgChange 10s ease infinite; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
    .card { background: rgba(255,255,255,0.98); padding: 40px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); width: 90%; max-width: 450px; text-align: center; }
    h1 { font-size: 2.2rem; animation: colorChange 4s infinite; font-weight: 800; margin-bottom: 20px; }
    .btn { background: #000; color: #fff; padding: 18px; border-radius: 12px; cursor: pointer; font-size: 1.2rem; font-weight: bold; width: 100%; border: none; margin-top: 15px; transition: 0.3s; text-decoration: none; display: block; }
    .btn:hover { transform: scale(1.02); background: #222; }
    select, input { font-size: 1.1rem; padding: 12px; width: 100%; margin-top: 15px; border-radius: 10px; border: 2px solid #eee; outline: none; }
    footer { margin-top: auto; padding: 20px; }
    .footer-link { color: #fff; font-weight: bold; text-shadow: 1px 1px 3px #000; text-decoration: none; }
</style>
"""

def get_html(content):
    return f"""<html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head>
    <body onclick="document.getElementById('bgMusic').play()">
    <audio id='bgMusic' loop autoplay><source src='https://files.catbox.moe/mcy4cu.mp3' type='audio/mpeg'></audio>
    <div class='card'>{content}</div>
    <footer><a href='/admin-login' class='footer-link'>@2026 AlexCloud</a></footer></body></html>"""

@app.route('/')
def home():
    game_opts = "".join([f"<option>{g}</option>" for g in GAMES])
    time_opts = "".join([f"<option>{d}</option>" for d in DUR_LIMITS.keys()])
    admin_btn = f"<a href='/admin-login' class='btn' style='background:green'>ADMIN: TẠO KEY NHANH</a>" if session.get('admin') else ""
    return render_template_string(get_html(f"<h1>AlexCloud</h1><select id='game'>{game_opts}</select><select id='duration'>{time_opts}</select><button class='btn' onclick=\"window.location.href='/get-key?game='+document.getElementById('game').value+'&dur='+document.getElementById('duration').value\">NHẬN KEY</button>{admin_btn}"))

@app.route('/get-key')
def get_key():
    game, dur, code = request.args.get('game'), request.args.get('dur'), request.args.get('member_code')
    if code == MEMBER_CODE:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}"
        return redirect(f"/verify?key={k}&dur={dur}")
    html = f"<h1>Xác thực</h1><form action='/get-key' method='GET'><input type='hidden' name='game' value='{game}'><input type='hidden' name='dur' value='{dur}'><input type='password' name='member_code' placeholder='Mã thành viên...' required><button class='btn'>XÁC NHẬN</button></form><a href='/get-key-link?game={game}&dur={dur}&step=1' class='btn' style='background:#d9534f'>KHÔNG CÓ MÃ (VƯỢT {DUR_LIMITS[dur]} LẦN)</a>"
    return render_template_string(get_html(html))

@app.route('/get-key-link')
def get_key_link():
    game, dur = request.args.get('game'), request.args.get('dur')
    step = int(request.args.get('step', 1))
    limit = DUR_LIMITS.get(dur, 1)
    
    if step <= limit:
        # Chuyển hướng tới link rút gọn, khi xong sẽ quay về chính trang này với step + 1
        return_url = f"{BASE_URL}/get-key-link?game={game}&dur={dur}&step={step+1}"
        api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={urllib.parse.quote(return_url)}"
        try:
            return redirect(requests.get(api_url, timeout=10).json()['shortenedUrl'])
        except: return "Lỗi API, vui lòng thử lại!"
    
    k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}"
    return redirect(f"/verify?key={k}&dur={dur}")

@app.route('/verify')
def verify():
    k, dur = request.args.get('key'), request.args.get('dur')
    js = f"<script>function copy(){{navigator.clipboard.writeText('{k}'); document.getElementById('cpBtn').innerText='ĐÃ COPY!'; setTimeout(()=>{{document.getElementById('cpBtn').innerText='NHẬN LẠI KEY';}}, 2000);}}</script>"
    return render_template_string(get_html(f"{js}<h1>KEY CỦA BẠN:</h1><h1 style='color:red'>{k}</h1><p>Thời hạn: {dur}</p><button id='cpBtn' class='btn' onclick='copy()'>NHẤN ĐỂ COPY</button><a href='/' class='btn'>VỀ TRANG CHỦ</a>"))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST' and request.form.get('pin') == ADMIN_PIN: session['admin'] = True
    if session.get('admin'):
        if request.form.get('create'):
            k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}"
            return redirect(f"/verify?key={k}&dur={request.form.get('time')}")
        return render_template_string(get_html("<h1>ADMIN</h1><form method='POST'><select name='time'><option>12 Giờ</option><option>1 Ngày</option></select><button name='create' value='1' class='btn'>TẠO KEY NHANH</button></form><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    return render_template_string(get_html("<h1>ĐĂNG NHẬP ADMIN</h1><form method='POST'><input name='pin' type='password' placeholder='Nhập PIN...' required><button class='btn'>XÁC NHẬN</button></form>"))

@app.route('/admin-logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
