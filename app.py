from flask import Flask, render_template_string, request, redirect
import random, requests, os

app = Flask(__name__)

# --- CẤU HÌNH ---
GAMES = ["FREE FIRE MAX", "FREE FIRE"]
DURATIONS = ["12 Giờ", "1 Ngày"]

# CSS UI chuyên nghiệp, hiệu ứng 7 sắc cầu vồng
CSS = """
<style>
    @keyframes rainbow { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    body { 
        background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        background-size: 400% 400%;
        animation: rainbow 10s ease infinite;
        font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; color: white; 
    }
    .box { background: rgba(0,0,0,0.6); padding: 30px; border-radius: 20px; width: 320px; text-align: center; backdrop-filter: blur(15px); border: 2px solid rgba(255,255,255,0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
    .btn { background: linear-gradient(to right, #6a11cb, #2575fc); color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; cursor: pointer; font-weight: bold; margin-top: 15px; transition: 0.3s; }
    .btn:hover { transform: scale(1.05); filter: brightness(1.2); }
    select { width: 100%; padding: 12px; margin-top: 10px; border-radius: 8px; background: rgba(255,255,255,0.9); border: none; }
    .key-display { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; font-family: monospace; font-size: 1.4rem; color: #00ffcc; margin: 15px 0; border: 2px dashed #00ffcc; }
</style>
"""

def get_html(content):
    return f"""<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{CSS}</head>
    <body>
    <audio id='bgMusic' loop><source src='https://files.catbox.moe/5rqwul.mp3' type='audio/mpeg'></audio>
    <script>document.body.addEventListener('click', () => {{ document.getElementById('bgMusic').play(); }}, {{ once: true }});</script>
    <div class='box'>{content}</div></body></html>"""

@app.route('/')
def home():
    games = "".join([f"<option>{g}</option>" for g in GAMES])
    durs = "".join([f"<option>{d}</option>" for d in DURATIONS])
    content = f"<h1>ALEXCLOUD</h1><select id='g'>{games}</select><select id='d'>{durs}</select><button class='btn' onclick=\"location.href='/get-key?g='+document.getElementById('g').value+'&d='+document.getElementById('d').value\">NHẬN KEY</button>"
    return render_template_string(get_html(content))

@app.route('/get-key')
def get_key():
    k = f"AlexCloud-{random.randint(1000,9999)}"
    # Điều hướng trực tiếp đến trang verify sau khi tạo key
    return redirect(f"/verify?key={k}&dur={request.args.get('d')}")

@app.route('/verify')
def verify():
    k = request.args.get('key', 'LỖI')
    d = request.args.get('dur', 'N/A')
    content = f"""
    <h3>KEY CỦA BẠN</h3>
    <div class='key-display' id='k'>{k}</div>
    <p>Hạn dùng: <b>{d}</b></p>
    <button class='btn' onclick="copyKey()">COPY KEY NGAY</button>
    <a href='https://t.me/AlexCloud3' target='_blank'>
        <button class='btn' style='background: linear-gradient(to right, #0088cc, #00aaff);'>LIÊN HỆ TELEGRAM</button>
    </a>
    <br><br><a href='/' style='color:#ccc; font-size:0.8rem; text-decoration:none;'>« Quay lại trang chủ</a>
    <script>
        function copyKey() {{
            var text = document.getElementById('k').innerText;
            navigator.clipboard.writeText(text).then(() => {{ alert('Đã copy Key: ' + text); }});
        }}
    </script>
    """
    return render_template_string(get_html(content))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
