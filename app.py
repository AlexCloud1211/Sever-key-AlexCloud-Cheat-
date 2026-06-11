from flask import Flask, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy  # ### THÊM VÀO
import random, string, os, requests, urllib.parse
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'alexcloud_secret_key_2026'

# --- CẤU HÌNH DATABASE (THÊM VÀO) ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///keys.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class KeyModel(db.Model): # ### THÊM VÀO
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    tbi = db.Column(db.String(10))
    day = db.Column(db.String(10))
    time = db.Column(db.String(20))

with app.app_context(): # ### THÊM VÀO
    db.create_all()

# --- CẤU HÌNH ---
LINK4M_API = "6a27be48f348053ba11f3502"
ADMIN_PIN = "121113"
PASS_PHU = "DanhNgu"
MEMBER_CODE = "123567"
MY_DOMAIN = "https://sever-key-alexcloud-cheat.onrender.com"
# all_keys = []  # ### KHÔNG CẦN DÙNG NỮA

def get_vn_time():
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M:%S")

def generate_unique_key():
    while True:
        k = f"AlexCloud-{''.join(random.choices(string.ascii_uppercase, k=3))}-{''.join(random.choices(string.digits, k=3))}"
        if not KeyModel.query.filter_by(key=k).first(): return k # ### KIỂM TRA TRONG DB

# ... (Giữ nguyên các hàm get_bypass_link, LANGS, get_l, CSS, get_html, set_lang, home) ...

@app.route('/get-key', methods=['GET', 'POST'])
def get_key():
    if request.args.get('auto_key') == "true":
        k = generate_unique_key()
        new_k = KeyModel(key=k, tbi='1', day='1', time=get_vn_time()) # ### THÊM VÀO DB
        db.session.add(new_k); db.session.commit()
        return redirect(f"/verify?key={k}")

    l = get_l()
    code = request.args.get('member_code')
    bypass = get_bypass_link()
    
    if code == MEMBER_CODE:
        k = generate_unique_key()
        new_k = KeyModel(key=k, tbi='1', day='1', time=get_vn_time()) # ### THÊM VÀO DB
        db.session.add(new_k); db.session.commit()
        return redirect(f"/verify?key={k}")
    
    return render_template_string(get_html(f"<h1>{l['auth_title']}</h1><form action='/get-key'><input name='member_code' placeholder='{l['auth_input']}' required><button class='btn'>{l['auth_btn']}</button></form><a href='{bypass}' class='btn btn-red'>{l['link_btn']}</a>"))

@app.route('/verify')
def verify():
    k = request.args.get('key', '---')
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
            new_k = KeyModel(key=generate_unique_key(), tbi=tbi, day=day, time=get_vn_time())
            db.session.add(new_k); db.session.commit()
        
        if request.method == 'POST' and request.form.get('del') and session['admin'] == 'chinh':
            KeyModel.query.filter_by(key=request.form.get('del')).delete() # ### XÓA TRONG DB
            db.session.commit()

        # ### LẤY DỮ LIỆU TỪ DB
        keys_from_db = KeyModel.query.all()
        rows = "".join([f"<div style='border-bottom:1px solid #ccc; padding:8px; text-align:left;'>KEY: <span class='key-text' onclick=\"copyText('{i.key}')\">{i.key}</span><br>TBI: {i.tbi} | D: {i.day} | {i.time} {'<form method=POST style=display:inline><button name=del value='+i.key+'>Xóa</button></form>' if session['admin']=='chinh' else ''}</div>" for i in keys_from_db])
        
        form_tao = "<form method='POST'><input name='tbi' placeholder='TBI' required><input name='day' placeholder='Ngày' required><button name='create' value='1' class='btn'>TẠO KEY</button></form>" if session['admin'] == 'chinh' else "<form method='POST'><button name='create' value='1' class='btn'>TẠO KEY (Auto 1-1)</button></form>"
        return render_template_string(get_html(f"<h1>ADMIN {session['admin'].upper()}</h1>{form_tao}<div style='margin-top:15px'>{rows}</div><br><a href='/admin-logout' class='btn' style='background:red'>ĐĂNG XUẤT</a>"))
    
    return render_template_string(get_html("<h1>LOGIN ADMIN</h1><form method='POST'><input name='pin' type='password' placeholder='Mật khẩu...' required><button class='btn'>ĐĂNG NHẬP</button></form>"))

# ... (Phần cuối giữ nguyên)
