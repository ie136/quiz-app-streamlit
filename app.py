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
col1, col2 = st.columns(2)
with col1:
    quiz_type = st.selectbox("Loại đề", ["APP", "TWR"])
with col2:
    mode = st.selectbox("Chế độ", ["Tất cả câu hỏi", "Luyện tập", "Thi thử"])

# ================== CREATE QUIZ ==================
if st.button("🎲 Tạo đề mới"):
    random_seed = random.randint(1, 999999)
    random.seed(random_seed)

    df_ltc_app = pd.read_csv(FILES["LTC_APP"])
    df_ltc_twr = pd.read_csv(FILES["LTC_TWR"])
    df_ltc_all = pd.concat([df_ltc_app, df_ltc_twr], ignore_index=True)

    df_ltcs = pd.read_csv(FILES["LTCS"])

    if mode == "Tất cả câu hỏi":
        df_final = pd.concat([df_ltc_all, df_ltcs], ignore_index=True)
    else:
        df_ltc_sample = df_ltc_all.sample(n=35, replace=False)
        df_ltcs_sample = df_ltcs.sample(n=15, replace=False)
        df_final = pd.concat([df_ltc_sample, df_ltcs_sample], ignore_index=True)

    df_final.reset_index(drop=True, inplace=True)
    st.session_state["questions"] = df_final
    st.session_state["answers"] = {}
    st.session_state["submitted"] = False  # Reset trạng thái

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
            st.session_state["answers"][i] = answer[0]

        # Hiển thị kết quả khi không ở "Thi thử"
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
        wrong_answers = []

        for i, row in st.session_state["questions"].iterrows():
            chosen = st.session_state["answers"].get(i)
            if chosen == row["correct_answer"]:
                correct += 1
            else:
                wrong_answers.append({
                    "index": i,
                    "Câu": i + 1,
                    "Câu hỏi": row["question"],
                    "Đáp án của bạn": chosen if chosen else "Không chọn",
                    "Đáp án đúng": row["correct_answer"]
                })

        percent = round(correct / total * 100, 2)
        st.session_state["submitted"] = True
        st.session_state["wrong_answers"] = wrong_answers
        st.session_state["score"] = (correct, total, percent)

# ================== SHOW RESULT ==================
if st.session_state.get("submitted", False):
    correct, total, percent = st.session_state["score"]

    st.markdown("## 🎯 Kết quả")
    st.info(f"**{correct}/{total} câu đúng ({percent}%)**")
    if correct >= 35:
        st.success("🎉 ĐẠT")
    else:
        st.error("❌ CHƯA ĐẠT")

    wrong_answers = st.session_state["wrong_answers"]

    # Chỉ hiện chi tiết khi ở Thi thử
    if mode == "Thi thử":
        st.markdown("---")
        st.markdown("### 🧩 Xem lại bài làm")

        show_only_wrong = st.checkbox("🔍 Chỉ hiển thị các câu sai", value=True)

        for i, row in st.session_state["questions"].iterrows():
            chosen = st.session_state["answers"].get(i)
            correct_ans = row["correct_answer"]

            is_wrong = (chosen != correct_ans)
            if show_only_wrong and not is_wrong:
                continue

            # Màu highlight
            box_color = "#2b2b3c"
            if is_wrong:
                border_color = "#ff4d4d"
            else:
                border_color = "#2ecc71"

            chosen_text = chosen if chosen else "Không chọn"
            st.markdown(
                f"""
                <div style='background-color:{box_color};
                            border:2px solid {border_color};
                            border-radius:8px;
                            padding:10px;
                            margin-bottom:10px;'>
                    <b>Câu {i+1}:</b> {row['question']}<br>
                    <span style='color:#66ccff;'>Bạn chọn: {chosen_text}</span><br>
                    <span style='color:#66ff99;'>Đáp án đúng: {correct_ans}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
