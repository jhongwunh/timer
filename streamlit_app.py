import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="多任務倒數計時器", layout="centered")

st.title("⏱️ 多任務倒數計時器")
st.markdown("你可以同時新增多個任務計時器，並各自操作暫停與繼續。")

# 初始化 session_state 用來記錄所有計時器
if "timers" not in st.session_state:
    st.session_state.timers = {}

# 新增計時器
with st.form("new_timer_form"):
    task_name = st.text_input("📝 任務名稱", "")
    minutes = st.number_input("⏳ 計時（分鐘）", min_value=1, max_value=120, value=10)
    submitted = st.form_submit_button("新增計時器")

    if submitted and task_name:
        task_id = f"{task_name}_{int(time.time())}"
        st.session_state.timers[task_id] = {
            "name": task_name,
            "duration": int(minutes * 60),  # 秒數
            "remaining": int(minutes * 60),
            "is_running": True,
            "last_updated": time.time()
        }

# 每次重新渲染時，自動更新每個計時器的剩餘時間
for task_id, timer in list(st.session_state.timers.items()):
    now = time.time()
    if timer["is_running"]:
        elapsed = now - timer["last_updated"]
        timer["remaining"] -= int(elapsed)
        timer["last_updated"] = now
        if timer["remaining"] <= 0:
            timer["remaining"] = 0
            timer["is_running"] = False

# 顯示所有計時器
for task_id, timer in list(st.session_state.timers.items()):
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
    mins, secs = divmod(timer["remaining"], 60)
    status = "⏳ 進行中" if timer["is_running"] else "⏸️ 已暫停 / 結束"

    with col1:
        st.markdown(f"**{timer['name']}** — {status}<br/>剩餘時間：{mins:02d}:{secs:02d}", unsafe_allow_html=True)
    with col2:
        if st.button("暫停" if timer["is_running"] else "繼續", key=f"pause_{task_id}"):
            timer["is_running"] = not timer["is_running"]
            timer["last_updated"] = time.time()
    with col3:
        if st.button("重置", key=f"reset_{task_id}"):
            timer["remaining"] = timer["duration"]
            timer["last_updated"] = time.time()
            timer["is_running"] = False
    with col4:
        if st.button("❌ 刪除", key=f"delete_{task_id}"):
            del st.session_state.timers[task_id]
            st.experimental_rerun()

# 自動刷新每秒
st.experimental_rerun()
