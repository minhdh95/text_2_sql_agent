
# 💬 Text-to-SQL với Gemini và SQLite

Ứng dụng chuyển đổi ngôn ngữ tự nhiên (tiếng Việt hoặc tiếng Anh) thành truy vấn SQL, thực thi trên cơ sở dữ liệu SQLite và trả lại kết quả cho người dùng.

## 🚀 Tính năng chính

- Nhập câu hỏi bằng ngôn ngữ tự nhiên
- AI tự động sinh truy vấn SQL tương ứng
- Truy vấn được thực thi trên cơ sở dữ liệu SQLite
- Trả kết quả và hiển thị câu SQL đã sinh
- Giao diện người dùng đơn giản với Gradio

---

## 📦 Công nghệ sử dụng

- [LangChain](https://www.langchain.com/)
- [Gemini (Google Generative AI)](https://ai.google.dev/)
- [Gradio](https://gradio.app/)
- [SQLite](https://www.sqlite.org/index.html)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📁 Cấu trúc thư mục

```
.
├── text_to_sql_agent.py              # File chính chạy ứng dụng
├── my_data.db           # File SQLite (dữ liệu mẫu)
├── .env                 # Biến môi trường (API key, v.v.)
└── README.md            # Tài liệu dự án
```

---

## ⚙️ Cài đặt và chạy

### 1. Clone dự án và tạo môi trường

```bash
git clone https://github.com/trangq/text_to_sql_agent.git
cd text-to-sql-gemini
python -m venv venv
source venv/bin/activate   # Hoặc venv\Scripts\activate trên Windows
```

### 2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

> Nếu chưa có file `requirements.txt`, bạn có thể dùng:
```bash
pip install langchain langchain-google-genai gradio python-dotenv
```

### 3. Tạo file `.env`

Tạo file `.env` trong thư mục gốc:

```
GOOGLE_API_KEY=your_google_api_key_here
```

> Đăng ký API key tại: https://ai.google.dev/gemini-api/docs/api-key

### 4. Chuẩn bị cơ sở dữ liệu

Tạo file `my_data.db` với bảng và dữ liệu mẫu, hoặc sử dụng công cụ như [DB Browser for SQLite](https://sqlitebrowser.org/).

Ví dụ:
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    purchase_date DATE
);
```

### 5. Chạy ứng dụng

```bash
python text_to_sql_agent.py
```

> Ứng dụng chạy tại: `http://localhost:7861`

---

## 💡 Ví dụ câu hỏi

- "Liệt kê 5 khách hàng gần đây nhất?"
- "How many orders were placed last month?"
- "Có bao nhiêu sản phẩm trong kho?"

---

## 📋 Kết quả đầu ra

Ứng dụng trả về:

- ✅ Kết quả từ truy vấn
- 📄 Câu SQL được sinh ra

---

## 📌 Gợi ý mở rộng

- Hỗ trợ các hệ quản trị khác (PostgreSQL, MySQL…)
- Tích hợp xác thực người dùng
- Xuất kết quả dưới dạng CSV
- Cho phép người dùng tải file SQLite riêng

---


