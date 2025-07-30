import streamlit as st
import time

st.set_page_config(page_title="倒數計時器", layout="centered")

st.title("⏱️ 倒數計時器")
st.markdown("這是一個簡單的倒數計時小工具。請輸入任務名稱和時間。")

# 使用者輸入
task_name = st.text_input("📝 任務名稱", "午餐休息")
minutes = st.number_input("⏳ 倒數時間（分鐘）", min_value=1, max_value=120, value=30, step=1)

if st.button("開始倒數"):
    total_seconds = int(minutes * 60)
    st.success(f"✅ 任務【{task_name}】開始倒數 {minutes} 分鐘！")

    # 倒數計時顯示區
    countdown_placeholder = st.empty()

    for remaining in range(total_seconds, -1, -1):
        mins, secs = divmod(remaining, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        countdown_placeholder.markdown(f"## ⏳ 剩下時間：{time_str}")
        time.sleep(1)

    # 完成提醒
    st.balloons()
    st.markdown(f"🎉 任務【{task_name}】倒數結束囉！可以繼續下一件事了～")
