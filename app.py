from flask import Flask, render_template_string, request, redirect, session, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import random, string, os, requests, urllib.parse, logging, time
from datetime import datetime, timedelta

# --- THIẾT LẬP LOGGING CHUYÊN NGHIỆP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = os.urandom(24) # Secret key ngẫu nhiên an toàn hơn

# --- CẤU HÌNH DATABASE VỚI POSTGRESQL (SẴN SÀNG CHO RENDER) ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///alexcloud.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- CÁC MODELS DỮ LIỆU ---
class AlexKey(db.Model):
    __tablename__ = 'alex_keys'
    id = db.Column(db.Integer, primary_key=True)
    key_value = db.Column(db.String(64), unique=True, nullable=False)
    member_code = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiry = db.Column(db.DateTime, nullable=False)
    max_devices = db.Column(db.Integer, default=1)
    used_devices = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="active")

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- HẰNG SỐ CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MY_DOMAIN = "https://sever-key-alexcloud-cheat.onrender.com"

# --- CÁC HÀM XỬ LÝ KỸ THUẬT ---
def generate_complex_key():
    parts = [''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(4)]
    return f"AC-{'-'.join(parts)}"

def log_action(msg):
    db.session.add(SystemLog(action=msg))
    db.session.commit()

def call_bypass_api(url):
    try:
        r = requests.get(f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={url}", timeout=10)
        return r.json().get('shortenedUrl', url)
    except Exception as e:
        logging.error(f"API Error: {e}")
        return url

# --- GIAO DIỆN HỆ THỐNG (CSS & HTML) ---
UI_HEADER = """
<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
<style>
    body { background: #f0f2f5; font-size: 20px; }
    .main-box { background: white; border-radius: 30px; padding: 50px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
    .btn-lg { border-radius: 15px; padding: 20px; font-weight: bold; }
    .admin-nav { background: #343a40; color: white; padding: 20px; border-radius: 15px; margin-bottom: 30px; }
</style>
"""

# --- ROUTES CHÍNH ---
@app.route('/')
def index():
    return render_template_string(UI_HEADER + """
    <div class='container mt-5'><div class='main-box text-center'>
        <h1>🌐 AlexCloud @2026</h1>
        <p>Hệ thống quản lý key cao cấp</p>
        <a href='/get-key' class='btn btn-primary btn-lg w-100'>LẤY KEY NGAY</a>
        <div class='mt-5'>
            <input type='password' id='pin' class='form-control' placeholder='Admin PIN'>
            <button class='btn btn-dark mt-2 w-100' onclick="if(document.getElementById('pin').value=='121113') window.location.href='/admin-panel'">Truy cập Admin</button>
        </div>
    </div></div>""")

@app.route('/get-key')
def get_key_flow():
    # Vượt 2 lần
    link1 = call_bypass_api(f"{MY_DOMAIN}/verify-link")
    link2 = call_bypass_api(link1)
    return render_template_string(UI_HEADER + f"""
    <div class='container mt-5 text-center'>
        <h1>Vượt Link Bước 2</h1>
        <a href='{link2}' class='btn btn-danger btn-lg'>NHẤN ĐỂ NHẬN KEY</a>
    </div>""")

@app.route('/verify-link')
def verify():
    k = generate_complex_key()
    new_k = AlexKey(key_value=k, expiry=datetime.utcnow() + timedelta(days=1))
    db.session.add(new_k)
    db.session.commit()
    log_action(f"Generated key: {k}")
    return redirect(url_for('result', key=k))

@app.route('/result')
def result():
    return render_template_string(UI_HEADER + f"""
    <div class='container mt-5'><div class='main-box text-center'>
        <h1>KEY CỦA BẠN:</h1>
        <h2 class='text-success'>{request.args.get('key')}</h2>
        <button class='btn btn-outline-secondary' onclick='navigator.clipboard.writeText("{request.args.get('key')}")'>Copy Key</button>
    </div></div>""")

@app.route('/admin-panel')
def admin():
    keys = AlexKey.query.all()
    return render_template_string(UI_HEADER + f"""
    <div class='container mt-5'>
        <div class='admin-nav'><h2>Quản trị AlexCloud</h2></div>
        <table class='table table-hover'>
            <thead><tr><th>Key</th><th>Hạn</th><th>Trạng thái</th></tr></thead>
            <tbody>
                {"".join([f"<tr><td>{k.key_value}</td><td>{k.expiry}</td><td>{k.status}</td></tr>" for k in keys])}
            </tbody>
        </table>
    </div>""")

if __name__ == '__main__':
    # Chạy hệ thống
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
