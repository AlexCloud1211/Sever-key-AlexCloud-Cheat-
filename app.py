from flask import Flask, render_template_string, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import random, string, os, requests, urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH DATABASE ---
# Nếu có DATABASE_URL (PostgreSQL trên Render), nó sẽ dùng. Nếu không có, nó dùng SQLite cục bộ.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///alexcloud.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODEL DỮ LIỆU ---
class AlexKey(db.Model):
    __tablename__ = 'alex_keys'
    id = db.Column(db.Integer, primary_key=True)
    key_value = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tự động tạo bảng trong Database khi khởi chạy
with app.app_context():
    db.create_all()

# --- CẤU HÌNH CŨ ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
MY_DOMAIN = "https://sever-key-alexcloud-cheat.onrender.com"

# --- LOGIC DỮ LIỆU ---
def generate_unique_key():
    return f"AlexCloud-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

def get_bypass_link():
    token = ''.join(random.choices(string.ascii_letters, k=10))
    dest = f"{MY_DOMAIN}/verify-link?token={token}"
    target_url = urllib.parse.quote(dest)
    api_url = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={target_url}"
    try:
        res = requests.get(api_url, timeout=5).json()
        return res.get('shortenedUrl', '#')
    except:
        return "#"

# --- ROUTES ---
@app.route('/')
def home():
    return render_template_string(f"""
    <h1>AlexCloud Cheat</h1>
    <a href='/get-key' style='padding:15px; background:blue; color:white; text-decoration:none;'>LẤY KEY NGAY</a>
    """)

@app.route('/get-key')
def get_key():
    bypass_url = get_bypass_link()
    return render_template_string(f"""
    <h1>Bước 1: Vượt link</h1>
    <a href='{bypass_url}' target='_blank' style='padding:15px; background:red; color:white;'>NHẤN ĐỂ VƯỢT LINK</a>
    """)

@app.route('/verify-link')
def verify_link():
    token = request.args.get('token')
    if token:
        new_key = generate_unique_key()
        # Lưu vào Database thật
        new_entry = AlexKey(key_value=new_key)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('show_key', key=new_key))
    return "Lỗi xác thực!"

@app.route('/key-result')
def show_key():
    key = request.args.get('key')
    return render_template_string(f"<h1>KEY CỦA BẠN:</h1><h2 style='color:green;'>{key}</h2>")

if __name__ == '__main__':
    # Sử dụng PORT của Render hoặc mặc định là 8080
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
