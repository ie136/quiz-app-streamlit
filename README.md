# 🎓 HUY QUIZ APP – Ứng dụng luyện thi trắc nghiệm trực tuyến

Ứng dụng luyện thi trắc nghiệm dành cho học viên **APP/TWR & LTC/LTCS**,  
chạy trực tiếp trên web (không cần cài đặt) – sử dụng framework **Streamlit**.

🌐 **Link chạy trực tiếp:**  
👉 [https://ie136-quiz-app-streamlit.streamlit.app](https://ie136-quiz-app-streamlit.streamlit.app)

---

## 🚀 Tính năng chính

| Tính năng | Mô tả |
|-----------|--------|
| 🧠 **Ba chế độ học** | • Tất cả câu hỏi<br>• Luyện tập (hiện đáp án khi chọn)<br>• Thi thử (ẩn đáp án, chỉ hiện khi nộp bài) |
| 🎲 **Random thông minh** | 35 câu LTC + 15 câu LTCS trong mỗi lần thi |
| ✅ **Hiển thị đúng/sai** | Highlight màu xanh – đỏ, cập nhật realtime |
| 📊 **Thanh đếm tiến độ** | Hiển thị số câu đã làm, đúng, sai bằng emoji |
| 📱 **Chạy mượt trên iPhone / iPad** | Dạng web app – có thể thêm ra màn hình chính |
| 🧾 **Ghi log kết quả** | Lưu lịch sử thi vào file `log_streamlit.txt` |

---

## 🧩 Cấu trúc dự án

quiz-app-streamlit/
├── app_streamlit.py # Code chính của ứng dụng Streamlit
├── question_LTC.csv # Câu hỏi Lý thuyết chung (LTC)
├── question_LTCS.csv # Câu hỏi Lý thuyết cơ sở (LTCS)
└── README.md # (file hướng dẫn này)

---

## 🧠 Cách chạy (cho người phát triển)

### 1️⃣ Cài môi trường Python
```bash
pip install streamlit pandas

streamlit run app_streamlit.py

☁️ Cách triển khai lên Streamlit Cloud
1️⃣ Tạo repo trên GitHub

Tên gợi ý: quiz-app-streamlit

Đặt 3 file: app_streamlit.py, question_LTC.csv, question_LTCS.csv

2️⃣ Truy cập: https://share.streamlit.io

Đăng nhập bằng tài khoản GitHub

Nhấn New app

Chọn:

Repository → ie136/quiz-app-streamlit

Branch → main

File → app_streamlit.py

Bấm Deploy

3️⃣ Mở app web

Sau vài phút, bạn sẽ nhận link dạng:

https://ie136-quiz-app-streamlit.streamlit.app

📱 Sử dụng trên điện thoại
✅ iPhone / iPad

Mở link bằng Safari

Chọn Share → Add to Home Screen

App sẽ xuất hiện như ứng dụng riêng biệt

✅ Android

Mở link bằng Chrome

Chọn Add to Home Screen

🧾 Ghi chú thêm

Đảm bảo 2 file CSV có cấu trúc cột như sau:

question,A,B,C,D,correct_answer


question: nội dung câu hỏi

A, B, C, D: 4 phương án

correct_answer: ký tự A / B / C / D

Không để dòng trống hoặc nan trong file CSV.

Streamlit tự động rebuild app mỗi khi commit code mới lên GitHub.

🧰 Liên hệ & ghi công

Tác giả / Maintainer: ie136

Công nghệ: Python 3.10+, Streamlit, Pandas

Trợ lý kỹ thuật: ChatGPT (OpenAI GPT-5)
