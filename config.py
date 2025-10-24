import os

class Settings:
    PORT = int(os.getenv("PORT", 8000))
    LANGGRAPH_API_KEY = os.getenv("LANGGRAPH_API_KEY", "your_langgraph_api_key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///supportai.db")
    FEEDBACK_STORE = "feedback_data.json"
    DEBUG = True

settings = Settings()
