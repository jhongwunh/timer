import streamlit as st
import time
import base64
import os

st.set_page_config(page_title="多任務倒數計時器", layout="centered")

# 初始化 session_state
if "timers" not in st.session_state:
    st.session_state.timers = {}
if "focus" not in st.session_state:
    st.session_state.focus = None  # 放大任務 ID

# 聲音提示功能：播放本地 ding.mp3
def play_sound():
    sound_path = os.path.join(os.path.dirname(__file__), "ding.mp3")
    if os.path.exists(sound_path):
        with open(sound_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)

# 新增任務表單（只有在沒放大任務時才顯示）
if st.session_state.focus is None:
    st.title("⏱️ 多任務倒數計時器")

    with st.form("add_timer"):
        task_name = st.text_input("📝 任務名稱", "")
        minutes = st.number_input("⏳ 計時（分鐘）", min_value=1, max_value=120, value=5)
        add = st.form_submit_button("新增任務")

        if add and task_name:
            task_id = f"{task_name}_{int(time.time())}"
            now = time.time()
            st.session_state.timers[task_id] = {
                "name": task_name,
                "duration": int(minutes * 60),
                "remaining": int(minutes * 60),
                "is_running": True,
                "last_updated": now,
                "completed": False
            }

# 更新每個計時器的時間
now = time.time()
for task_id, timer in st.session_state.timers.items():
    if timer["is_running"] and not timer["completed"]:
        elapsed = int(now - timer["last_updated"])
        timer["remaining"] = max(timer["remaining"] - elapsed, 0)
        timer["last_updated"] = now
        if timer["remaining"] == 0:
            timer["is_running"] = False
            timer["completed"] = True
            play_sound()

# 顯示放大模式的任務
if st.session_state.focus:
    task_id = st.session_state.focus
    timer = st.session_state.timers[task_id]
    mins, secs = divmod(timer["remaining"], 60)

    st.title(f"🔍 專注任務：{timer['name']}")
    st.markdown(
        f"<h1 style='font-size:100px;text-align:center;'>{mins:02d}:{secs:02d}</h1>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("暫停" if timer["is_running"] else "繼續", key=f"focus_toggle_{task_id}"):
            timer["is_running"] = not timer["is_running"]
            timer["last_updated"] = time.time()
    with col2:
        if st.button("重設", key=f"focus_reset_{task_id}"):
            timer["remaining"] = timer["duration"]
            timer["is_running"] = False
            timer["last_updated"] = time.time()
            timer["completed"] = False
    with col3:
        if st.button("返回列表"):
            st.session_state.focus = None

# 顯示任務列表（非放大模式）
else:
    remove_list = []
    for task_id, timer in st.session_state.timers.items():
        mins, secs = divmod(timer["remaining"], 60)
        status = "⏳ 進行中" if timer["is_running"] else ("✅ 完成" if timer["completed"] else "⏸️ 已暫停")

        with st.container():
            st.markdown("---")
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])
            with col1:
                st.markdown(
                    f"**{timer['name']}**<br/>{status}<br/><span style='font-size:30px'>{mins:02d}:{secs:02d}</span>",
                    unsafe_allow_html=True
                )
            with col2:
                if st.button("暫停" if timer["is_running"] else "繼續", key=f"toggle_{task_id}"):
                    timer["is_running"] = not timer["is_running"]
                    timer["last_updated"] = time.time()
            with col3:
                if st.button("重設", key=f"reset_{task_id}"):
                    timer["remaining"] = timer["duration"]
                    timer["is_running"] = False
                    timer["last_updated"] = time.time()
                    timer["completed"] = False
            with col4:
                if st.button("🔍 放大", key=f"zoom_{task_id}"):
                    st.session_state.focus = task_id
                    st.experimental_rerun()
            with col5:
                if st.button("❌ 刪除", key=f"delete_{task_id}"):
                    remove_list.append(task_id)

    # 刪除任務（在 for 外處理避免錯誤）
    for tid in remove_list:
        del st.session_state.timers[tid]

# 每秒平滑刷新
time.sleep(1)
st.experimental_rerun()
