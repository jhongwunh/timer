
import streamlit as st
import time
import base64
import os

st.set_page_config(page_title="多任務倒數計時器", layout="centered")

# 初始化 session_state
if "timers" not in st.session_state:
    st.session_state.timers = {}
if "focus_timer" not in st.session_state:
    st.session_state.focus_timer = None

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

if st.session_state.focus_timer is None:
    st.markdown('<meta http-equiv="refresh" content="1">', unsafe_allow_html=True)
    st.title("⏱️ 多任務倒數計時器")
    with st.form("add_timer"):
        name = st.text_input("📝 任務名稱", "")
        minutes = st.number_input("⏳ 倒數幾分鐘", min_value=1, max_value=120, value=5)
        submitted = st.form_submit_button("新增任務")
        if submitted and name:
            key = f"{name}_{int(time.time())}"
            st.session_state.timers[key] = {
                "name": name,
                "duration": minutes * 60,
                "remaining": minutes * 60,
                "running": True,
                "last_update": time.time(),
                "completed": False
            }

def update_timers():
    for timer in st.session_state.timers.values():
        if timer["running"] and not timer["completed"]:
            now = time.time()
            elapsed = now - timer["last_update"]
            timer["remaining"] -= elapsed
            timer["last_update"] = now
            if timer["remaining"] <= 0:
                timer["remaining"] = 0
                timer["running"] = False
                timer["completed"] = True
                play_sound()

update_timers()

if st.session_state.focus_timer:
    timer = st.session_state.timers[st.session_state.focus_timer]
    st.title(f"🔍 專注任務：{timer['name']}")
    timer_placeholder = st.empty()

    while timer["remaining"] > 0 and timer["running"]:
        mins, secs = divmod(int(timer["remaining"]), 60)
        timer_placeholder.markdown(f"<h1 style='text-align:center;font-size:100px'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        time.sleep(1)
        update_timers()

    mins, secs = divmod(int(timer["remaining"]), 60)
    timer_placeholder.markdown(f"<h1 style='text-align:center;font-size:100px'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
    if timer["completed"]:
        st.success("✅ 任務完成！")

    if st.button("返回任務列表"):
        st.session_state.focus_timer = None
        st.stop()

else:
    remove_list = []
    for key, timer in st.session_state.timers.items():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        mins, secs = divmod(int(timer["remaining"]), 60)
        status = "⏳ 進行中" if timer["running"] else ("✅ 完成" if timer["completed"] else "⏸️ 已暫停")

        with col1:
            st.markdown(f"**{timer['name']}**<br/>{status}<br/><span style='font-size:28px'>{mins:02d}:{secs:02d}</span>", unsafe_allow_html=True)
        with col2:
            if st.button("暫停" if timer["running"] else "繼續", key=f"toggle_{key}"):
                timer["running"] = not timer["running"]
                timer["last_update"] = time.time()
        with col3:
            if st.button("重設", key=f"reset_{key}"):
                timer["remaining"] = timer["duration"]
                timer["running"] = False
                timer["completed"] = False
                timer["last_update"] = time.time()
        with col4:
            if st.button("🔍 放大", key=f"focus_{key}"):
                st.session_state.focus_timer = key
                st.stop()
        with col5:
            if st.button("❌", key=f"delete_{key}"):
                remove_list.append(key)

    for key in remove_list:
        del st.session_state.timers[key]
