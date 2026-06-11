import streamlit as st
import sqlite3
import random
import string
import requests

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AlexCloud Portal", layout="centered")

# CSS Tùy chỉnh: Trắng chủ đạo, bo góc, chữ to
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .css-1v3fvcr, .main { background-color: #ffffff; }
    
    /* Bo góc cho các thành phần */
    div[data-testid="stButton"] button {
        border-radius: 15px !important;
        border: 2px solid #e0e0e0;
        font-size: 20px !important;
        background-color: #f9f9f9;
    }
    
    /* Chữ to rõ cho người cận */
    .big-font { font-size: 28px !important; font-weight: bold; color: #333; }
    .normal-text { font-size: 20px !important; color: #555; }
    
    /* Ô nhập liệu */
    input { border-radius: 10px !important; font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
conn = sqlite3.connect('alexcloud.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS keys 
             (id INTEGER PRIMARY KEY, key_val TEXT, devices INTEGER, duration INTEGER, member_code TEXT)''')
conn.commit()

# --- CÁC HÀM ---
def shorten_link(url):
    api_token = "6a27be48f348053ba11f3502"
    api_url = f"https://link4m.co/api-shorten/v2?api={api_token}&url={url}"
    try:
        resp = requests.get(api_url).json()
        return resp.get('shortenedUrl', 'Lỗi link')
    except: return "Lỗi hệ thống"

# --- GIAO DIỆN CHÍNH ---
st.markdown('<p class="big-font" style="text-align: center;">🌐 AlexCloud @2026</p>', unsafe_allow_html=True)

# Logo & Liên kết
col1, col2, col3 = st.columns([1, 1, 2])
col1.write("🇻🇳 VN")
col2.write("🇺🇸 EN")
col3.markdown("[✈️ Telegram Support](https://t.me/AlexCloud3)")

# Phần Game
st.markdown("---")
st.header("🎮 Free Fire Max")

tab1, tab2 = st.tabs(["Get Key", "Nhập Mã Thành Viên"])

with tab1:
    if st.button("Nhấn để Get Key"):
        # Tạo link vượt 2 lần
        l1 = shorten_link("https://your-key-page.com")
        l2 = shorten_link(l1)
        st.write(f"Link vượt 1: {l1}")
        st.write(f"Link vượt 2: {l2}")

with tab2:
    m_code = st.text_input("Nhập mã thành viên:")
    if st.button("Xác nhận"):
        st.success("Mã hợp lệ! Đang chuyển hướng...")

# --- ADMIN PANEL ---
st.sidebar.markdown("---")
st.sidebar.header("🔐 Admin Panel")
admin_pass = st.sidebar.text_input("Admin Pass:", type="password")

if admin_pass == "121113":
    st.sidebar.success("Chào Admin!")
    # Quản lý Key
    with st.sidebar.form("add_key"):
        devs = st.number_input("Số thiết bị", 1, 10)
        days = st.number_input("Số ngày", 1, 30)
        if st.form_submit_button("Tạo Key"):
            new_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            st.sidebar.code(new_key)
            st.sidebar.info("Nhấn vào Key để copy")
