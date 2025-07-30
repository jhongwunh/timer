import streamlit as st
import time

# 頁面設定
st.set_page_config(page_title="平滑倒數計時器", layout="centered")

# CSS：模擬翻頁時鐘風格
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

st.title("🕒 平滑倒數計時器（翻頁風格）")

# 任務與時間輸入
with st.form("start_form"):
    task_name = st.text_input("📝 任務名稱", "午餐休息")
    minutes = st.number_input("⏳ 倒數時間（分鐘）", min_value=1, max_value=120, value=5)
    start = st.form_submit_button("開始倒數")

if start:
    total_seconds = int(minutes * 60)
    st.success(f"✅ 任務【{task_name}】開始倒數 {minutes} 分鐘")

    # 動態容器
    timer_display = st.empty()

    # 倒數邏輯
    for remaining in range(total_seconds, -1, -1):
        mins, secs = divmod(remaining, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        timer_display.markdown(f"<div class='timer'>{time_str}</div>", unsafe_allow_html=True)
        time.sleep(1)

    st.balloons()
    st.success(f"🎉 任務【{task_name}】倒數完成！")
