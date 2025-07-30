import streamlit as st
import time

# 設定頁面
st.set_page_config(page_title="翻頁倒數計時器", layout="centered")

# 自動每秒刷新
st.markdown('<meta http-equiv="refresh" content="1">', unsafe_allow_html=True)

# CSS 美化翻頁數字風格
st.markdown("""
    <style>
    .timer {
        font-family: 'Courier New', monospace;
        font-size: 80px;
        font-weight: bold;
        color: #ffffff;
        background-color: #000000;
        padding: 30px 50px;
        border-radius: 15px;
        display: inline-block;
        letter-spacing: 10px;
        text-align: center;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕒 翻頁風格倒數計時器")
st.markdown("輸入任務與時間，開始倒數！")

# 初始化 timer
if "countdown_start" not in st.session_state:
    st.session_state.countdown_start = None
if "duration" not in st.session_state:
    st.session_state.duration = 0
if "task_name" not in st.session_state:
    st.session_state.task_name = ""

# 輸入任務
with st.form("start_form"):
    task_name = st.text_input("📝 任務名稱", value=st.session_state.task_name)
    minutes = st.number_input("⏳ 倒數時間（分鐘）", min_value=1, max_value=120, value=5)
    start = st.form_submit_button("開始倒數")

    if start:
        st.session_state.task_name = task_name
        st.session_state.countdown_start = time.time()
        st.session_state.duration = int(minutes * 60)

# 顯示倒數時間
if st.session_state.countdown_start is not None:
    elapsed = int(time.time() - st.session_state.countdown_start)
    remaining = st.session_state.duration - elapsed

    if remaining < 0:
        remaining = 0

    mins, secs = divmod(remaining, 60)
    time_str = f"{mins:02d}:{secs:02d}"

    st.markdown(f"<div class='timer'>{time_str}</div>", unsafe_allow_html=True)

    if remaining == 0:
        st.success(f"✅ 任務【{st.session_state.task_name}】倒數結束！")
        st.balloons()
