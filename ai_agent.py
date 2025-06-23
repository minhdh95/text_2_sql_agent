import os
import logging
from dotenv import load_dotenv
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import create_sql_agent
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler

# === Load biến môi trường ===
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# === Callback để thu SQL ===
class SQLHandler(BaseCallbackHandler):
    def __init__(self):
        self.sql_result = []

    def on_agent_action(self, action, **kwargs):
        if action.tool in ["sql_db_query", "sql_db_query_checker"]:
            sql_text = action.tool_input.strip()
            if sql_text not in self.sql_result:
                self.sql_result.append(sql_text)



# === Lớp chính ===
class TextToSQLAgent:
    def __init__(self, api_key: str, db_uri: str):
        self.api_key = api_key
        self.db_uri = db_uri
        self.llm = self._init_llm()
        self.db = SQLDatabase.from_uri(self.db_uri)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        self.agent = self._init_agent()

    def _init_llm(self):
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=self.api_key,
            temperature=0.3,
            max_output_tokens=2048
        )

    def _init_agent(self):
        agent = create_sql_agent(
            llm=self.llm,
            db=self.db,
            verbose=True,
            memory=self.memory,
            agent_executor_kwargs={"return_intermediate_steps": True}
        )
        return agent

    def query(self, user_question: str) -> dict:
        try:
            handler = SQLHandler()
            result = self.agent.invoke(
                {"input": user_question},
                config={"callbacks": [handler]}
            )

            output = result.get("output", "Không thể xử lý truy vấn.")
            sql_queries = handler.sql_result

            return {
                "output": output,
                "sql": "\n".join(sql_queries) if sql_queries else "⚠️ Không tìm thấy câu SQL phù hợp."
            }

        except Exception as e:
            logger.exception("Lỗi khi xử lý truy vấn")
            return {
                "output": f"❌ Lỗi hệ thống: {e}",
                "sql": ""
            }


# === Khởi tạo agent ===
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
db_uri = "sqlite:///my_data.db"
agent = TextToSQLAgent(api_key=GOOGLE_API_KEY, db_uri=db_uri)

# === Giao diện Gradio ===
def handle_query(user_input):
    response = agent.query(user_input)
    return response["output"], response["sql"]

demo = gr.Interface(
    fn=handle_query,
    inputs=gr.Textbox(lines=3, label="Câu hỏi (bằng tiếng Việt hoặc tiếng Anh)"),
    outputs=[
        gr.Textbox(label="✅ Kết quả trả về từ database"),
        gr.Textbox(label="📄 Truy vấn SQL được tạo")
    ],
    title="💬 Trợ thủ phân tích dữ liệu với AI",
    description="Nhập câu hỏi bằng ngôn ngữ tự nhiên, AI sẽ trả kết quả và câu SQL tương ứng."
)

if __name__ == "__main__":
    demo.launch(server_port=7861)
