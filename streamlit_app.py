
import streamlit as st
import time
import base64
import os

st.set_page_config(page_title="專注倒數計時器", layout="centered")

# 初始化 session_state
if "task" not in st.session_state:
    st.session_state.task = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "duration" not in st.session_state:
    st.session_state.duration = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "completed" not in st.session_state:
    st.session_state.completed = False

# 播放聲音
def play_sound():
    sound_path = os.path.join(os.path.dirname(__file__), "ding.mp3")
    if os.path.exists(sound_path):
        with open(sound_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'''
                <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            ''', unsafe_allow_html=True)

# 使用者輸入
if not st.session_state.running and not st.session_state.completed:
    st.title("🎯 專注倒數計時器")
    with st.form("set_timer"):
        name = st.text_input("任務名稱", "午餐休息")
        minutes = st.number_input("倒數時間（分鐘）", min_value=1, max_value=120, value=5)
        start = st.form_submit_button("開始倒數")
        if start:
            st.session_state.task = name
            st.session_state.duration = int(minutes * 60)
            st.session_state.start_time = time.time()
            st.session_state.running = True

# 專注倒數畫面
if st.session_state.running:
    st.title(f"🔍 任務：{st.session_state.task}")
    timer_display = st.empty()

    while True:
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = st.session_state.duration - elapsed
        if remaining <= 0:
            st.session_state.running = False
            st.session_state.completed = True
            break
        mins, secs = divmod(remaining, 60)
        timer_display.markdown(f"<h1 style='text-align:center;font-size:100px'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        time.sleep(1)

# 完成畫面
if st.session_state.completed:
    st.balloons()
    st.success(f"✅ 任務【{st.session_state.task}】倒數結束！")
    play_sound()
    if st.button("重新設定任務"):
        for key in ["task", "start_time", "duration", "running", "completed"]:
            st.session_state[key] = None
        st.experimental_rerun()
