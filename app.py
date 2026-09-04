import streamlit as st
import datetime
import os
import pandas as pd

st.title("課程報名系統")

# 1. 建立文字輸入框
name = st.text_input("請輸入您的姓名")

# 2. 建立下拉選單
course = st.selectbox(
    "請選擇想報名的課程",
    ["工安課程研習班, "投資理財模擬實戰班", "淺能開發班"]
)

# 3. 建立送出按鈕與防呆存檔邏輯
if st.button("確認送出報名"):
    if name:
        # ── 防呆檢查機制 ──
        is_duplicate = False
        if os.path.exists("registrations.txt"):
            try:
                df_check = pd.read_csv("registrations.txt", header=None, names=["報名時間", "學員姓名", "報名課程"])
                # 檢查輸入的姓名是否已經存在於「學員姓名」欄位中
                if name in df_check["學員姓名"].values:
                    is_duplicate = True
            except Exception:
                pass
        
        if is_duplicate:
            st.warning(f"⚠️ 提醒：【{name}】已經完成報名囉，請勿重複提交！")
        else:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("registrations.txt", "a", encoding="utf-8") as f:
                f.write(f"{now},{name},{course}\n")
            st.success(f"太棒了，{name}！您已成功報名：【{course}】（資料已自動存檔）")
    else:
        st.warning("請先輸入您的姓名才能完成報名喔！")

# 4. 讀取並顯示報名名單（結合篩選與下載功能）
st.divider()
st.subheader("📋 目前所有報名名單與後台管理")

if os.path.exists("registrations.txt"):
    try:
        df = pd.read_csv("registrations.txt", header=None, names=["報名時間", "學員姓名", "報名課程"])
        if not df.empty:
            
            filter_options = ["全部顯示", "Python 基礎入門班", "投資理財模擬實戰班", "AI 協作開發班"]
            selected_course = st.selectbox("🔍 篩選欲檢視的課程", filter_options)
            
            if selected_course != "全部顯示":
                display_df = df[df["報名課程"] == selected_course]
            else:
                display_df = df
            
            st.write(f"目前顯示筆數：{len(display_df)} 筆")
            st.dataframe(display_df, use_container_width=True)
            
            csv_data = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 下載完整報名名單 (CSV 檔)",
                data=csv_data,
                file_name="course_registrations.csv",
                mime="text/csv"
            )
            
        else:
            st.info("目前尚無報名紀錄。")
    except Exception:
        st.info("目前尚無報名紀錄。")
else:
    st.info("目前尚無報名紀錄。")
