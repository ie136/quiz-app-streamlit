import streamlit as st
import pandas as pd
import random
from datetime import datetime

# -----------------------
# Cấu hình giao diện
# -----------------------
st.set_page_config(page_title="HUY QUIZ APP", layout="wide")
st.markdown(
    """
    <style>
    .correct {background-color: #1cbf4b; color: white; font-weight: bold; padding: 6px 10px; border-radius: 6px;}
    .wrong {background-color: #e74c3c; color: white; font-weight: bold; padding: 6px 10px; border-radius: 6px;}
    .question-box {
        background: #23233a; 
        padding: 18px; 
        border-radius: 16px; 
        margin-bottom: 12px;
        color: #fff;
    }
    body {
        background-color: #1c1c28;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

# -----------------------
# Nạp dữ liệu câu hỏi
# -----------------------
@st.cache_data
def load_data():
    df_ltc = pd.read_csv("question_LTC.csv")
    df_ltcs = pd.read_csv("question_LTCS.csv")
    return df_ltc, df_ltcs

df_ltc, df_ltcs = load_data()

# -----------------------
# Giao diện chọn chế độ
# -----------------------
st.sidebar.title("⚙️ Cấu hình")
mode = st.sidebar.selectbox("Chế độ", ["Tất cả câu hỏi", "Luyện tập", "Thi thử"])
show_answer = st.sidebar.checkbox("Hiện đáp án khi chọn", value=(mode != "Thi thử"))
seed = st.sidebar.number_input("Chọn mã đề (1-9999)", min_value=1, max_value=9999, value=1)

if mode == "Tất cả câu hỏi":
    questions = pd.concat([df_ltc, df_ltcs], ignore_index=True)
else:
    random.seed(seed)
    df_ltc_sample = df_ltc.sample(n=35, replace=False)
    df_ltcs_sample = df_ltcs.sample(n=15, replace=False)
    questions = pd.concat([df_ltc_sample, df_ltcs_sample], ignore_index=True)

questions.reset_index(drop=True, inplace=True)

# -----------------------
# Bộ nhớ session
# -----------------------
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# -----------------------
# Bộ đếm realtime
# -----------------------
total = len(questions)
answered = len(st.session_state.answers)
correct = sum(
    1 for i, v in st.session_state.answers.items()
    if v == questions.loc[i, "correct_answer"]
)
wrong = answered - correct

if mode in ["Luyện tập", "Tất cả câu hỏi"]:
    st.markdown(
        f"<div style='text-align:center; font-size:22px; font-weight:bold; background:#23233a; padding:10px; border-radius:10px;'>"
        f"📊 {answered}/{total} | <span style='color:#1cbf4b;'>✅ {correct}</span> | <span style='color:#e74c3c;'>❌ {wrong}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

# -----------------------
# Hiển thị câu hỏi
# -----------------------
st.title("HUY QUIZ APP")
st.write(f"### 🎯 Chế độ: {mode}")

for idx, row in questions.iterrows():
    st.markdown(f"<div class='question-box'>**Câu {idx+1}: {row['question']}**</div>", unsafe_allow_html=True)
    
    # Tạo danh sách đáp án có nội dung
    options = []
    labels = []
    for opt in ["A", "B", "C", "D"]:
        value = str(row.get(opt, "")).strip()
        if value and value.lower() != "nan":
            options.append(opt)
            labels.append(f"{opt}. {value}")

    # Hiển thị radio với nội dung thật
    choice_label = st.radio(
        f"Chọn đáp án cho câu {idx+1}",
        labels,
        key=f"q_{idx}",
        index=None,
        horizontal=False
    )

    if choice_label:
        choice = choice_label.split(".")[0]
        st.session_state.answers[idx] = choice
        if show_answer or st.session_state.submitted:
            correct_ans = row["correct_answer"]
            if choice == correct_ans:
                st.markdown(f"<span class='correct'>✅ Đúng rồi!</span>", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<span class='wrong'>❌ Sai</span> &nbsp;→ Đáp án đúng là: <b>{correct_ans}. {row[correct_ans]}</b>",
                    unsafe_allow_html=True
                )

    st.divider()

# -----------------------
# Nộp bài
# -----------------------
if mode in ["Luyện tập", "Thi thử"]:
    if st.button("📤 Nộp bài"):
        st.session_state.submitted = True
        total = len(questions)
        answered = len(st.session_state.answers)
        correct = sum(
            1 for i, v in st.session_state.answers.items()
            if v == questions.loc[i, "correct_answer"]
        )
        wrong = answered - correct

        passed = correct >= 35
        color = "#1cbf4b" if passed else "#e74c3c"
        st.markdown(
            f"<div style='text-align:center; background:#23233a; padding:18px; border-radius:12px;'>"
            f"<span style='font-size:36px; color:{color}; font-weight:bold;'>{'ĐẬU' if passed else 'RỚT'}</span><br>"
            f"<span style='font-size:24px;'>✅ {correct}/{total} câu đúng</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Lưu log
        with open("log_streamlit.txt", "a", encoding="utf-8") as f:
            f.write(f"{mode} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {correct}/{total}\n")
