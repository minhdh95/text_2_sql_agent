import os
from dotenv import load_dotenv
import gradio as gr
from groq import Groq
from sqlalchemy import create_engine, text

# ===== LOAD ENV =====
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===== INIT GROQ =====
client = Groq(api_key=GROQ_API_KEY)

DB_URI = "sqlite:///my_data.db"   # đúng với file bạn đang có
engine = create_engine(DB_URI)
def get_db_schema() -> str:
    schema = ""
    with engine.connect() as conn:
        tables = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        ).fetchall()

        for (table_name,) in tables:
            schema += f"\nTable {table_name} (\n"
            columns = conn.execute(
                text(f"PRAGMA table_info({table_name})")
            ).fetchall()

            for col in columns:
                schema += f"  {col[1]} {col[2]},\n"
            schema += ")\n"

    return schema


# ===== TEXT → SQL =====
def text_to_sql(question: str) -> str:
    schema = get_db_schema()   # 👈 lấy schema thật

    prompt = f"""
Bạn là chuyên gia SQL.

Schema database:
{schema}

Viết câu SQL CHÍNH XÁC để trả lời câu hỏi.
Chỉ trả về SQL thuần, KHÔNG markdown, KHÔNG giải thích.

Câu hỏi:
{question}
"""

    res = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return res.choices[0].message.content.strip()



# ===== RUN SQL =====
def run_sql(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()
    return columns, rows


# ===== RESULT → NGÔN NGỮ TỰ NHIÊN =====
def explain_result(question, columns, rows):
    prompt = f"""
Người dùng hỏi:
{question}

Kết quả truy vấn:
Cột: {list(columns)}
Dữ liệu: {rows}

Hãy trả lời bằng tiếng Việt, dễ hiểu, tự nhiên như người thật.
"""

    res = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return res.choices[0].message.content

def clean_sql(sql: str) -> str:
    sql = sql.strip()

    # Xóa markdown ```sql ... ```
    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

    return sql

# ===== PIPELINE CHÍNH =====
def handle_query(question):
    try:
        raw_sql = text_to_sql(question)
        sql = clean_sql(raw_sql)

        cols, rows = run_sql(sql)
        answer = explain_result(question, cols, rows)

        return answer, sql

    except Exception as e:
        return f"❌ Lỗi: {e}", ""



# ===== GRADIO UI =====
demo = gr.Interface(
    fn=handle_query,
    inputs=gr.Textbox(lines=3, label="💬 Nhập câu hỏi"),
    outputs=[
        gr.Textbox(label="✅ Câu trả lời"),
        gr.Textbox(label="📄 SQL được sinh ra"),
    ],
    title="🧠 AI Text-to-SQL Assistant",
    description="Hỏi bằng tiếng Việt hoặc tiếng Anh. AI sẽ truy vấn DB và trả lời.",
)

if __name__ == "__main__":
    demo.launch(server_port=7861)
