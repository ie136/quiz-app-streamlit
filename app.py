import streamlit as st
import pandas as pd
import random

# ================== SETTINGS ==================
st.set_page_config(page_title="Quiz App", layout="centered")

FILES = {
    "LTC_APP": "question_LTC_APP.csv",
    "LTC_TWR": "question_LTC_TWR.csv",
    "LTCS": "question_LTCS.csv",
}

# ================== UI HEADER ==================
st.title("🧠 LUYỆN TRẮC NGHIỆM ONLINE")
st.markdown(
    """
    <style>
    * { word-wrap: break-word; }
    .stRadio > div { flex-direction: column; align-items: flex-start; }
    div.row-widget.stRadio > div[role='radiogroup'] label { 
        display: block; 
        white-space: normal !important; 
        line-height: 1.5;
    }
    .question-box {
        background-color: #2b2b3c;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        color: #f0f0f0;
        font-size: 17px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== SELECTION PANEL ==================
col1, col2, col3 = st.columns(3)
with col1:
    quiz_type = st.selectbox("Loại đề", ["APP", "TWR"])
with col2:
    mode = st.selectbox("Chế độ", ["Tất cả câu hỏi", "Luyện tập", "Thi thử"])
with col3:
    seed_choice = st.selectbox("Đề", ["Đề 1", "Đề 2", "Đề 3", "Đề 4", "Đề 5"])

# ================== CREATE QUIZ ==================
if st.button("🎲 Tạo đề"):
    seed = int(seed_choice.split()[-1])
    random.seed(seed)

    # Load data
    if quiz_type == "APP":
        df_ltc = pd.read_csv(FILES["LTC_APP"])
    else:
        df_ltc = pd.read_csv(FILES["LTC_TWR"])
    df_ltcs = pd.read_csv(FILES["LTCS"])

    # Select question set
    if mode == "Tất cả câu hỏi":
        df_final = pd.concat([df_ltc, df_ltcs], ignore_index=True)
    else:
        df_ltc_sample = df_ltc.sample(n=35, random_state=seed)
        df_ltcs_sample = df_ltcs.sample(n=15, random_state=seed)
        df_final = pd.concat([df_ltc_sample, df_ltcs_sample], ignore_index=True)

    df_final.reset_index(drop=True, inplace=True)

    st.session_state["questions"] = df_final
    st.session_state["answers"] = {}

# ================== DISPLAY QUESTIONS ==================
if "questions" in st.session_state:
    st.divider()
    st.subheader(f"📋 {len(st.session_state['questions'])} câu hỏi")

    for i, row in st.session_state["questions"].iterrows():
        st.markdown(f"<div class='question-box'><b>Câu {i+1}:</b> {row['question']}</div>", unsafe_allow_html=True)
        options = [f"{opt}. {row[opt]}" for opt in ["A", "B", "C", "D"] if str(row[opt]) != "nan" and row[opt] != ""]
        key = f"q{i}"
        answer = st.radio(" ", options, index=None, key=key, label_visibility="collapsed")

        if answer:
            st.session_state["answers"][i] = answer[0]  # Lưu chữ cái A/B/C/D

        # Hiện đáp án đúng nếu không ở chế độ Thi thử
        if mode != "Thi thử" and answer:
            if answer[0] == row["correct_answer"]:
                st.success("✅ Chính xác!")
            else:
                st.error(f"❌ Sai! Đáp án đúng là {row['correct_answer']}")
        st.markdown("---")

    # ================== SUBMIT ==================
    if st.button("📤 Nộp bài"):
        correct = 0
        total = len(st.session_state["questions"])
        for i, row in st.session_state["questions"].iterrows():
            if st.session_state["answers"].get(i) == row["correct_answer"]:
                correct += 1
        percent = round(correct / total * 100, 2)

        st.markdown("## 🎯 Kết quả")
        st.info(f"**{correct}/{total} câu đúng ({percent}%)**")
        if correct >= 35:
            st.success("🎉 ĐẠT")
        else:
            st.error("❌ CHƯA ĐẠT")
