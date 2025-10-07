import streamlit as st
import pandas as pd
import random

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    df_app = pd.read_csv("question_LTC_APP.csv")
    df_twr = pd.read_csv("question_LTC_TWR.csv")
    df_ltcs = pd.read_csv("question_LTCS.csv")
    return df_app, df_twr, df_ltcs

df_app, df_twr, df_ltcs = load_data()

# ==========================================
# PAGE SETTINGS
# ==========================================
st.set_page_config(page_title="Quiz App", page_icon="🧠", layout="wide")

st.title("🧠 LUYỆN TRẮC NGHIỆM ONLINE")
st.markdown("Ứng dụng luyện thi **APP / TWR** trực tuyến. \
Hỗ trợ 3 chế độ: *Tất cả câu hỏi*, *Luyện tập*, *Thi thử*.")

# ==========================================
# SELECT OPTIONS
# ==========================================
col1, col2 = st.columns(2)
with col1:
    exam_type = st.selectbox("📘 Chọn loại đề", ["APP", "TWR"])
with col2:
    mode = st.selectbox("⚙️ Chọn chế độ", ["Tất cả câu hỏi", "Luyện tập", "Thi thử"])

# ==========================================
# LOAD QUESTIONS
# ==========================================
if exam_type == "APP":
    df_ltc = df_app
else:
    df_ltc = df_twr

if mode == "Tất cả câu hỏi":
    df_final = pd.concat([df_ltc, df_ltcs], ignore_index=True)
else:
    df_ltc_sample = df_ltc.sample(n=35, replace=False)
    df_ltcs_sample = df_ltcs.sample(n=15, replace=False)
    df_final = pd.concat([df_ltc_sample, df_ltcs_sample], ignore_index=True)

df_final.reset_index(drop=True, inplace=True)

# ==========================================
# QUIZ UI
# ==========================================
st.markdown("---")
st.subheader(f"📄 Tổng số câu hỏi: {len(df_final)}")

score = 0
user_answers = {}

for i, row in df_final.iterrows():
    st.markdown(f"### ❓ Câu {i+1}: {row['question']}")

    options = [opt for opt in ['A', 'B', 'C', 'D'] if str(row.get(opt, '')).strip()]
    answer = st.radio(
        "Chọn đáp án:",
        options,
        key=f"q{i}",
        horizontal=True,
        label_visibility="collapsed"
    )

    user_answers[i] = answer

    if mode != "Thi thử" and answer:
        if answer == row["correct_answer"]:
            st.success(f"✅ Đúng! Đáp án: {row['correct_answer']}")
        else:
            st.error(f"❌ Sai! Đáp án đúng là: {row['correct_answer']}")

st.markdown("---")

if mode != "Tất cả câu hỏi":
    if st.button("📤 Nộp bài"):
        correct = sum(
            1 for i, row in df_final.iterrows()
            if user_answers.get(i) == row["correct_answer"]
        )
        total = len(df_final)
        percent = round(correct / total * 100, 2)
        result = "🎯 **ĐẠT**" if correct >= 35 else "❌ **CHƯA ĐẠT**"
        st.success(f"{result} — {correct}/{total} câu đúng ({percent}%)")
